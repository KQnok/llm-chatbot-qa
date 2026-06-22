import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Chatbot QA Dashboard", layout="wide")
st.title("🤖 LLM Chatbot QA Dashboard")
st.markdown("Banking support chatbot quality evaluation — Banking77 dataset, 462 queries across 77 intent categories")

# ── Metric explanations ───────────────────────────────────────────────────────
with st.expander("📖 What do these metrics mean?"):
    st.markdown("""
    | Metric | What it means | Good value |
    |--------|--------------|------------|
    | **Relevance Score** | Does the bot actually answer the customer's question? (0 = completely off-topic, 1 = perfectly relevant) | > 0.75 |
    | **Hallucination Rate** | % of responses where the bot made up false information (e.g. fake phone numbers, wrong policies) | < 5% |
    | **Escalation Rate** | % of queries the bot couldn't resolve and needed to pass to a human agent | < 20% |
    | **Categories Below Threshold** | Number of intent categories where average relevance < 0.6 — these need prompt improvement | Lower is better |
    """)

# Load data
@st.cache_data
def load_data():
    results = pd.read_csv("analysis/data/evaluation_results.csv")
    category_stats = pd.read_csv("analysis/data/category_stats.csv")
    return results, category_stats

results_df, category_stats = load_data()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.subheader("Overall Performance")
col1, col2, col3, col4 = st.columns(4)

avg_relevance = results_df['relevance_score'].mean()
hallucination = results_df['hallucination'].mean()
escalation = results_df['escalation_needed'].mean()
below_threshold = (category_stats['avg_relevance'] < 0.6).sum()

with col1:
    delta = "✅ Above target" if avg_relevance >= 0.75 else "⚠️ Below target (0.75)"
    st.metric("Avg Relevance Score", f"{avg_relevance:.2f}", delta)
with col2:
    delta = "✅ Within limit" if hallucination <= 0.05 else "🔴 Above limit (5%)"
    st.metric("Hallucination Rate", f"{hallucination:.1%}", delta)
with col3:
    delta = "✅ Within limit" if escalation <= 0.20 else "⚠️ Above limit (20%)"
    st.metric("Escalation Rate", f"{escalation:.1%}", delta)
with col4:
    st.metric("Categories Below 0.6 Threshold", f"{below_threshold} / {len(category_stats)}")

st.caption("Targets based on finance industry benchmarks: relevance ≥ 0.75, hallucination ≤ 5%, escalation ≤ 20%")

st.divider()

# ── Metric selector ───────────────────────────────────────────────────────────
st.subheader("📊 Performance by Intent Category")

metric_option = st.radio(
    "Select metric to visualize:",
    options=["avg_relevance", "hallucination_rate", "escalation_rate"],
    format_func=lambda x: {
        "avg_relevance": "Relevance Score (higher = better)",
        "hallucination_rate": "Hallucination Rate (lower = better)",
        "escalation_rate": "Escalation Rate (lower = better)"
    }[x],
    horizontal=True
)

n_categories = st.slider("Show top N worst-performing categories:", min_value=5, max_value=40, value=15)

if metric_option == "avg_relevance":
    sorted_df = category_stats.nsmallest(n_categories, 'avg_relevance')
    color_scale = 'RdYlGn'
    threshold = 0.6
    threshold_label = "Min threshold 0.6"
    title = f"Bottom {n_categories} Categories by Relevance Score"
else:
    sorted_df = category_stats.nlargest(n_categories, metric_option)
    color_scale = 'Reds'
    threshold = None
    title = f"Top {n_categories} Categories by {metric_option.replace('_', ' ').title()}"

fig = px.bar(
    sorted_df,
    x=metric_option,
    y='category',
    orientation='h',
    color=metric_option,
    color_continuous_scale=color_scale,
    title=title,
    labels={
        'avg_relevance': 'Avg Relevance Score',
        'hallucination_rate': 'Hallucination Rate',
        'escalation_rate': 'Escalation Rate',
        'category': 'Intent Category'
    }
)

if threshold:
    fig.add_vline(x=threshold, line_dash="dash", line_color="red",
                  annotation_text=threshold_label, annotation_position="top right")

fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig, use_container_width=True)

st.caption("""
**How to read this chart:** Each bar represents one type of customer query (intent category).
Longer red bars = categories where the bot performs poorly and needs prompt improvement.
Green bars = categories where the bot handles queries well.
""")

st.divider()

# ── Category drill-down ───────────────────────────────────────────────────────
st.subheader("🔍 Category Deep Dive")
st.markdown("Select a category to see individual query examples and bot responses.")

selected_category = st.selectbox(
    "Select intent category:",
    options=sorted(results_df['category'].unique())
)

filtered = results_df[results_df['category'] == selected_category]
cat_stats = category_stats[category_stats['category'] == selected_category].iloc[0]

col_a, col_b, col_c = st.columns(3)
with col_a:
    color = "🟢" if cat_stats['avg_relevance'] >= 0.75 else "🔴"
    st.metric(f"{color} Avg Relevance", f"{cat_stats['avg_relevance']:.2f}")
with col_b:
    color = "🟢" if cat_stats['hallucination_rate'] <= 0.05 else "🔴"
    st.metric(f"{color} Hallucination Rate", f"{cat_stats['hallucination_rate']:.1%}")
with col_c:
    color = "🟢" if cat_stats['escalation_rate'] <= 0.20 else "🔴"
    st.metric(f"{color} Escalation Rate", f"{cat_stats['escalation_rate']:.1%}")

st.markdown("**Sample queries and bot responses:**")
display_df = filtered[['query', 'bot_response', 'relevance_score', 'hallucination', 'escalation_needed']].copy()
display_df.columns = ['Customer Query', 'Bot Response', 'Relevance Score', 'Hallucination', 'Escalation Needed']
st.dataframe(display_df, use_container_width=True, height=300)

st.divider()

# ── Export ────────────────────────────────────────────────────────────────────
st.subheader("📥 Export Results")
st.markdown("Download full evaluation results for further analysis or prompt improvement.")

if len(results_df) > 0:
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        json_data = results_df.to_json(orient='records', indent=2)
        st.download_button(
            label="⬇️ Download JSON (for developers)",
            data=json_data,
            file_name="evaluation_results.json",
            mime="application/json"
        )
    
    with col_exp2:
        csv_data = results_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download CSV (for business users)",
            data=csv_data,
            file_name="evaluation_results.csv",
            mime="text/csv"
        )
else:
    st.error("No data available for export.")