# Arbitration Clause Checker

Most jurisdictional challenges in international arbitration don't stem from complex legal
disputes; they trace back to flawed drafting. An inverted typo in an institution's name,
ambiguous "may" vs. "shall" language, or a single "or" can tie up a cross-border
transaction in years of jurisdictional fights.

This tool systematizes the pattern recognition required to catch these flaws before
execution. It deploys two separate, hardcoded rule engines: one mapped to major
international institutional rules (ICC, AAA, LCIA, SIAC) and the other to PRC
Arbitration Law and the 2006 Supreme Court Judicial Interpretation. A bilingual ML
classifier identifies initial language patterns; the rule engines then process the
jurisdiction-specific legal outcomes.

Keeping these logic streams isolated is a deliberate architectural choice. A "hybrid"
clause permitting both arbitration and litigation is treated as an ambiguous, often
salvageable defect under many common-law frameworks. Under Article 7 of the PRC
Judicial Interpretation, it is strictly invalid. Conflating the two produces false
confidence, not coverage.

## Background

I worked as an arbitration case secretary for three years before moving into data
science. A large share of the jurisdictional fights I administered started with a badly
drafted clause, not a hard legal question. This project turns that pattern recognition
into code.

## Why Two Separate Rule Engines

English-language checks are derived from transnational soft law, major institutional
rules (ICC, AAA, LCIA, SIAC), and leading treatises such as *Redfern & Hunter on
International Arbitration*. Chinese law, however, approaches arbitration agreements
through a strict statutory framework. `detector_cn.py` is grounded in the **PRC
Arbitration Law** and the **Supreme People's Court's 2006 Judicial Interpretation**
(法释〔2006〕7号), Articles 3–7. The recently revised PRC Arbitration Law softens some
of these rules; see the note under the statutory mapping table below.

The two systems reach opposite outcomes on structurally identical clauses. Take the
"hybrid" clause that lets either party choose between arbitration and litigation
("或裁或诉"):

- Under Chinese law (Art. 7, 2006 Interpretation), the clause is invalid *ab initio*,
  with one narrow subsequent-validation exception.
- Under ICC, AAA, or LCIA practice, the same wording is usually treated as ambiguous
  but salvageable. Courts read it down rather than strike it.

Translating one rule set into the other language would misclassify exactly these cases:
false negatives in one jurisdiction, false positives in the other. So `detector.py` and
`detector_cn.py` are written independently, each against its own jurisdiction's case
law and statute.

## Architecture

```
                    ┌─────────────────────┐
   English clause → │   detector.py        │ → 14 EN-specific checks
                    └─────────────────────┘   (ICC, AAA, LCIA, SIAC,
                                               JAMS institutional rules
                                               & Redfern & Hunter guidance)

                    ┌─────────────────────┐
   Chinese clause → │   detector_cn.py     │ → 7 CN-specific checks
                    └─────────────────────┘   (PRC Arbitration Law &
                                               2006 Judicial Interpretation,
                                               Arts. 3–7)

                    ┌──────────────────────────────────────┐
   Either language → │  Unified bilingual ML classifier      │ → single defect
                    │  (jieba segmentation for Chinese,      │   probability
                    │   TF-IDF + Logistic Regression over    │   score
                    │   a combined EN+CN vocabulary)         │
                    └──────────────────────────────────────┘
```

The Streamlit app (`app.py`) auto-detects the input language (presence of CJK
characters) and routes to the matching rule engine, while the ML classifier runs on
either language through one shared model. It is never told which language it is
processing.

## Chinese Rule Engine: Statutory Mapping

Each check in `detector_cn.py` is anchored to a specific provision of the PRC
statutory framework:

| Category | Legal Basis | Risk Level |
|:---|:---|:---|
| **或裁或诉** (Arbitration-or-litigation clause) | Art. 7, 2006 Interpretation | **Fatal** — void under PRC law |
| **仅约定仲裁规则未约定机构** (Rules cited, no institution named) | Art. 4, 2006 Interpretation | **High** — requires subsequent agreement to cure |
| **条件性约定仲裁机构** (Conditional institution, e.g. "违约方所在地仲裁委员会") | Art. 6 & Supreme Court Guiding Cases | **High** — jurisdictional uncertainty at commencement |
| **约定两个以上仲裁机构** (Two or more institutions named) | Art. 5, 2006 Interpretation | **High** — void if parties cannot agree on choice |
| **仲裁机构名称无法识别** (Unrecognized institution name) | Art. 3, 2006 Interpretation | **Medium** — saved where institution is identifiable by intent |
| **未约定仲裁地** (Missing seat of arbitration) | Drafting best practice | **Medium** — leaves procedural law undetermined |
| **争议范围表述模糊** (Vague scope of disputes) | Drafting best practice | **Advisory** — risk of partial jurisdictional challenge |

