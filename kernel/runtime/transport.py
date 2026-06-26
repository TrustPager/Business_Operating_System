"""HTTP transport — the vendor-neutral network seam for the BOS kernel.

This is the mechanism that issues an authenticated HTTP request and turns the
result into either a parsed dict, an ApprovalPending (202 = queued for human
approval), or a friendly BOSError. It knows NOTHING about any specific vendor:
everything provider-specific arrives through a DriverConfig.

A driver builds one DriverConfig describing its API (base URL, how to resolve
the key, the secret-key shape to redact, the per-HTTP-code human messages, the
approval URL) and then calls `request(cfg, method, path, ...)`.

Design notes:
  - The offline guard (is_offline()) runs BEFORE cfg.key_resolver() so a real
    key is never read in tests/CI. tests/test_safety.py depends on this order.
  - The actual network call goes through the module-level `_http` indirection
    so tests can monkeypatch kernel.runtime.transport._http without a socket.
  - Retry/backoff for 429 (honouring Retry-After) and 5xx is preserved here.
  - Per-code messages come from cfg.error_map; absent codes fall back to a
    GENERIC kernel message. No vendor literal appears in this file.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable

from kernel.runtime.errors import BOSError
from kernel.runtime.offline import is_offline
from kernel.runtime.redaction import register_secret_pattern

DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_RETRIES_ON_429 = 3
DEFAULT_RETRIES_ON_5XX = 2


@dataclass
class DriverConfig:
    """Everything the transport needs to talk to ONE vendor's API.

    Fields:
        base_url:       API base, no trailing slash (e.g. "https://x/api/v1").
        key_resolver:   zero-arg callable returning the bearer token. Called
                        lazily, and never when offline.
        secret_pattern: regex matching this vendor's key shape. Registered with
                        the redaction registry on construction so the key never
                        lands in a journal/log.
        error_map:      {http_code: human_message_template}. Keys are normally
                        an exact int HTTP code; the string sentinel "5xx" is
                        also honoured as a fallback template for any 500-599
                        code with no exact-code entry (so a driver can give one
                        rich server-error message without listing every code).
                        The template may contain {path}, {url}, {detail},
                        {code}, {available} placeholders; any subset is fine
                        (missing keys are tolerated).
        approval_url:   where the operator approves a queued (202) write.
        extra_headers:  optional headers merged into every request.
    """

    base_url: str
    key_resolver: Callable[[], str]
    secret_pattern: str
    # Keys are exact int HTTP codes, plus an optional "5xx" string sentinel
    # honoured as a fallback for any 500-599 code (see _format_http_error).
    error_map: dict[int | str, str]
    approval_url: str
    extra_headers: dict[str, str] | None = None

    def __post_init__(self) -> None:
        # Register this driver's key shape so any key that ever surfaces in a
        # journal/log line gets masked. Idempotent in the registry.
        if self.secret_pattern:
            register_secret_pattern(self.secret_pattern)


@dataclass
class ApprovalPending:
    """Returned (NOT raised) when an API write returns 202 + approval_id.

    The action has been queued for human approval, not executed. Callers can:
      - hand the approval_id back to the operator to approve in-app
      - access .body for the full 202 response payload

    The str() form is human-readable. approval_url is supplied by the driver
    config at request time — the kernel hardcodes no vendor URL.
    """

    approval_id: str
    body: dict[str, Any]
    approval_url: str = ""

    def __str__(self) -> str:
        where = f" Approve at {self.approval_url}" if self.approval_url else ""
        return f"Queued for approval (id: {self.approval_id})." + where


def _build_url(base_url: str, path: str, params: dict[str, Any] | None = None) -> str:
    """Build a full URL from a base, a path (with/without leading slash), and query params."""
    path = path.lstrip("/")
    url = f"{base_url.rstrip('/')}/{path}"
    if params:
        clean = {k: ("true" if v is True else "false" if v is False else str(v))
                 for k, v in params.items() if v is not None}
        if clean:
            url = f"{url}?{urllib.parse.urlencode(clean)}"
    return url


def _parse_response_body(raw: bytes) -> dict[str, Any]:
    """Parse a JSON response body. Returns {} for empty/non-JSON bodies."""
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {"_raw": raw[:300].decode("utf-8", errors="replace")}


def _http(req: urllib.request.Request, timeout: int):
    """Thin indirection over urllib.request.urlopen.

    Exists so tests can monkeypatch kernel.runtime.transport._http and feed a
    fake response/error without opening a socket. Returns a context-manager
    response object (what urlopen returns).
    """
    return urllib.request.urlopen(req, timeout=timeout)


def request(cfg: DriverConfig, method: str, path: str,
            params: dict[str, Any] | None = None,
            body: dict[str, Any] | None = None,
            timeout: int = DEFAULT_TIMEOUT_SECONDS,
            extra_headers: dict[str, str] | None = None,
            _attempt: int = 0) -> dict[str, Any] | ApprovalPending:
    """Low-level HTTP request, parameterized by a DriverConfig.

    Returns:
        - dict on 2xx (parsed JSON response)
        - ApprovalPending on 202 (write was queued, not executed)
        - Raises BOSError on every other failure mode

    Retry behaviour:
        - 429: retries up to DEFAULT_RETRIES_ON_429 times, honouring Retry-After
        - 5xx: retries up to DEFAULT_RETRIES_ON_5XX times with exponential backoff
        - Network errors: no retry — bubbles up immediately

    The offline guard fires BEFORE cfg.key_resolver() so a real key is never
    read in tests/CI.
    """
    if is_offline():
        raise BOSError(
            f"BOS is in offline mode (BOS_OFFLINE is set) — refusing the {method} {path} "
            f"network call.\nThis guard means tests and CI can never reach the live API or "
            f"read a real API key. Mock api_get/api_post with fixtures instead "
            f"(see tools/test-skill.py)."
        )
    api_key = cfg.key_resolver()
    url = _build_url(cfg.base_url, path, params)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": "BusinessOperatingSystem/1.0",
    }
    if cfg.extra_headers:
        headers.update(cfg.extra_headers)
    if extra_headers:
        headers.update(extra_headers)
    data: bytes | None = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with _http(req, timeout) as resp:
            payload = resp.read()
            parsed = _parse_response_body(payload)
            # 202 = queued for approval. Return ApprovalPending, don't raise.
            if resp.status == 202:
                approval_id = (
                    parsed.get("approval_id")
                    or parsed.get("id")
                    or (parsed.get("data") or {}).get("approval_id")
                    or "unknown"
                )
                return ApprovalPending(approval_id=approval_id, body=parsed,
                                       approval_url=cfg.approval_url)
            return parsed
    except urllib.error.HTTPError as e:
        detail_raw = b""
        try:
            detail_raw = e.read()
        except OSError:
            pass
        detail_parsed = _parse_response_body(detail_raw)
        detail_str = (detail_raw or b"").decode("utf-8", errors="replace")[:500]

        # 429 — rate limited. Retry honouring Retry-After.
        if e.code == 429 and _attempt < DEFAULT_RETRIES_ON_429:
            retry_after = e.headers.get("Retry-After") if hasattr(e, "headers") else None
            wait = int(retry_after) if retry_after and retry_after.isdigit() else 2 ** _attempt
            time.sleep(min(wait, 30))
            return request(cfg, method, path, params=params, body=body,
                           timeout=timeout, extra_headers=extra_headers,
                           _attempt=_attempt + 1)

        # 5xx — server error. Retry a couple of times then give up.
        if 500 <= e.code < 600 and _attempt < DEFAULT_RETRIES_ON_5XX:
            time.sleep(2 ** _attempt)
            return request(cfg, method, path, params=params, body=body,
                           timeout=timeout, extra_headers=extra_headers,
                           _attempt=_attempt + 1)

        raise BOSError(_format_http_error(cfg, e.code, path, url, detail_str,
                                          detail_parsed)) from None
    except urllib.error.URLError as e:
        raise BOSError(
            f"Could not reach the API.\n"
            f"Check your internet connection. Underlying error: {e.reason}"
        ) from None
    except (json.JSONDecodeError, OSError) as e:
        raise BOSError(f"Unexpected response from {path}: {e}") from None


def _format_http_error(cfg: DriverConfig, code: int, path: str, url: str,
                       detail_str: str, detail_parsed: dict[str, Any]) -> str:
    """Build the user-facing message for a non-retryable HTTP error.

    Prefers the vendor-specific template from cfg.error_map; falls back to a
    GENERIC kernel message (no vendor literal) when the code isn't mapped.

    Lookup order for the template:
      1. an exact int key for this code (e.g. error_map[404])
      2. for any 500-599 code, the string sentinel error_map["5xx"]
    This lets a driver supply ONE rich server-error message (with {detail}) for
    the whole 5xx band without enumerating every code, while the kernel keeps
    no vendor strings of its own.

    Templates may reference any subset of {path}, {url}, {code}, {detail},
    {available}. {detail} resolves to the server's response body/message, so a
    driver can echo what the server said (e.g. on 429/5xx). A driver that wants
    to surface a validation endpoint's available-options hint (the common 422
    shape) puts {available} in that code's template; {available} resolves to the
    empty string when the server sent no such hint, so it stays inert for
    codes/responses without one.
    """
    # Pull a server-side message + any "available" hint (common 422 shape).
    err = detail_parsed.get("error", {}) if isinstance(detail_parsed, dict) else {}
    server_msg = err.get("message") if isinstance(err, dict) else None
    available = (err.get("details") or {}).get("available") if isinstance(err, dict) else None
    avail_str = f"\nValid options: {available}" if available else ""

    # Exact-code template first; then the "5xx" sentinel for any server-error
    # code. Both are driver-supplied — the kernel hardcodes no vendor template.
    template = cfg.error_map.get(code)
    if template is None and 500 <= code < 600:
        template = cfg.error_map.get("5xx")
    if template is not None:
        try:
            base = template.format(path=path, url=url, code=code,
                                   detail=server_msg or detail_str,
                                   available=avail_str)
        except (KeyError, IndexError):
            # A template with an unexpected placeholder must not crash error
            # reporting — fall back to the raw template text.
            base = template
        return base

    # Generic kernel fallback — vendor-neutral. Reached when neither an
    # exact-code template nor (for 5xx) the "5xx" sentinel is present in
    # cfg.error_map. 429 and 5xx land here by default with the generic
    # messages below; a driver MAY override either with its own richer message
    # (e.g. echoing {detail} or adding a docs link) by adding an error_map
    # entry (429 as an exact key, "5xx" as the band sentinel).
    server_said = f"\nServer said: {server_msg or detail_str}" if (server_msg or detail_str) else ""
    if 500 <= code < 600:
        return (
            f"The API returned a server error ({code}) for {path}.\n"
            f"This is usually temporary; try again shortly.{server_said}"
        )
    if code == 429:
        return (
            f"Rate-limited by the API ({code}) on {path} after retries.\n"
            f"Slow down the request rate or contact support to raise your limit."
        )
    return (
        f"HTTP {code} on {path}.\n"
        f"Full URL was: {url}{server_said}"
    )
