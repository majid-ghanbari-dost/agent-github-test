# Current Handoff — Holoo H-2
Date: 2026-11-11
Repository: majid-ghanbari-dost/agent-github-test
User role: Product Owner; execution delegated.
Mission status: H2-1 through H2-6 completed with evidence package; remaining uncertainties are explicitly listed below.

## Safety boundary
- Only isolated database `HolooAnalysis` restored inside GitHub Actions.
- No live-shop connection.
- No modification of the original backup.
- No writes to Kandoo repositories.
- SQL Server container removed after each successful run.

## Latest successful extraction
- Run ID: 42975548964 (run number 17)
- Commit: `e4156c41ea176e50f58ae9e8b664092483b2ad16`
- Job ID: 130373678954; conclusion success.
- Artifact ID: 13835013322; name `holoo-restored-database-inventory`
- Artifact SHA-256: `75003c45e8bb687ed3eb9c3eb96f19a176ed3b8aa820fad346b8fe28c243ff51`
- 47 raw files; both CORE and H2 success markers present.
- Workflow: `.github/workflows/holoo-restore-inventory.yml`
- Run URL: https://github.com/majid-ghanbari-dost/agent-github-test/actions/runs/42975548964

## Final findings
1. H2-1: Per-line integer rounding of qty*Price_BS matches FACTURE.Sum_Price in all 8,071 invoices. F and Y match even raw; K has 4 raw mismatches, X has 2, Z has 1; all resolved by per-line rounding.
2. H2-2: 4,202/4,202 active F invoices join to CUSTOMER. 152 distinct customer codes. Code 00001, named «مشتری», has 3,551 invoices and 164,847,179,800 (86.9164% of F sales). Other customers total 24,814,592,705 across 651 invoices; largest non-00001 customer is 4,664,910,000 (18.7991% of the other-customer subtotal).
3. H2-3: 1,819/1,820 ARTICLE stock rows reconcile. Sole mismatch A_Code 0101001, name سرویس, Model `#*Not_Article*#`, TypeArt 12; delta 9,000,000,000. The view W_ShowArticleForSearch_Big sets Is_Khadamat=1 for this marker; Sp_CreateTempArtPrice excludes it from normal stock/price calculations; ConvertDataForFreeSarfasl and sp_ShowFacTitr treat it specially. Classification as service/non-stock is supported; reason for sentinel stock values remains unknown.
4. H2-4: `Sum_Price = FNaghd + FCheck + FNesieh + Card + Takhfif` holds exactly for all 8,066 F/K/X/Y invoices. Z is separate. sp_ShowFacTitr exposes payment fields and computes discount percentage from Takhfif/Sum_Price. FCheck and Card are all zero in this backup; do not infer universal feature absence. Exact operational semantics of every payment field remain partially unproven.
5. H2-5: 335 month/type groups over 102 Gregorian months, 2015-12 to 2024-05. Totals: F 189,661,772,505; K 157,236,982,810; X 943,344,154; Y 6,536,461,000; Z 21,751,003. F-Y = 183,125,311,505; do not label this profit or cash collection. 2024 is partial through May.
6. EndBuy_PriceK: 1,953 nonzero sales rows; 1,949 had prior purchases; 1,831 matched last prior purchase-day weighted cost, 190 all-time weighted average, 642 current ARTICLE.Buy_Price. These are correlations, not proven field semantics; no direct stored-module reference found.

## Package deliverable
- Independent ZIP: `HOLOO-H2-FINAL-2026-11-11.zip`
- SHA-256: `b5a7544603ce8649f5ca3618d4889ffe6dbcd2359157c194ead2e2ccfc9c20b8`
- 47 raw evidence files, Persian report, methodology/query source, evidence index, provenance and SHA-256 manifest.
- GitHub report: `reports/H2_FINAL_REPORT_FA_2026-11-11.md`
- Early checkpoint: `handoff/HANDOFF-HOLOO-H2-2026-11-11-EARLY.md`
- Package artifact: https://github.com/majid-ghanbari-dost/agent-github-test/actions/runs/42975548964/artifacts/13835013322

## Remaining uncertainties (not blockers to H-2 completion)
- Why service item 0101001 has First_Exist=10bn and Exist=1bn.
- Definitive semantics of FNaghd/FCheck/FNesieh/Card across all app workflows.
- Definitive app-side meaning of EndBuy_PriceK.
- Currency denomination (rial/toman) not inferred.

## Resume instructions
If continuing beyond H-2, do not rerun or modify completed extraction unless a specific question requires it. Start with a technical review of the remaining uncertainties and identify whether app-side executable/source or additional isolated query evidence is available. Keep uncertainty labels. No product decision is currently required.