> **Note.** The Chinese engine follows the 2006 Judicial Interpretation, which still
> governs most contracts in force today. The revised PRC Arbitration Law relaxes some
> of these rules, notably around institution-name formalism. Updating `detector_cn.py`
> for the new statute is on the roadmap.

## English Rule Engine: Check Categories

`detector.py` covers 14 checks organized into five categories:

**Consent & Jurisdiction Conflict (2):** ambiguous "may" vs. "shall" language;
arbitration and litigation both permitted without exclusivity.

**Institutional Designation (2):** unrecognized institution name; named institution
and cited rules conflict (e.g. SIAC named but UNCITRAL Rules cited; AFA named but ICC
Rules cited).

**Defective Rule Selection (3):** institutional rules not specified; domestic rules
incorrectly applied to international contract (JAMS Comprehensive; AAA Commercial).

**Missing Procedural Elements (5):** missing seat of arbitration; missing governing
law; vague or narrow scope of disputes; number of arbitrators not specified; language
of arbitration not specified.

**Structural Defects (2):** unilateral option clause (asymmetric forum selection);
multi-tier clause without a defined trigger mechanism for the pre-arbitral step.

## Datasets and Results

| Dataset | Size | Rule Engine Accuracy | ML Classifier (CV) |
|:---|:---|:---|:---|
| English (`training_data_en.py`) | 221 clauses (76 valid / 145 defective) | 86.0%¹ | 94.1% (5-fold CV) |
| Chinese (`training_data_cn.py`) | 113 clauses (34 valid / 79 defective) | 98.2% | 93.8% (5-fold CV) |
| **Combined bilingual** | **334 clauses** | — | **94.0% overall** (94.1% EN / 93.8% CN) |

¹ Measured on high/medium severity flags only. Four checks (missing language,
unworkable tribunal size, multi-tier trigger, unilateral option) were added after the
original training set was built; the low-severity missing-language check produces known
false positives on older examples that pre-date it.

### Key Findings

**Feature convergence.** The classifier's strongest Chinese features (`可`, `可以`,
"may"/"can") and strongest English features (`may`, `either`, `either party`) point to
the same defect: permissive wording where mandatory wording is required. The model was
never told which language it was reading, so the convergence is not an artifact of
language-specific training.

**Iterative debugging.** Running the rule engines against the labeled data surfaced
real regex bugs. The English seat check missed `"the seat shall be Hong Kong"` because
it only matched `"seat of arbitration shall be..."`. The Chinese broad-scope check
missed the standard formula `"凡因本合同引起的或与本合同有关的任何争议"` because of a
character-distance limit that was too tight. Both fixes are locked in with regression
tests.

## Project Files

- `detector.py` / `detector_cn.py` — The two independent rule engines.
- `training_data_en.py` / `training_data_cn.py` — Labeled datasets for each language
  (hand-constructed from institutional model clauses and published judicial decisions).
- `sample_clauses.py` / `sample_clauses_cn.py` — Curated samples used in the
  Streamlit demo dropdown.
- `train_classifier_bilingual.py` — Trains the unified EN+CN classifier; produces
  `clause_classifier_bilingual.joblib`.
- `app.py` — Bilingual Streamlit interface: language auto-detection, rule-engine
  routing, and side-by-side ML/rule-engine output.
- `test_detector.py` / `test_detector_cn.py` — 17 unit and regression tests, including
  accuracy floors that fail the build if either rule engine drops below threshold.

## Running the Tool

```bash
pip install -r requirements.txt

# Train the bilingual classifier (run once; produces clause_classifier_bilingual.joblib)
python3 train_classifier_bilingual.py

# Launch the interactive web app
streamlit run app.py
```

Run the test suite:

```bash
python3 -m pytest test_detector.py test_detector_cn.py -v
```

## Limitations and Next Steps

**Pattern rigidity.** Both rule engines are regex-based and miss anything their
hand-written patterns don't cover. The Chinese "unrecognized institution name" check is
tuned conservative on purpose: Article 3 gives a safe harbor for minor name errors, so
flagging every typo would contradict how courts actually rule.

**Dataset source.** The labeled data is hand-built from institutional model clauses
and defect patterns documented in published court decisions. Real commercial arbitration
clauses sit in confidential contracts and are not publicly scrapable. The 94.0% figure
describes performance on this constructed dataset, not on production contracts. The
obvious next test: clauses quoted verbatim in published jurisdictional-challenge
decisions, since those were not written by me.

**Jurisdictional scope.** The Chinese rule set covers PRC mainland arbitration law
specifically. It has not been validated against Hong Kong, Taiwan, or Singapore
Chinese-language arbitration practice, which operate under different validity
standards.

**Code-switched clauses.** Neither rule engine has been tested on clauses mixing
Chinese and English in one sentence, which does happen in bilingual contracts. Both
engines assume single-language input.

## Disclaimer

Academic and portfolio project demonstrating rule-based NLP and ML text analysis
applied to international arbitration clause review. It does not constitute legal advice
and is not a substitute for review by qualified counsel in the relevant jurisdiction.
