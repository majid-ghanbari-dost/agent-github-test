# H-2 Preliminary Verified Findings
Date: 2026-11-11
Source artifact: workflow run 42973595886, artifact 13833798895
Artifact SHA-256: 3b29c4725fa6d688348af63bf55802ccd9f50aa9c90fc16a51e95f07a6b84865

> This is a preliminary evidence note, not the final H-2 package. The workflow run's extraction job concluded FAILURE after successful restore and partial extraction. The artifact upload succeeded because it is configured with `if: always()`.

## H2-1 — Invoice row-price reconciliation (verified from complete 8,071-row export)
The export contains 8,071 invoice headers and the following per-type outcomes:

| Type | Invoice count | Raw line sum exact | Per-line rounded sum exact |
|---|---:|---:|---:|
| F (sales) | 4,202 | 4,202 | 4,202 |
| K (purchase) | 3,343 | 3,339 | 3,343 |
| X (purchase return) | 41 | 39 | 41 |
| Y (sales return) | 480 | 480 | 480 |
| Z (waste) | 5 | 4 | 5 |
| **Total** | **8,071** | **8,064** | **8,071** |

Rule proven against this backup:
`FACTURE.Sum_Price = SUM(ROUND(FACTART.Few_Article * FACTART.Price_BS, 0))` grouped by `Fac_Code, Fac_Type`.
This is a per-line rounding rule, not rounding only the final invoice aggregate. Four K, two X, and one Z invoices differ under raw multiplication; all reconcile under per-line integer rounding. Sales invoices F already reconcile without rounding.

## H2-3 — Stock anomaly (verified; cause unresolved)
The stock reconstruction report showed 1,819 of 1,820 ARTICLE rows matching. One row differs:
- A_Code: `0101001`
- A_Name: `سرويس`
- Model: `#*Not_Article*#`
- TypeArt: `12`
- First_Exist / First_Exist2: 10,000,000,000
- Exist / Exist2: 1,000,000,000
- Calculated movement in the tested reconstruction: 0 in, 0 out
- Difference: 9,000,000,000

This supports classifying the row as a likely non-stock/service record for investigation, but does not prove why the two stored quantities differ. Do not silently normalize or discard it.

## Cost-field finding (cross-cutting, not a final H2 acceptance item)
For 1,953 sales rows with nonzero `FACTART.EndBuy_PriceK`:
- 1,949 had a prior purchase record.
- 1,831 matched the weighted average of purchases on the latest prior purchase date.
- 190 matched the all-time weighted purchase average.
- 642 matched the current `ARTICLE.Buy_Price`.

This is strong evidence of a historical purchase-cost snapshot relationship, but not a definitive definition. The field was not referenced in the extracted SQL module definitions; application-side assignment remains possible.

## Still pending
H2-2 customer top-ten ranking and contribution; H2-4 payment field meaning and reconciliation; H2-5 monthly time series; H2-6 Persian final report, complete evidence package, archive and SHA-256 manifest. A corrected workflow adds these extracts, but no completion claim is valid until a successful new Actions run and artifact are inspected.
