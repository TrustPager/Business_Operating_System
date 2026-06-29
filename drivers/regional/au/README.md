# AU Regional Constants

This directory holds versioned, authoritative Australian tax and wage constants
for the BOS money pack. The file name encodes the financial year the figures
are valid for (e.g. `constants-FY2026-27.json`).

The loader at `tools/regional.py` (function `load_au_constants`) reads the
most recent file in this directory and refuses to load it for any region
other than "AU".

---

## Provenance table

Every figure stored in `constants-FY2026-27.json` is listed here with its
official source URL, the date it became effective, and the date we retrieved it.

| Figure | Value | Effective from | Source URL | Retrieved |
|--------|-------|----------------|------------|-----------|
| GST rate | 10% | 2000-07-01 | https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/how-gst-works | 2026-06-28 |
| GST registration threshold (standard) | $75,000 | 2012-07-01 | https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/how-gst-works | 2026-06-28 |
| BAS field G1 (total sales) | Label + method | 2017-07-01 | https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/reporting-and-paying-gst/completing-your-bas/how-to-complete-the-simpler-bas | 2026-06-28 |
| BAS field 1A (GST on sales) | Label + method | 2017-07-01 | https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/reporting-and-paying-gst/completing-your-bas/how-to-complete-the-simpler-bas | 2026-06-28 |
| BAS field 1B (GST on purchases) | Label + method | 2017-07-01 | https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/reporting-and-paying-gst/completing-your-bas/how-to-complete-the-simpler-bas | 2026-06-28 |
| Super guarantee rate | 12% | 2026-07-01 | https://www.ato.gov.au/tax-rates-and-codes/key-superannuation-rates-and-thresholds/super-guarantee | 2026-06-28 |
| Super max contribution base (annual) | $270,830 | 2026-07-01 | https://www.ato.gov.au/tax-rates-and-codes/key-superannuation-rates-and-thresholds/super-guarantee | 2026-06-28 |
| Super concessional contributions cap | $32,500 | 2026-07-01 | https://www.ato.gov.au/tax-rates-and-codes/key-superannuation-rates-and-thresholds/contributions-caps | 2026-06-28 |
| Resident income tax brackets | 5-band table (see notes) | 2024-07-01 | https://www.ato.gov.au/tax-rates-and-codes/tax-rates-australian-residents | 2026-06-28 |
| Tax-free threshold | $18,200 | 2012-07-01 | https://www.ato.gov.au/tax-rates-and-codes/tax-rates-australian-residents | 2026-06-28 |
| Medicare levy rate | 2% | 2014-07-01 | https://www.ato.gov.au/individuals-and-families/medicare-and-private-health-insurance/medicare-levy/what-is-the-medicare-levy | 2026-06-28 |
| FBT rate | 47% | 2022-04-01 (to 2027-03-31) | https://www.ato.gov.au/tax-rates-and-codes/fringe-benefits-tax-rates-and-thresholds | 2026-06-28 |
| FBT Type 1 gross-up rate | 2.0802 | 2022-04-01 (to 2027-03-31) | https://www.ato.gov.au/tax-rates-and-codes/fringe-benefits-tax-rates-and-thresholds | 2026-06-28 |
| FBT Type 2 gross-up rate | 1.8868 | 2022-04-01 (to 2027-03-31) | https://www.ato.gov.au/tax-rates-and-codes/fringe-benefits-tax-rates-and-thresholds | 2026-06-28 |
| National Minimum Wage (hourly) | $26.44 | 2026-07-01 | https://www.fairwork.gov.au/about-us/workplace-laws/annual-wage-review/annual-wage-review-2026 | 2026-06-28 |
| National Minimum Wage (weekly) | $1,004.90 | 2026-07-01 | https://www.fairwork.gov.au/about-us/workplace-laws/annual-wage-review/annual-wage-review-2026 | 2026-06-28 |
| Casual loading (NES minimum) | 25% | 2021-03-27 | https://www.fairwork.gov.au/pay-and-wages/minimum-wages | 2026-06-28 |

---

## Notes on specific figures

### Income tax brackets (FY2026-27)

The ATO resident tax rates page (last updated 1 June 2026) explicitly labels
the most recent table as "Resident tax rates 2025-26". Separate FY2026-27
brackets had not been published as at 2026-06-28 (the day before FY2026-27
begins). The same five-band structure applied for both FY2024-25 and FY2025-26.

