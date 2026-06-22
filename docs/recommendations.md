# Chatbot QA Recommendations
## Based on LLM-as-judge evaluation of 462 queries across 77 intent categories

---

## ⚠️ Priority Categories for Prompt Improvement

### 1. failed_transfer (Relevance: 0.567 | Hallucination: 16.7%)

**Observed pattern:** Bot requests excessive clarifying information 
instead of providing general guidance first. Customer receives no 
actionable help and is immediately escalated to a human agent.

**Business impact:** Every unnecessary escalation costs agent time 
and increases resolution time. With escalation rate already at 16.7% 
overall, this category is a direct contributor.

**Recommendation:** Restructure bot prompt for this intent to follow 
a two-step approach: (1) provide general troubleshooting steps first, 
(2) then request specific details if needed.

**Expected outcome:** Relevance score improvement from 0.567 → 0.70+, 
reduction in unnecessary escalations for this category.

**Validation note:** Pattern observed in 6-query sample — 
statistical significance requires broader manual review before 
implementing prompt changes.

---

### 2. card_payment_wrong_exchange_rate (Relevance: 0.575 | Hallucination: 16.7%)

**Observed pattern:** Bot requests irrelevant personal details 
(transaction ID, item purchased) instead of addressing the core 
question about exchange rate discrepancy or asking for relevant 
information (currency pair, transaction date).

**Business impact:** Customer with an urgent financial dispute 
receives no useful response — high risk of dissatisfaction and 
complaint escalation.

**Recommendation:** Update prompt to recognize exchange rate dispute 
intent and respond with: (1) explanation of how exchange rates are 
applied, (2) request for relevant data only (currency, date, amount).

**Expected outcome:** Relevance score improvement from 0.575 → 0.70+.

**Validation note:** Pattern observed in 6-query sample — 
requires broader validation before prompt changes.

---

### 3. balance_not_updated_after_cheque_or_cash_deposit (Relevance: 0.583)

**Observed pattern:** Bot provides generic examples and hypothetical 
scenarios instead of clear step-by-step instructions for checking 
deposit status.

**Business impact:** Customer with a pending deposit receives 
confusing response — likely to call support or escalate.

**Recommendation:** Create a structured response template for this 
intent: (1) explain standard processing times, (2) provide specific 
steps to check deposit status in app, (3) escalate only if deposit 
is older than X business days.

**Expected outcome:** Relevance score improvement from 0.583 → 0.72+.

**Validation note:** Pattern observed in 6-query sample — 
requires broader validation before prompt changes.

---

## 📋 Proposed Validation Approach

Before implementing any prompt changes, recommend:

1. **Manual review** of 20+ queries per category by QA team
2. **A/B test** — run improved prompt vs current prompt on same queries
3. **Success metric** — relevance score improvement ≥ 0.10 per category
4. **Guardrail metric** — hallucination rate must not increase

---

## 🔍 Limitation Disclosure

All patterns identified from samples of 6 queries per category.
Findings are directional hypotheses, not statistically validated conclusions.
Full validation requires manual review by QA team before action.