# EARLY HANDOFF — Holoo H-2 execution checkpoint
Date: 2026-11-11
Repository: majid-ghanbari-dost/agent-github-test
Default branch: main
Purpose: durable checkpoint created early, before continuing deeper analysis.

## Mission and non-negotiable safety boundary
Continue H2-1 through H2-6. The user is Product Owner and has delegated execution; do not ask for routine approval. Use only the isolated backup restored by GitHub Actions as dbo database `HolooAnalysis`. Never connect to a live shop, never modify the original backup, and never modify Kandoo repositories. Keep all claims evidence-backed. Before any session limit, create/update a handoff in this folder.

## Verified latest successful Holoo workflow execution
- Workflow: `.github/workflows/holoo-restore-inventory.yml`
- Successful Holoo run ID: **42974695068** (workflow run number 16; event push)
- Commit SHA: `1532c4a2692251720beb71a4793b42eaabee08fe`
- Job: `restore-and-inventory`, job ID `130370920891`, conclusion **success**
- All relevant steps succeeded: archive extraction, isolated SQL Server 2022 start, RESTORE VERIFYONLY + restore, DBCC CHECKDB, inventory, core/H2 SQL extraction, artifact upload, container destruction.
- Artifact: `holoo-restored-database-inventory`, artifact ID **13835180883**
- Artifact SHA-256 (GitHub ZIP digest): `0561f0bfe23d4857216f8837c19328043c16abc785c3a9fdc46ac9b20d66fb76`
- Artifact download URL: https://github.com/majid-ghanbari-dost/agent-github-test/actions/runs/42974695068/artifacts/13835180883
- A separate run ID 42974722230 is a Python unit-test workflow (job named `test`) and has no artifacts; do not mistake it for the Holoo extraction run.
- Downloaded and locally inspected artifact: `/mnt/data/holoo-h2-run-42974695068.zip`; extracted to `/mnt/data/holoo_h2_run/` in the current runtime. Those paths may not persist in another session; re-download artifact by ID if needed.

## Important execution verification
The artifact contains 43 files, including:
- `CORE_EXTRACTION_SUCCESS.txt`
- `H2_EXTRACTION_SUCCESS.txt`
- `H2_1_invoice_price_reconciliation.txt`
- `H2_2_top10_customers.txt`
- `H2_2_customer_join_quality.txt`
- `H2_3_stock_anomalies.txt`
- `H2_4_payment_field_analysis.txt`
- `H2_4_payment_samples.txt`
- `H2_4_payment_modules.txt`
- `H2_5_monthly_invoice_stats.txt`
- plus core inventory, relationships, modules, stock and EndBuy evidence.
The successful workflow log explicitly shows all extraction commands executed and both success markers written. It uploaded 43 files; the artifact upload itself succeeded; SQL Server container was destroyed in cleanup.

## Verified H2 results from artifact

### H2-1 — invoice totals and line rounding
By invoice type:
| Fac_Type | Invoices | Raw exact | Exact after per-line ROUND(qty*price,0) | Max raw delta | Max rounded delta |
| F | 4202 | 4202 | 4202 | 0 | 0 |
| K | 3343 | 3339 | 3343 | 0.6660000011 | 0 |
| X | 41 | 39 | 41 | 0.464 | 0 |
| Y | 480 | 480 | 480 | 0 | 0 |
| Z | 5 | 4 | 5 | 0.16 | 0 |
Total 8,071 invoices. Per-line integer rounding reconciles all invoice types and all 8,071 totals. F sales and Y returns reconcile even without rounding. This is strong evidence of the stored total calculation rule, not proof of every UI setting. `rounding_settings.txt` returned no matching rows for the four guessed setting names.

### H2-2 — customer concentration and join quality
- 4,202 non-deleted F invoices checked.
- Customer code absent: 0; code not found in CUSTOMER: 0; matched: 4,202.
- Top customer code 00001, label «مشتري»: 3,551 invoices; 164,847,179,800; share 86.9164%.
- Share denominator is total sales amount for all non-deleted F invoices with nonblank C_Code (all 4,202 qualify).
- This concentration is real in the extracted data but the generic customer label «مشتري» may aggregate walk-in/anonymous customers; do not interpret it as one named individual without further evidence.

### H2-3 — stock anomalies
- Full movement reconstruction from earlier extraction matches 1,819 of 1,820 ARTICLE rows; one mismatch.
- Mismatch A_Code 0101001 «سرويس», Model `#*Not_Article*#`, TypeArt 12.
- First_Exist and First_Exist2 = 10,000,000,000; Exist and Exist2 = 1,000,000,000; movement InQty=0 and OutQty=0; delta = 9,000,000,000.
- Article created 2015-11-23; Buy_Price and EndBuy_Price are 0; ArtForKiosk=1.
- Do not claim cause proven. Non-article/service classification is a plausible explanation but needs corroborating procedure/app logic.
- H2_3 query flags opening/current quantity gaps >=1,000,000; its result contains this one row. Explain threshold in final report.

