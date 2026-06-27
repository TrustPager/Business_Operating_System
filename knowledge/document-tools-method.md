# Document tools method

**The standard way BOS turns any document into something Claude can work with is Microsoft MarkItDown.** It converts PDF, Word, Excel, PowerPoint, images (with OCR / optional AI description), HTML, CSV, JSON, and more into clean Markdown. Markdown is the format an LLM reads most reliably, so every "read a document" workflow goes through MarkItDown first, then Claude works on the Markdown.

There are two directions, and they use different tools — don't conflate them:

- **Extract / read (MarkItDown):** document → Markdown → structured data. This is the standard ingest layer. Skills: `/extract-document` (and the engine under `/import-from-anywhere`).
- **Update / write (a PDF writer):** data → into a PDF (fill form fields, or generate a filled copy). MarkItDown does NOT do this — it only reads. Skill: `/update-pdf`. MarkItDown is still used here to *read the blank form first* so Claude understands its fields and labels before filling.

## The standard tool

MarkItDown is invoked through the bundled wrapper so behaviour is consistent and the install is checked once:

```bash
python tools/markitdown_convert.py <path-to-file>      # prints Markdown to stdout
python tools/markitdown_convert.py <path> --out out.md  # or write to a file
```

If it isn't installed, the wrapper says exactly how: `pip install markitdown` (or `pip install 'markitdown[all]'` for the image/audio extras). It is a one-time setup, like the rest of BOS.

## Supported inputs (what you can throw at it)
PDF, Word (.docx), Excel (.xlsx/.csv), PowerPoint (.pptx), images (.png/.jpg — text via OCR, optional AI description), HTML, JSON, XML, ZIP (walks the contents), and plain text. If a format isn't supported, say so rather than guessing at the content.

## Why this is the standard
One reliable conversion path for every document type means skills don't each reinvent parsing, and Claude always works on clean Markdown rather than raw bytes or brittle text dumps. Building new document skills on MarkItDown keeps them consistent and lets them inherit format support for free.

## Building new skills on it
Any new skill that needs to read a file (extract data, summarise a contract, pull figures from a statement, ingest a paper form) calls `tools/markitdown_convert.py` to get Markdown first, then does its specific work on that. Don't write bespoke per-format parsing.

---

# The two keyless drivers

BOS has two keyless document drivers. They run locally with no account and no network — one-time install, then offline forever. Together they cover read and write so a brand-new owner can do real document work at zero accounts.

| Driver | Direction | Tool(s) | `requires_driver` id |
|---|---|---|---|
| **MarkItDown** | keyless **READ** | `tools/markitdown_convert.py` | `markitdown` |
| **doc-lib-set** | keyless **WRITE** (and precise read) | `tools/write_xlsx.py`, `tools/write_docx.py`, `tools/make_pdf.py`, `tools/pdf_tables.py` | `doclib` |

A skill declares the driver it leans on in its manifest (`requires_driver: markitdown` or `requires_driver: doclib`). Both ids are in the onboarding binding check's keyless set (`tools/check-onboarding-binding.py` `_KEYLESS_DRIVERS`), so an app that declares either still counts as a genuine keyless instant-win.

## MarkItDown — the canonical keyless READ driver
MarkItDown (above) is the **one** keyless way to turn a document into something Claude can read: any file → clean Markdown. Every "read a file" workflow goes through `tools/markitdown_convert.py`. Downstream Wave-1 apps (transcript-summary, import-from-anywhere) lean on this as their clean keyless read path — they never reach into a CRM to read a file. `requires_driver: markitdown`.

## doc-lib-set — the keyless WRITE driver (`doclib`)
The write counterpart. Where MarkItDown reads, doc-lib-set produces a real file an owner can open and send. Four thin wrappers, each mirroring the MarkItDown wrapper exactly: an argparse CLI, an `INSTALL_HINT`, **exit 2** with a one-line `pip install` hint when the lib is missing, **exit 1** on a real error, clean stdout/stderr, no network at runtime.

| Wrapper | Library | What it does |
|---|---|---|
| `tools/write_xlsx.py` | **openpyxl** | Write a real `.xlsx` from JSON rows (optional bold header, sheet title). |
| `tools/write_docx.py` | **python-docx** | Write a real `.docx` from JSON blocks (heading / paragraph / bullet). |
| `tools/make_pdf.py` | **reportlab** | Generate a PDF from JSON blocks (heading / paragraph / bullet). |
| `tools/pdf_tables.py` | **pdfplumber** | Extract a PDF's table grid (or `--text`) as structured JSON — beyond what MarkItDown's flattened Markdown gives you. |

```bash
python tools/write_xlsx.py --out pricing.xlsx --rows '[["Item","Qty","Price"],["Site visit",1,120]]' --header
python tools/write_docx.py --out proposal.docx --blocks '[{"type":"heading","text":"Proposal"},{"type":"paragraph","text":"Thanks."}]'
python tools/make_pdf.py   --out brief.pdf      --blocks '[{"type":"heading","text":"Pre-call brief"},{"type":"bullet","text":"Ask about response time."}]'
python tools/pdf_tables.py statement.pdf                 # tables -> JSON on stdout
python tools/pdf_tables.py statement.pdf --text          # page text instead
```

Each wrapper also reads its JSON from stdin if `--rows`/`--blocks` is omitted, so Claude can pipe a generated payload straight in.

### Read vs write — don't conflate
- **Read** a document → `tools/markitdown_convert.py` (Markdown) or `tools/pdf_tables.py` (precise PDF grid).
- **Write / generate** a document → `tools/write_xlsx.py` / `tools/write_docx.py` / `tools/make_pdf.py`.
- **Fill an existing PDF form** is still the READ-then-write path under `/update-pdf` (read the blank form with MarkItDown so Claude understands the fields, then write). `make_pdf.py` generates a *fresh* PDF from data — it does not fill an existing form's fields.

### The install-once story
Like MarkItDown, the doc libs are vendored tool dependencies, **not** kernel dependencies. The kernel stays pure stdlib and vendor-neutral; these libs live only behind `tools/` wrappers and install on first use:

```bash
pip install openpyxl python-docx pdfplumber reportlab
```

If a lib isn't installed, the wrapper prints the exact one-line `pip install` and exits 2 — the same graceful path MarkItDown uses. One-time setup, then offline forever.

### Gated extras (NOT installed by default)
- **OCRmyPDF** — for OCR-ing a scanned PDF into a searchable one. Heavy (pulls a Tesseract system dependency), so it is **gated behind a one-time install preflight**: only prompt for it when a workflow actually hits a scanned/image-only PDF, then `pip install ocrmypdf` (plus the system Tesseract). Never assume it's present.
- **python-pptx** — writing `.pptx` decks is **on-demand only**: pull it in when a deck is genuinely the deliverable, not as part of the base doc-lib-set install.

## Licenses — all permissive, MIT/BSD (no AGPL/GPL)
The kernel must stay MIT-clean; every vendored doc lib was confirmed permissive:

| Library | License |
|---|---|
| openpyxl | **MIT** |
| python-docx | **MIT** |
| pdfplumber | **MIT** |
| reportlab (`reportlab` open-source toolkit) | **BSD** (3-clause) |
| MarkItDown | MIT |

None are AGPL/GPL — safe to vendor and ship behind the keyless drivers. (OCRmyPDF, if ever added, is MPL-2.0 / permissive; python-pptx is MIT.)
