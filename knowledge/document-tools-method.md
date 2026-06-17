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