### H2-4 — payment columns
Totals in raw report:
| Type | InvoiceCount | Sum_Price | FNaghd | FCheck | FNesieh | Card | Takhfif | ComponentsEqualSumPrice | Differ |
| F | 4202 | 189,661,772,505 | 175,016,360,500 | 0 | 13,255,063,900 | 0 | 1,390,348,105 | 3016 | 1186 |
| K | 3343 | 157,236,982,810 | 126,827,332,541 | 0 | 30,393,090,905 | 0 | 16,559,364 | 3327 | 16 |
| X | 41 | 943,344,154 | 533,181,954 | 0 | 409,862,200 | 0 | 300,000 | 40 | 1 |
| Y | 480 | 6,536,461,000 | 6,007,457,500 | 0 | 501,200,000 | 0 | 27,803,500 | 379 | 101 |
| Z | 5 | 21,751,003 | 0 | 0 | 0 | 0 | 0 | 0 | 5 |
- `H2_4_payment_modules.txt` includes `sp_CreateTempFacture_FactArt` defining FNaghd, card, FCheck, FNesieh, Takhfif as separate FACTURE-like fields; `sp_ShowFacTitr` selects F.FNaghd, F.FCheck, F.FNesieh, F.card, F.Takhfif, and calculates discount percentage as Takhfif*100/Sum_Price. This establishes application-level exposure and Takhfif-as-discount treatment in that procedure, but does not yet prove exact operational semantics of payment columns.
- FCheck and Card aggregate to zero and have zero nonzero rows in the report. Do not infer that the business never accepted checks/cards; possible legacy, alternate workflow, or data-model limitations.
- Component comparison currently tests FNaghd+FCheck+FNesieh+Card against Sum_Price; Takhfif is reported separately. Do not call it a final settlement equation until checking source procedures and samples. Analyze outliers, signs, returns, and whether Takhfif is included/excluded.

### H2-5 — monthly trends
- 335 grouped rows across 102 distinct Gregorian year-months, from 2015-12 through 2024-05.
- Types kept separate; query excludes rows with Delete=1.
- Aggregate totals across monthly rows:
  - F: 4,202 invoices; 189,661,772,505 amount; 31,454 quantity.
  - K: 3,343; 157,236,982,810; 29,897.
  - X: 41; 943,344,154; 204.
  - Y: 480; 6,536,461,000; 700.
  - Z: 5; 21,751,003; 15.
- Peak F monthly amount: 2023-12, 49 invoices, 8,203,800,000.
- Peak K monthly amount: 2024-02, 41 invoices, 6,565,020,550.
- Do not equate invoice amounts with net revenue or cash collected. If deriving net sales, define gross F minus sales return Y and state whether deleted rows are excluded. Consider also X separately.

## Core database context
- HolooAnalysis ONLINE, compatibility level 100, collation Arabic_CI_AS, recovery SIMPLE.
- 330 tables, 25 views, 209 stored procedures. Prior inventory also reported 26 functions.
- DBCC CHECKDB output file is zero bytes; the workflow command returned success. Earlier successful run evidence recorded no DBCC errors. In final report cite workflow success and note DBCC output empty/no reported diagnostics rather than fabricating output lines.
- Main row counts and joins remain as recorded in primary handoff.
- Invoice date span 2015-12-23 to 2024-05-12.
- Stored procedure ShowSanads maps F=sales, K=purchase, Y=sales return, X=purchase return, Z=waste.

## Next tasks — continue without waiting for user
1. Continue H2-4 forensic review: parse module names and SQL definitions in `H2_4_payment_modules.txt`, inspect exact writes/updates to payment fields and representative sample rows. Determine whether module definitions only expose fields or provide semantic evidence. Do not overclaim.
2. Audit H2-2: consider whether C_Code 00001 is an anonymous/aggregate customer and quantify concentration both including and excluding that code; if possible query further in a future isolated run.
3. Audit H2-3: check whether TypeArt=12 and Model marker #*Not_Article*# are handled specially by stored procedures/views; retain UNKNOWN unless direct evidence.
4. Audit H2-5: compute yearly/monthly net sales (F minus Y) as a separate derived metric only if clearly labelled; quantify active months and outliers, avoid mixing types.
5. Inspect `sales_cost_snapshot_validation.txt` and `sales_cost_snapshot_samples.txt`; validate prior EndBuy_PriceK correlations with correct FACTURE date alias. Keep correlation separate from field semantics.
6. Review query correctness: H2-2 top 10 includes all customer-coded active F invoices; H2-3 uses a hard threshold of 1,000,000; H2-4 payment sums compare components with Sum_Price but do not include Takhfif; H2-5 date grouping is Gregorian.
7. Create a Persian H2-6 final report, methodology, limitations, evidence index, source SQL, run/artifact provenance, manifest, and independent ZIP.
8. Generate SHA-256 for every packaged file and the ZIP. Re-download/re-verify artifact if needed. Do not overwrite raw evidence; package it unchanged.
9. Update the primary handoff and this checkpoint with final outputs and next mission before session limit.

## Existing primary handoff and findings
- `handoff/HANDOFF-HOLOO-H2-2026-11-11.md`
- `reports/H2_PRELIMINARY_VERIFIED_FINDINGS.md`

## Resume prompt
Continue Holoo H-2 from this early handoff. First retrieve artifact 13835180883 for run 42974695068 if local files are unavailable. Continue forensic validation H2-4, H2-2 concentration, H2-3 service-item handling, H2-5 trends, then produce H2-6 Persian ZIP + manifest + SHA-256. Preserve the read-only isolated-backup boundary. User is Product Owner and has delegated execution; only escalate a genuine product decision or missing access.
