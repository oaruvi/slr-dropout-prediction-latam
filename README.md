# Machine learning for student dropout prediction in Latin American higher education: data and materials of a systematic review

This repository contains the search strategies, selection records, coded dataset and analysis scripts of the systematic review:

> Ruiz-Vivanco, O.; González-Eras, A.; Sierra, B. Machine Learning for Student Dropout Prediction in Latin American Higher Education: A Systematic Review of Data, Models, Evaluation, and Reporting Practices. *Applied Sciences* (submitted).

- **Protocol registration (OSF Registries):** https://doi.org/10.17605/OSF.IO/UN5JS
- **Archived release (Zenodo):** `[DOI to be added after the first release]`
- **Article:** `[DOI to be added on publication]`

The review followed PRISMA 2020. Scopus, Web of Science, IEEE Xplore and the ACM Digital Library were searched on 15 March 2026 for studies published from 2020 onwards; 74 studies were included.

## Contents

```text
├── 01_Protocol/
│   ├── eligibility_criteria.csv            Inclusion (I1–I5) and exclusion (E1–E6) criteria
│   ├── screening_instructions.pdf          Instructions and exclusion codes used in screening
│   ├── extraction_instructions.pdf         Extraction instructions and full data dictionary
│   └── PRISMA_2020_checklist_and_sensitivity.pdf   PRISMA 2020 checklist and sensitivity tables
├── 02_Search_Strategies/                   Search string, fields, date and yield for each database
├── 03_Study_Selection/
│   ├── prisma_flow.csv                     Numbers at each stage of the flow diagram
│   ├── initial_records.csv                 Records identified (n = 1,095)
│   ├── duplicates.csv                      Duplicate records removed (n = 214)
│   ├── title_abstract_screening.csv        Records screened on title and abstract (n = 881)
│   ├── full_text_screening.csv             Reports assessed for eligibility (n = 317)
│   └── excluded_reports.csv                Reports excluded at full text, with reasons (n = 243)
├── 04_Coded_Dataset/
│   ├── coded_dataset.csv                   One row per included study (n = 74)
│   ├── data_dictionary.csv                 Definition and observed values of every column
│   └── included_studies.bib                References of the included studies (key = Study ID)
└── 05_Analysis/
    ├── reproduce_results.py                Recomputes all reported frequencies
    ├── make_figures.py                     Draws Figures 1–3
    ├── outputs/                            Tables produced by the scripts
    ├── figures/                            Figures produced by the scripts (PNG, 600 dpi)
    └── keyword_screening/                  Term lists and script of the keyword-assisted coding
```

## Reproducing the results

`reproduce_results.py` needs only Python 3.9 or later. `make_figures.py` also needs the packages in `requirements.txt`.

```bash
pip install -r requirements.txt
python 05_Analysis/reproduce_results.py
python 05_Analysis/make_figures.py
```

| Output | Content | In the article |
|---|---|---|
| `outputs/frequencies.csv` | Number and percentage of studies in every category of every coded variable | Sections 3.1–3.8, Tables 4–8 |
| `outputs/by_period.csv` | Indicators for 2020–2022 and 2023–2026 | Figure 3 and comparisons by period |
| `outputs/sensitivity_recomputed.csv` | Indicators for the main analysis and sensitivity analyses S1–S3 | Section 3.9, Table S4 |
| `figures/fig1_prisma.png` | PRISMA 2020 flow diagram | Figure 1 |
| `figures/fig2_year_country.png` | Studies by year and by country of the dataset | Figure 2 |
| `figures/fig3_practices_period.png` | Reporting practices by period | Figure 3 |

## The coded dataset

Each row of `coded_dataset.csv` is one included study, identified by a Study ID such as `ART13_SCP` (the suffix gives the database of origin). The same ID is the BibTeX key in `included_studies.bib`. The columns cover the data source, best-performing model, metrics, validation, calibration, class-imbalance treatment, explanation methods, fairness, deployment, and governance and reproducibility reporting. `data_dictionary.csv` defines each column and maps it to the entities of the registered protocol.

Three points matter when reusing the data:

1. **The codes describe what the studies report.** "None reported" or "Not reported" means the article does not describe the practice, not that the practice was absent.
2. **Not every column was verified to the same standard.** The column `verified_against_full_text` of the data dictionary marks the columns that were checked against the full texts by a second reviewer. Sample size (with its unit) and the leading predictor dimension were verified against the full texts by the first author; publication type, year and title come from the verified bibliographic records.
3. **Country refers to the dataset**, not to the authors' affiliation.

## Study selection files

The files in `03_Study_Selection/` hold the bibliographic fields of the records at each stage (title, authors, venue, year, database, document type, DOI) as exported from the databases. Abstracts, keywords and affiliations were removed.

`excluded_reports.csv` lists the 243 reports excluded after full-text assessment: 161 at full-text screening and 82 in an eligibility audit carried out during data extraction (column `Stage`). The 495 records excluded on title and abstract and the 69 reports that could not be retrieved are not listed in a separate file; together they are the records of `title_abstract_screening.csv` that do not appear in `full_text_screening.csv`.

## Keyword-assisted coding

Reporting practices were coded with the help of keyword searches of the full texts. `keyword_screening/keyword_terms.json` contains the term lists (regular expressions in English, Spanish and Portuguese) of the three passes, and `keyword_flags.py` applies them to a folder of plain-text files. A match only located a candidate passage; every code was assigned by a reviewer after reading the passage and verified by a second reviewer.

The full texts are not distributed, for copyright reasons. `outputs/keyword_match_counts.csv` gives the number of matches of each term list in each included study. `outputs/keyword_indicators_broader_criterion.csv` holds the comparison reported in place of the fourth registered sensitivity analysis; it counts mentions in the text, not verified practices. The regular expressions and minimum number of matches of each indicator are in `keyword_screening/indicator_definitions.json`; the broader corpus is the 74 included studies plus the 38 excluded reports whose target was academic risk or performance.

## Deviations from the registered protocol

- The registration reports 99 included studies. Verification of the extracted data against the full texts, a final check of the educational level and prediction target of each study, and a last review of the eligibility of the included reports left 74. Twenty-seven reports were removed and two restored (net change of 25); all removed reports are listed in `03_Study_Selection/excluded_reports.csv` with the stage "Eligibility audit". The main reasons were datasets from outside Latin America, a target other than dropout, no performance metrics, and samples that were not undergraduate cohorts (graduate, secondary-level or non-degree students).
- The registered criteria name journal articles and full-length conference papers. One peer-reviewed book chapter (ART64_SCP) that met all other criteria was retained; this is a deviation from the registered wording, and sensitivity analysis S2 excludes it. Studies whose only Latin American data served to validate externally a model trained on data from another region were excluded (ART56_SCP).
- The fourth registered sensitivity analysis (broader reading of the prediction-target criterion) could not be carried out with verified codes and was replaced by a comparison of automated keyword indicators.

## Licenses

- Code (`*.py`): MIT License, see `LICENSE`.
- Data and documents (CSV, JSON, PDF, TXT): Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/. Bibliographic records originate from Scopus, Web of Science, IEEE Xplore and the ACM Digital Library.

## How to cite

Please cite the article and, for the data, the archived release (see `CITATION.cff`).

## Funding and contact

This work was supported by Universidad Técnica Particular de Loja (UTPL), Ecuador. Questions can be sent through the issue tracker of this repository or to the corresponding author named in the article.
