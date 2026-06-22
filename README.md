**Sampling:** Stratified sample of 6 queries per category (462 total out of 3,080)
to ensure all 77 intent categories are represented equally.

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/KQnok/llm-chatbot-qa.git
cd llm-chatbot-qa

# Install dependencies
pip install groq streamlit plotly pandas python-dotenv

# Add your API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run the evaluation pipeline
jupyter notebook analysis/qa_analysis.ipynb

# Launch the dashboard
python -m streamlit run dashboard/app.py
```

---

## 🔬 Judge Calibration

To validate LLM-as-judge reliability, 10 random samples were manually
reviewed and compared against judge scores.

**Results:** 7/10 full agreement, 2/10 minor divergence (±0.1),
1/10 significant divergence (judge overscored by ~0.2).

**Known bias identified:** Judge tends to reward polite, action-oriented
responses even when they lack substantive explanation
("Let me help you fix that" scored 0.80 vs human score 0.60–0.70).

**Mitigation applied:** System prompt updated to instruct judge to
evaluate informational content only, ignoring politeness phrases.

**Conclusion:** Judge scores are directionally reliable for identifying
low-performing categories. Absolute scores should be interpreted with
±0.1 margin. Full manual QA review recommended before acting on results.

---

## 🗄️ SQL Analysis

Key metrics can be reproduced with SQL on the exported CSV
loaded into any database:

```sql
-- Average relevance score by intent category (worst performers first)
SELECT
    category,
    ROUND(AVG(relevance_score), 3)              AS avg_relevance,
    ROUND(AVG(CAST(hallucination AS INT)), 3)   AS hallucination_rate,
    ROUND(AVG(CAST(escalation_needed AS INT)), 3) AS escalation_rate,
    COUNT(*)                                    AS query_count
FROM evaluation_results
GROUP BY category
ORDER BY avg_relevance ASC;

-- Categories below performance threshold
SELECT category, ROUND(AVG(relevance_score), 3) AS avg_relevance
FROM evaluation_results
GROUP BY category
HAVING AVG(relevance_score) < 0.6
ORDER BY avg_relevance ASC;

-- Overall KPIs
SELECT
    ROUND(AVG(relevance_score), 3)               AS avg_relevance,
    ROUND(AVG(CAST(hallucination AS INT)), 3)    AS hallucination_rate,
    ROUND(AVG(CAST(escalation_needed AS INT)), 3) AS escalation_rate,
    COUNT(*)                                     AS total_evaluated
FROM evaluation_results;
```

---

## 🔌 API Testing with Postman

The Groq API used in this project can be tested directly via Postman.

**Endpoint:** `https://api.groq.com/openai/v1/chat/completions`
**Method:** POST
**Headers:**
- `Authorization: Bearer YOUR_GROQ_API_KEY`
- `Content-Type: application/json`

**Body — bot response generation:**
```json
{
  "model": "llama-3.1-8b-instant",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful banking support chatbot."
    },
    {
      "role": "user",
      "content": "How do I block my card?"
    }
  ]
}
```

**Body — LLM-as-judge evaluation:**
```json
{
  "model": "llama-3.1-8b-instant",
  "messages": [
    {
      "role": "system",
      "content": "You are a QA evaluator. Return ONLY valid JSON."
    },
    {
      "role": "user",
      "content": "Customer query: How do I block my card?\nBot response: You can block your card in the app under Settings > Cards > Block Card.\n\nEvaluate and return: {\"relevance_score\": float, \"hallucination\": bool, \"escalation_needed\": bool}"
    }
  ]
}
```

---

## 📋 BA Documentation

This project includes full BA documentation:

- **BRD** — business objectives, scope, stakeholders, functional
  and non-functional requirements, assumptions and constraints
- **User Stories** — 4 stakeholders (Head of Support, QA Analyst,
  Chatbot Developer, Compliance Officer) with Given/When/Then AC
- **BPMN Diagram** — full support chatbot process: customer verification
  subprocess, confidence score gateway, escalation flow, timer boundary
  event, interaction logging

---

## ⚠️ Limitations

- Sample of 462 queries (15% of Banking77) — patterns are directional,
  not statistically validated
- LLM-generated bot responses simulate chatbot behaviour —
  not a real production chatbot
- Judge calibration based on 10 manual samples — full validation
  requires broader human review
- Dataset is English only — real Banco Plata chatbot would require
  Spanish language evaluation

---

## 👤 Author

**Karina Kuralionak**
- GitHub: [github.com/KQnok](https://github.com/KQnok)
- LinkedIn: [linkedin.com/in/karina-kuralionak](https://linkedin.com/in/karina-kuralionak)