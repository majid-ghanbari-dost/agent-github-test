# Handoff — Holoo Backup Analysis / H-2
Date: 2026-11-11
Repository: majid-ghanbari-dost/agent-github-test
Default branch: main
Backup scope: isolated copy restored as SQL Server database `HolooAnalysis`
Safety boundary: read-only analysis only; never connect to the live shop; never modify the source backup or Kandoo repositories.

## Mission
Finish H2-1 through H2-6 using reproducible SQL outputs and a Persian final report. The user has delegated execution and may be absent; do not wait for user input unless a genuine product decision or missing credential is required.

## Verified baseline
Successful restore/inventory evidence is from workflow run 42973595886, artifact `holoo-restored-database-inventory` (artifact ID 13833798895; SHA-256 `3b29c4725fa6d688348af63bf55802ccd9f50aa9c90fc16a51e95f07a6b84865`).
- Database `HolooAnalysis` ONLINE; DBCC CHECKDB completed with no reported errors.
- 330 tables, 25 views, 209 stored procedures; prior inventory also recorded 26 functions.
- FACTURE 8,071; FACTART 35,641; ARTICLE 1,820; CUSTOMER 225; SANAD 8,740; SND_INDX 8,071; SND_LIST 33,748.
- Invoice types: F=4,202; K=3,343; Y=480; X=41; Z=5.
- Invoice dates: 2015-12-23 through 2024-05-12.
- Core joins previously validated: all 8,071 FACTURE rows link to SANAD; all 8,071 SND_INDX invoice links validated; all 33,748 SND_LIST rows link to SANAD.
- Main keys: FACTURE(Fac_Code,Fac_Type); FACTART(Fac_Code,Fac_Type,A_Code,A_Index); ARTICLE(A_Code); CUSTOMER(C_Code); SANAD(Sanad_Code); SND_INDX(Sanad_Code,Fac_Code,Fac_Type,Check_Code); SND_LIST(Sanad_Code,Index).
- No meaningful FK constraints across core tables; validate relationships through data and stored procedures.

## Important verified calculations
- `SUM(ROUND(Few_Article * Price_BS, 0))` per invoice exactly matches FACTURE.Sum_Price for all 8,071 invoices.
- Raw unrounded line multiplication matches all F (4,202) and Y (480); raw differences occur in 4 K, 2 X, and 1 Z invoices. Per-line rounding resolves all 8,071.
- Sum(Few_Article) matches FACTURE.Sum_Few for all 8,071 according to prior validated analysis.
- Stock reconstruction previously matched 1,819/1,820 ARTICLE rows. Sole mismatch: A_Code 0101001, name سرویس, Model `#*Not_Article*#`, TypeArt 12; First_Exist and First_Exist2 = 10,000,000,000; Exist and Exist2 = 1,000,000,000; calculated movements zero; delta 9,000,000,000. Do not label the cause as proven. Investigate whether non-stock/service classification explains it.
- FACTART.EndBuy_PriceK is nonzero on 1,953 F rows. It matches last prior purchase-day weighted cost on 1,831 rows, all-time weighted purchase average on 190, current ARTICLE.Buy_Price on 642. This is correlation, not proof of field semantics. No stored module reference to EndBuy_PriceK was found; inspect app-side possibility only if available.
- Stored procedure ShowSanads maps F=sales, K=purchase, Y=sales return, X=purchase return, Z=waste.

## Prior failed run diagnosis
Run 42973595886 restored and inventoried successfully but failed in final extraction. The final sample query selected `s.Fac_Date` from FACTART alias s; the date belongs to FACTURE alias f. This has been corrected to `f.Fac_Date`.
A second workflow authoring defect initially escaped the shell variable as `\${SQLCMD[@]}`; corrected in commit df6eb2634a57ffad3c610c26b740ae6bcc37794f. Verify the committed YAML before trusting the next run.

## Recent commits
- de01c32ec83cf3d15cdd7a5ada828e226f02bbe4 — fixed date alias and added H2 extraction SQL queries.
- df6eb2634a57ffad3c610c26b740ae6bcc37794f — corrected shell variable expansion.
Workflow: `.github/workflows/holoo-restore-inventory.yml`.
A push to this workflow path should trigger a new Actions run. The connector available in the prior session could fetch jobs/artifacts/logs for a known run ID but did not expose a general list-workflow-runs or workflow_dispatch action. If run ID cannot be discovered, inspect GitHub Actions UI or use a supported GitHub Actions listing/dispatch capability; do not claim a run completed without evidence.

## H2 deliverables and intended outputs
- H2-1 invoice line pricing: `H2_1_invoice_price_reconciliation.txt`; prove raw vs per-line rounded match by type. Explain that F sales are exact even raw; all invoice types match with per-line rounding.
- H2-2 customer analysis: `H2_2_top10_customers.txt`, `H2_2_customer_join_quality.txt`; top 10 F sales customers by Sum_Price, invoice counts, contribution share, customer name, join quality. State denominator used for share (customer-coded sales only).
- H2-3 stock anomalies: `H2_3_stock_anomalies.txt`; report every significant First_Exist/Exist or First_Exist2/Exist2 gap. Classify the service item carefully; unknown cause stays UNKNOWN.
- H2-4 payment analysis: `H2_4_payment_field_analysis.txt`, `H2_4_payment_samples.txt`; quantify FNaghd, FCheck, FNesieh, Card, Takhfif and compare candidate component sum to Sum_Price. Do not assign field semantics until corroborated by stored procedure/view definitions and samples.
- H2-5 monthly trends: `H2_5_monthly_invoice_stats.txt`; Gregorian monthly counts, amounts, quantities by Fac_Type. Keep sales and returns separate; optionally derive net sales as F minus Y with transparent definition.
- H2-6 package: create Persian executive summary, methodology, evidence index, limitations, SQL/query source, run/artifact IDs, SHA-256 manifest, and a ZIP deliverable.

## Next execution steps
1. Verify latest workflow YAML on main. Ensure every SQLCMD invocation uses `${SQLCMD[@]}` (without a literal backslash) and the EndBuy sample query uses `f.Fac_Date`.
2. Obtain the new workflow run ID and inspect job steps/logs.
3. Download the resulting artifact and verify it contains all H2_1–H2_5 files plus `CORE_EXTRACTION_SUCCESS.txt` and `H2_EXTRACTION_SUCCESS.txt`.
4. If any SQL fails, use the exact SQL error to fix the query; rerun. Do not mark the H2 item complete merely because the artifact uploaded (upload is configured with if: always()).
5. Analyze the outputs, cross-check totals and row counts, then create H2-6 Persian report and ZIP.
6. Include manifest and SHA-256. Keep raw report files unmodified; add interpreted summaries separately.
7. Final acceptance checklist: all H2 items have evidence; uncertainties explicitly labelled; no writes to source backup; no live-store access; no Kandoo repo modifications.

## Critical cautions
- The database uses collation Arabic_CI_AS and compatibility level 100 (SQL Server 2008-era behavior); avoid modern-only T-SQL constructs.
- SQL Server is restored inside a temporary GitHub Actions container and destroyed after the job. There is no persistent live DB session.
- Artifact upload happens even when the extraction step fails. Check job conclusion and success marker files.
- Do not claim exact meaning of EndBuy_PriceK, payment columns, or the 0101001 stock discrepancy without additional evidence.
