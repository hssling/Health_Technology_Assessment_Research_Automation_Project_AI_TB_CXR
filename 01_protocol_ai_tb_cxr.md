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