The file stores these brackets under `effective_from: "2024-07-01"` and
includes a `_note` field explaining the gap. When the ATO publishes the
FY2026-27 brackets (typically around 1 July or shortly after), update the
`effective_from` date and create a new versioned file if the brackets change.

### Casual loading (25%)

The 25% minimum casual loading is set by the Fair Work Act 2009 (National
Employment Standards). The Fair Work Ombudsman website was reorganized in
mid-2026 and many former direct URLs now return 404. The figure is referenced
on the minimum wages hub page and is statutory (not subject to annual review
in the same way as the minimum wage). Individual awards may specify a higher
or lower casual loading rate, but 25% is the NES floor for award/agreement-free
casuals.

Source: Fair Work Act 2009 s.96; fairwork.gov.au/pay-and-wages/minimum-wages

### GST BAS field map (Simpler BAS)

The Simpler BAS reporting method was introduced 1 July 2017 for businesses
with annual turnover under $10 million. Under Simpler BAS, businesses only
need to report G1, 1A, and 1B (plus W1/W2 for PAYG withholding if applicable).
Larger businesses use the full BAS with additional label codes. The field map
stored here covers the Simpler BAS labels only.

---

## Deliberate scope narrowing

Two data types were intentionally excluded from this constants file:

1. **Per-award pay rates (122 modern awards)**: These change annually, vary by
   classification and industry, and are best served through the Fair Work
   Commission API or the FWO Pay and Conditions Tool. Embedding them here would
   require a large, volatile dataset. This is flagged as a future
   connected-tier deepener.

2. **PAYG withholding schedules**: The ATO publishes tax withheld schedules
   (NAT 1008, NAT 3539, etc.) as large tables that vary by earnings period,
   claim type, and resident status. These are too large and too volatile to
   bundle as static constants. The ATO tax withheld calculator at
   https://www.ato.gov.au/calculators-and-tools/tax-withheld-calculator
   should be referenced instead.

---

## How to refresh this file each financial year

1. **Trigger**: Beginning of each Australian financial year (1 July) or when
   a mid-year ATO announcement updates a figure.

2. **Create a new file**: Copy `constants-FY<current>.json` to
   `constants-FY<new>.json`. Never edit a previous year's file.

3. **Update each figure** by re-scraping the source URLs listed in the
   provenance table above. For each value:
   - Confirm the figure on the official page.
   - Update `value` and `effective_from` if changed.
   - Update `retrieved_on` to today's date in ISO format (YYYY-MM-DD).
   - Update `source_url` if the page has moved (the ATO reorganizes URLs
     periodically).

4. **Check for FY2026-27 income tax brackets**: The ATO sometimes publishes
   new brackets before or shortly after 1 July. Check
   https://www.ato.gov.au/tax-rates-and-codes/tax-rates-australian-residents

5. **Run tests**: `BOS_OFFLINE=1 python -m unittest tests.test_regional_au -v`
   All 14 tests must pass.

6. **Run all gates**:
   - `python tools/check-no-secrets.py`
   - `python tools/check-onboarding-binding.py`
   - `python tools/registry-generator.py --check`

7. **Commit**: Use the pattern
   `feat(p5): refresh AU constants FY<new> (sources updated YYYY-MM-DD)`

**Key source pages to check each year:**

| Figure | URL |
|--------|-----|
| Super guarantee rate | https://www.ato.gov.au/tax-rates-and-codes/key-superannuation-rates-and-thresholds/super-guarantee |
| Super caps | https://www.ato.gov.au/tax-rates-and-codes/key-superannuation-rates-and-thresholds/contributions-caps |
| Income tax brackets | https://www.ato.gov.au/tax-rates-and-codes/tax-rates-australian-residents |
| Medicare levy | https://www.ato.gov.au/individuals-and-families/medicare-and-private-health-insurance/medicare-levy/what-is-the-medicare-levy |
| FBT rates | https://www.ato.gov.au/tax-rates-and-codes/fringe-benefits-tax-rates-and-thresholds |
| National Minimum Wage | https://www.fairwork.gov.au/pay-and-wages/minimum-wages |
| Annual Wage Review | https://www.fairwork.gov.au/about-us/workplace-laws/annual-wage-review/ |
