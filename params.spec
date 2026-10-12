# variants|group|KEY|rule|description   (variants: all, or C for GGL-C-1.0 only)
all|Licensor|LICENSOR_NAME|text|Legal name of the licensor (company or person)
all|Licensor|LICENSOR_LOCATION|text|City and state or country of the licensor
all|Licensor|COPYRIGHT_YEAR|year|Year of first publication
all|Licensor|LICENSING_CONTACT|contact|Email or https URL for licensing requests
all|Inventor|INVENTOR_NAME|text|LOCKED. Original inventor's full legal name (Section I)
all|Inventor|INVENTOR_ORCID|orcid|LOCKED. Inventor's ORCID iD, form 0000-0000-0000-000X
all|Inventor|INVENTOR_RECORD_DOI|doi|LOCKED. DOI of the Zenodo Inventor Record
all|Program|PROGRAM_NAME|text|Name of the specification program
all|Program|SPEC_NUMBER_PREFIX|text|Prefix of specification numbers
all|Program|ATTRIBUTION_NAMES|text|Names that attribution must carry besides the inventor (S.3)
all|Program|MARKS|text|Names and marks reserved under G.4, comma separated
all|Covered Work|COVERED_WORK|text|Name and number of the work this copy covers
all|Covered Work|COVERED_WORK_VERSION|semver|Version of the covered work, x.y.z
all|Covered Work|SPEC_LICENSE|enum:CC BY 4.0,CC BY-ND 4.0,not applicable|Part S license for the text
all|Covered Work|OFFERED_LICENSES|offered|Family licenses this work is offered under, comma separated: GGL-OS-1.0, GGL-EGR-1.0, GGL-C-1.0
all|Covered Work|PATENT_SCHEDULE|text|Path or URL of the Patent Schedule (P.1)
all|Covered Work|PATENT_SCHEDULE_VERSION|int|Patent Schedule version number
C|Commercial: Startup Tier|SMALL_BIZ_MAX_WORKERS|int|Small business worker ceiling (C.4)
C|Commercial: Startup Tier|SMALL_BIZ_MAX_REVENUE_USD|money|Small business revenue ceiling in US dollars (C.4)
C|Commercial: Startup Tier|INFLATION_BASE_YEAR|year|Base year for CPI-U adjustment (C.4)
C|Commercial: Startup Tier|EVAL_DAYS|int|Free evaluation period in days (C.4)
C|Commercial: Fees|REVENUE_SHARE_PCT|pct|Give-back share of Gross Revenue, percent (C.5)
C|Commercial: Fees|FEE_PER_UOP_USD|money|Fee per Unit of Proof in US dollars (C.5)
C|Commercial: Fees|MIN_ANNUAL_FEE_USD|money|Minimum annual fee in US dollars (C.5)
C|Commercial: Fees|ANNUAL_CAP_USD|money|Annual fee cap in US dollars (C.5); must be at least the minimum fee
C|Commercial: Fees|RATES_URL|url|https URL where commercial rates are published (C.8)
all|Lineage|POOL_CAP_PCT|pct|Most of the fee all pool shares in one ancestry may take (E.7)
all|Lineage|LINEAGE_URL|text|Where the canonical lineage file lives (E.9)
C|Commercial: Terms|REPORT_DAYS|int|Days after fiscal year end to report and pay (C.7)
C|Commercial: Terms|AUDIT_UNDERPAY_PCT|pct|Underpayment that shifts audit cost to the licensee (C.7)
C|Commercial: Terms|FAIRNESS_DAYS|int|Days the Licensor has to offer published terms (C.8)
all|Terms|CURE_DAYS|int|Days to cure a violation (G.2)
all|Terms|LATE_INTEREST_PCT_MONTH|pct|Late interest, percent per month (G.3)
all|Law|GOVERNING_LAW|text|Governing law, e.g. Colorado (G.10)
all|Law|VENUE|text|Exclusive venue for disputes (G.10)
