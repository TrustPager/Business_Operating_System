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

If it isn't installed (or a per-format reader like the Word/PDF/Excel extra is missing), the wrapper prints the machine-readable `BOS_MISSING_DEP: <spec>` signal (e.g. `markitdown[docx]`) and exits non-zero. You do NOT relay a command to the owner; you run the **detect, offer, install-on-yes, verify** loop below. It is a one-time setup, like the rest of BOS, and the BOS does it for them.

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
The write counterpart. Where MarkItDown reads, doc-lib-set produces a real file an owner can open and send. Four thin wrappers, each mirroring the MarkItDown wrapper exactly: an argparse CLI, an `INSTALL_HINT` that emits `BOS_MISSING_DEP: <spec>` + a `python -m pip install <spec>` recommendation and **exits non-zero (2)** when the lib is missing, **exit 1** on a real error, clean stdout/stderr, no network at runtime.

| Wrapper | Library | What it does |
|---|---|---|
| `tools/write_xlsx.py` | **openpyxl** | Write a real `.xlsx` from JSON rows (optional bold header, sheet title). |
| `tools/write_docx.py` | **python-docx** | Write a real `.docx` from JSON blocks (heading / paragraph / bullet / table). |
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

#### `write_docx.py` block types (including the priced-line-item `table`)
`write_docx.py` renders an ordered list of blocks. Each block is an object keyed by `type`:

| Block | Shape | Renders |
|---|---|---|
| `heading` | `{"type":"heading","text":"...","level":1}` | A heading (`level` 0-9, default 1). |
| `paragraph` | `{"type":"paragraph","text":"..."}` | A body paragraph. |
| `bullet` | `{"type":"bullet","text":"..."}` | A bulleted list item. |
| `table` | `{"type":"table","header":[...],"rows":[[...],...]}` | A real Word table (Table Grid). |

The **`table`** block is how a quote or proposal lays out priced line items as a real grid, not bullets with `$____`. `header` is an optional list of column labels (rendered **bold** as the first row); `rows` is a list of rows, each a list of cell values. Every cell is coerced to a string, so numbers and money strings (`"$120"`) both work. The column count comes from the header when present, else from the widest row; short rows are padded and over-long rows truncated, so a slightly ragged payload still produces a valid table. A `table` block with neither a header nor any rows is an error (exit 1).

```bash
python tools/write_docx.py --out quote.docx --blocks '[
  {"type":"heading","text":"Your investment","level":2},
  {"type":"table",
   "header":["Item","Qty","Price"],
   "rows":[["Site visit","1","$120"],["Labour","2","$180"],["Total","","$300"]]}
]'
```

Use the `table` block (not bullets) wherever a proposal or quote shows a priced breakdown, or wherever a tender section shows a deliverables / criteria grid.

### Read vs write — don't conflate
- **Read** a document → `tools/markitdown_convert.py` (Markdown) or `tools/pdf_tables.py` (precise PDF grid).
- **Write / generate** a document → `tools/write_xlsx.py` / `tools/write_docx.py` / `tools/make_pdf.py`.
- **Fill an existing PDF form** is still the READ-then-write path under `/update-pdf` (read the blank form with MarkItDown so Claude understands the fields, then write). `make_pdf.py` generates a *fresh* PDF from data — it does not fill an existing form's fields.

### The install-once story
Like MarkItDown, the doc libs are vendored tool dependencies, **not** kernel dependencies. The kernel stays pure stdlib and vendor-neutral; these libs live only behind `tools/` wrappers. They are **bundled at setup** (`python tools/setup.py` installs them, and they are declared in the repo-root `requirements.txt`), so a normal install has the full document floor with zero manual steps. If anything is ever missing, the BOS heals it for the owner, never the other way round.

```bash
# The manual fallback the owner almost never needs (always `python -m pip`, never bare `pip`):
python -m pip install -r requirements.txt
```

If a lib isn't installed, the wrapper prints `BOS_MISSING_DEP: <spec>` + a `python -m pip install <spec>` recommendation and exits non-zero, the same graceful path MarkItDown uses. The assistant turns that signal into the offer loop below; it never hands the owner the command. One-time setup, then offline forever.

### D11: the detect, offer, install-on-yes, verify loop (NEVER hand the owner a command)
This is the brain-dead self-sufficiency contract ([founder decision D11](../docs/architecture/founder-decisions.md)). When ANY doc tool prints a `BOS_MISSING_DEP: <spec>` line and exits non-zero, the assistant (not the owner) closes the gap:

1. **Detect.** A tool exited non-zero and stderr carries `BOS_MISSING_DEP: <spec>`. Read the `<spec>` (e.g. `markitdown[docx]`, `python-docx`, `openpyxl`, `reportlab`, `pdfplumber`).
2. **Offer, in plain language.** Say: *"To do this I need to add the document reader. It's a quick, free, one-time setup on your machine. Want me to go ahead?"* Name the capability in plain words ("document reader", "spreadsheet writer"), never the package name or a command.
3. **Do it on yes, yourself.** On a yes, run the install with the SAME interpreter: `python -m pip install <spec>` (equivalently `sys.executable -m pip install <spec>`). Never `pip install` bare (it can land in the wrong Python on a multi-Python machine, the exact openpyxl mismatch the field test hit). Never paste the command for the owner to run.
4. **Verify, then continue.** Re-run the tool (or `python tools/check-install.py`) to confirm it now works, then finish the original job as if nothing happened.

The whole floor can be healed in one shot with `python tools/check-install.py --fix`, which installs every missing document dependency the same way (same interpreter) and re-runs the write/read round-trip. `start-here`'s first doc-tool use may offer to run `--fix` with permission as the one-time setup beat. The plain-language owner-facing version of all this is in [knowledge/setup-and-dependencies.md](setup-and-dependencies.md).

**Any skill that uses a doc tool inherits this loop.** If a tool exits non-zero with `BOS_MISSING_DEP`, run the offer loop, then retry. Do not surface the raw signal or a command to the owner.

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
