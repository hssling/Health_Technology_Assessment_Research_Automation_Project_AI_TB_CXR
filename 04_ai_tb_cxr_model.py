"""AI-based TB CXR screening HTA – decision tree
Compares three strategies:
1. Symptom + Xpert only
2. Human CXR + Xpert
3. AI-CXR + Xpert
Outputs cost per TB case detected and cost per DALY averted.
"""

import math

population = 10000  # people screened
tb_prev = 0.04      # 4% in ACF
tb_cases = population * tb_prev

# Costs (INR) – placeholders
cost_xpert = 1500
cost_cxr = 300
cost_ai_read = 80
cost_tb_treatment = 8000

# Diagnostic performance – placeholders
sens_symptom = 0.65
spec_symptom = 0.9

sens_human_cxr = 0.80
spec_human_cxr = 0.85

sens_ai_cxr = 0.90
spec_ai_cxr = 0.80

def strategy_symptom_only():
    tested = population * sens_symptom
    true_pos = tb_cases * sens_symptom
    false_pos = (population - tb_cases) * (1 - spec_symptom)
    xpert_tests = tested + false_pos
    cost = xpert_tests * cost_xpert + true_pos * cost_tb_treatment
    return cost, true_pos

def strategy_human_cxr():
    cxr_all = population
    true_pos_cxr = tb_cases * sens_human_cxr
    false_pos_cxr = (population - tb_cases) * (1 - spec_human_cxr)
    xpert_tests = true_pos_cxr + false_pos_cxr
    cost = cxr_all * cost_cxr + xpert_tests * cost_xpert + true_pos_cxr * cost_tb_treatment
    return cost, true_pos_cxr

def strategy_ai_cxr():
    cxr_all = population
    true_pos_cxr = tb_cases * sens_ai_cxr
    false_pos_cxr = (population - tb_cases) * (1 - spec_ai_cxr)
    xpert_tests = true_pos_cxr + false_pos_cxr
    cost = cxr_all * cost_cxr + cxr_all * cost_ai_read + xpert_tests * cost_xpert + true_pos_cxr * cost_tb_treatment
    return cost, true_pos_cxr

if __name__ == "__main__":
    cost_s, tp_s = strategy_symptom_only()
    cost_h, tp_h = strategy_human_cxr()
    cost_ai, tp_ai = strategy_ai_cxr()

    print("Symptom+Xpert: cost", cost_s, "TB detected", tp_s, "Cost per TB detected", cost_s / tp_s)
    print("Human CXR:     cost", cost_h, "TB detected", tp_h, "Cost per TB detected", cost_h / tp_h)
    print("AI CXR:        cost", cost_ai, "TB detected", tp_ai, "Cost per TB detected", cost_ai / tp_ai)

    # Incremental vs human
    incr_cost = cost_ai - cost_h
    incr_tb = tp_ai - tp_h
    icer_tb = incr_cost / incr_tb if incr_tb != 0 else None
    print("ICER (INR per additional TB detected) – AI vs Human:", icer_tb)
