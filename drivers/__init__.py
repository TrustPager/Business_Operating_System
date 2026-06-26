"""drivers — vendor-specific bindings over the vendor-neutral kernel.

Each driver (e.g. drivers/trustpager) parameterizes the kernel for ONE vendor:
its base URL, key resolver, key shape to redact, per-HTTP-code messages, and
approval URL. Dependencies are one-way: a driver imports from kernel.runtime.*
(and stdlib) only — never from tools/. The kernel never imports a driver.
"""
