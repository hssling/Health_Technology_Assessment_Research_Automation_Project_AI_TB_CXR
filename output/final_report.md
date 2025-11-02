# HTA Automation Report – hta_project_05_ai_tb_cxr

**Generated:** 2025-11-02 11:26:13

## 1. Protocol (parsed)
# HTA Protocol: Cost-Effectiveness of AI-Assisted Chest X-ray Screening for Tuberculosis Compared with Human Reading / GeneXpert-Only Algorithms in India

## 1. Background
India is moving towards TB elimination. Active case finding (ACF) and contact screening are key strategies. However, interpreting large volumes of chest X-rays is resource-intensive. AI-based CXR tools (CAD4TB and similar WHO-approved CAD solutions) can triage presumptive TB for confirmatory testing (e.g. GeneXpert/Truenat). There is a need to assess whether adding AI to the diagnostic cascade is cost-effective compared with existing algorithms.

## 2. Objectives
- To determine the cost-effectiveness of AI-assisted CXR screening in ACF / OPD settings compared with (a) human X-ray reading and (b) no CXR (symptom + Xpert only).
- To estimate budget impact for NTEP/state TB cells for scaling to district/mobile vans.
- To explore threshold prices for AI licensing per X-ray / per device.

## 3. PICO
- **Population:** Adults undergoing TB screening in ACF campaigns, OPDs, and high-TB-burden districts.
- **Intervention:** AI/CAD-based CXR interpretation with defined score threshold to refer for GeneXpert/Truenat.
- **Comparators:** 
  1. Human radiologist/physician CXR reading,
  2. Symptom screening + GeneXpert only (no X-ray).
- **Outcomes:** TB cases detected, time to diagnosis, false positives, cost per case detected, cost per DALY averted.
- **Perspective:** Programme (NTEP); secondary societal.
- **Time horizon:** 1–5 years.
- **Discounting:** 3%.

## 4. Methods

### 4.1 Diagnostic Accuracy
- Extract sensitivity/specificity of AI-CXR tools at different thresholds from WHO TB CAD reports and Indian evaluation studies.
- Compare with human readers.
- Model the diagnostic pathway: Screen → CXR (AI or human) → Xpert → TB diagnosed → treatment.

### 4.2 Economic Model
- Decision tree per 10,000 individuals screened.
- Costs:
  - AI license / per-read cost
  - CXR cost
  - Xpert/Truenat test cost
  - Treatment cost for TB (DS-TB)
  - Cost of false positives (unnecessary Xpert)
- Outcomes:
  - True TB detected
  - DALYs averted using standard TB disability weights
  - ICER = cost per additional TB case detected or cost per DALY averted

### 4.3 Scenarios
- Mobile van with digital X-ray + AI (rural)
- District hospital OPD high-volume
- Different AI license pricing
- Different TB prevalence (ACF vs general OPD)

### 4.4 Budget Impact
- Number of X-rays per year per district/state
- Apply AI-per-read fee vs perpetual license
- Estimate incremental NTEP budget

## 5. Outputs
1. Search strategy
2. Diagnostic accuracy extraction sheet
3. Python decision-tree model
4. BIA sheet
5. Draft manuscript / policy brief


## 2. Search Strategy
PubMed / WHO search:
(("Tuberculosis/diagnosis"[Mesh] OR "pulmonary tuberculosis" OR "TB screening")
AND ("computer aided diagnosis" OR "CAD" OR "AI" OR "artificial intelligence" OR "deep learning" OR "CAD4TB" OR "qXR" OR "Lunit")
AND (X-ray OR "chest radiography" OR CXR OR "digital radiography")
AND (India OR "high TB burden")
AND (cost OR "cost-effectiveness" OR HTA OR "economic evaluation"))

Also consult:
- WHO Rapid Communication on automated CXR detection of TB
- FIND evaluation reports
- NTEP ACF/mobile van guidelines


## 3. Model Output (stdout)
```
Symptom+Xpert: cost 13270000.0 TB detected 260.0 Cost per TB detected 51038.46153846154
Human CXR:     cost 8200000.0 TB detected 320.0 Cost per TB detected 25625.0
AI CXR:        cost 10100000.0 TB detected 360.0 Cost per TB detected 28055.555555555555
ICER (INR per additional TB detected) – AI vs Human: 47500.0

```

## 4. Draft Manuscript (template)
# Draft Manuscript – Cost-Effectiveness of AI-Assisted Chest X-Ray Screening for Tuberculosis in India

## Title
Economic Evaluation of Artificial Intelligence-Based Chest Radiography Screening for Tuberculosis in India: A Programme Perspective

## Abstract
To be auto-filled from model runs.

## Sections
1. Introduction – TB elimination, ACF, digital X-ray vans, rationale for AI
2. Methods – decision tree, diagnostic accuracy, cost inputs, scenario analyses
3. Results – cost per TB detected; ICER AI vs human vs symptom-only
4. Discussion – affordability for NTEP, pricing of AI licenses, operational issues
5. Conclusion – policy message


## 5. Orchestrator Log
```
=== Processing project: hta_project_05_ai_tb_cxr ===
Protocol: loaded.
Search strings: loaded.
Literature search: starting...
Literature search: completed, extracted 8 data points.
Data processing: starting...
Data processing: completed, filled 8 rows.
R: executed.
R stderr:
â”€â”€ Attaching core tidyverse packages â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ tidyverse 2.0.0 â”€â”€
âœ” dplyr     1.1.4     âœ” readr     2.1.5
âœ” forcats   1.0.0     âœ” stringr   1.5.2
âœ” ggplot2   4.0.0     âœ” tibble    3.3.0
âœ” lubridate 1.9.4     âœ” tidyr     1.3.1
âœ” purrr     1.1.0     
â”€â”€ Conflicts â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ tidyverse_conflicts() â”€â”€
âœ– dplyr::filter() masks stats::filter()
âœ– dplyr::lag()    masks stats::lag()
â„¹ Use the conflicted package (<http://conflicted.r-lib.org/>) to force all conflicts to become errors
Error: 'data/ai_tb_cxr_search_results.csv' does not exist in current working directory ('D:/research-automation/HTA projects').
Execution halted

Model: executed 04_ai_tb_cxr_model.py
Model stdout:
Symptom+Xpert: cost 13270000.0 TB detected 260.0 Cost per TB detected 51038.46153846154
Human CXR:     cost 8200000.0 TB detected 320.0 Cost per TB detected 25625.0
AI CXR:        cost 10100000.0 TB detected 360.0 Cost per TB detected 28055.555555555555
ICER (INR per additional TB detected) – AI vs Human: 47500.0

Manuscript generation: starting...
Manuscript generation: completed.
```