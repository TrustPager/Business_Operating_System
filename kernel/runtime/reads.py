"""Scaled reads/writes — fan-out GETs, pagination, and bulk writes.

Driver-agnostic: every function takes the bound `get`/`write` callable as its
first argument instead of importing a global. A driver (or a tool re-exporting
these) binds its own api_get / write fn:

    from functools import partial
    parallel_get = lambda calls, **kw: kernel_parallel_get(api_get, calls, **kw)

The kernel itself knows nothing about any vendor, the base URL, or the key.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Iterator

from kernel.runtime.errors import BOSError

DEFAULT_PARALLEL_WORKERS = 8


def parallel_get(get_fn: Callable[..., dict[str, Any]],
                 calls: list[tuple[str, dict[str, Any]]],
                 max_workers: int = DEFAULT_PARALLEL_WORKERS) -> dict[str, dict[str, Any]]:
    """Fan out multiple GET requests in parallel using the supplied get_fn.

    Args:
        get_fn: bound GET callable, get_fn(path, **params) -> dict.
        calls: list of (path, params_dict) tuples. The path is also the result key.
        max_workers: parallel HTTP threads (default 8).

    Returns:
        Dict mapping each path to its response (or an `{"error": "..."}` dict
        on failure). Never raises — failures land per-key in the result.
    """
    out: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_path = {
            pool.submit(get_fn, path, **params): path
            for path, params in calls
        }
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                out[path] = future.result()
            except BOSError as e:
                out[path] = {"error": str(e)}
            except Exception as e:  # noqa: BLE001 — last-resort safety net
                out[path] = {"error": f"Unexpected error on {path}: {e}"}
    return out


def paginate(get_fn: Callable[..., dict[str, Any]], path: str,
             max_pages: int | None = None,
             **params: Any) -> Iterator[dict[str, Any]]:
    """Yield every row across every page of a list endpoint via get_fn.

    Auto-follows pagination.next_cursor until has_more is false (or max_pages
    is reached, if set). Default API limit is small — pass limit=100 to minimise
    calls. The path-param `after` is reserved for the cursor — don't pass it.
    """
    cursor: str | None = None
    pages = 0
    while True:
        call_params = dict(params)
        if cursor:
            call_params["after"] = cursor
        response = get_fn(path, **call_params)
        rows = response.get("data", []) if isinstance(response, dict) else []
        for row in rows:
            yield row
        pages += 1
        if max_pages is not None and pages >= max_pages:
            return
        pagination = response.get("pagination", {}) if isinstance(response, dict) else {}
        if not pagination.get("has_more"):
            return
        cursor = pagination.get("next_cursor")
        if not cursor:
            return


def bulk_apply(write_fn: Callable[[Any], Any], items: list[Any],
               parallelism: int = 4,
               on_error: str = "collect",
               progress: Callable[[int, int, str], None] | None = None,
               *, approval_cls: type | None = None) -> dict[str, Any]:
    """Apply a write function across many items with progress + error aggregation.

    Args:
        write_fn: callable taking a single item, returning anything
        items: list of inputs to write_fn
        parallelism: concurrent writes (default 4 — keep low to avoid 429s)
        on_error: 'collect' (default) accumulates errors and continues
                  'raise' raises on first failure
        progress: optional callback(completed, total, item_summary) for logging
        approval_cls: the type that signals "queued for approval" (caller's
                  ApprovalPending). Results of that type land in `queued`.

    Returns:
        {
          "total": N,
          "succeeded": [{"item": ..., "result": ...}, ...],
          "failed":    [{"item": ..., "error": "..."}, ...],
          "queued":    [{"item": ..., "approval_id": "..."}, ...],   # 202 responses
        }
    """
    succeeded: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    queued: list[dict[str, Any]] = []
    total = len(items)
    completed = 0

    with ThreadPoolExecutor(max_workers=parallelism) as pool:
        futures = {pool.submit(write_fn, item): item for item in items}
        for future in as_completed(futures):
            item = futures[future]
            completed += 1
            try:
                result = future.result()
                if approval_cls is not None and isinstance(result, approval_cls):
                    queued.append({"item": item,
                                   "approval_id": getattr(result, "approval_id", None)})
                else:
                    succeeded.append({"item": item, "result": result})
            except BOSError as e:
                if on_error == "raise":
                    raise
                failed.append({"item": item, "error": str(e)})
            except Exception as e:  # noqa: BLE001
                if on_error == "raise":
                    raise
                failed.append({"item": item, "error": f"Unexpected: {e}"})
            if progress:
                summary = str(item)[:60]
                progress(completed, total, summary)

    return {
        "total": total,
        "succeeded": succeeded,
        "failed": failed,
        "queued": queued,
    }
