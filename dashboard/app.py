import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Chatbot QA Dashboard", layout="wide")
st.title("🤖 LLM Chatbot QA Dashboard")
st.markdown("Banking support chatbot quality evaluation — Banking77 dataset")


@st.cache_data
def load_data():
    results = pd.read_csv("analysis/data/evaluation_results.csv")
    category_stats = pd.read_csv("analysis/data/category_stats.csv")
    return results, category_stats

results_df, category_stats = load_data()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Avg Relevance Score", f"{results_df['relevance_score'].mean():.2f}")
with col2:
    st.metric("Hallucination Rate", f"{results_df['hallucination'].mean():.1%}")
with col3:
    st.metric("Escalation Rate", f"{results_df['escalation_needed'].mean():.1%}")
with col4:
    below_threshold = (category_stats['avg_relevance'] < 0.6).sum()
    st.metric("Categories Below 0.6", f"{below_threshold} / {len(category_stats)}")

st.divider()


st.subheader("⚠️ Lowest Performing Categories")

bottom15 = category_stats.nsmallest(15, 'avg_relevance')
fig1 = px.bar(
    bottom15,
    x='avg_relevance',
    y='category',
    orientation='h',
    color='avg_relevance',
    color_continuous_scale='RdYlGn',
    range_color=[0.4, 1.0],
    labels={'avg_relevance': 'Avg Relevance Score', 'category': 'Intent Category'},
    title="Bottom 15 Categories by Relevance Score"
)
fig1.add_vline(x=0.6, line_dash="dash", line_color="red", annotation_text="Threshold 0.6")
fig1.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig1, use_container_width=True)

st.divider()

st.subheader("🔴 Hallucination Rate by Category")

hallucinating = category_stats[category_stats['hallucination_rate'] > 0].sort_values(
    'hallucination_rate', ascending=False
).head(15)

fig2 = px.bar(
    hallucinating,
    x='category',
    y='hallucination_rate',
    color='hallucination_rate',
    color_continuous_scale='Reds',
    labels={'hallucination_rate': 'Hallucination Rate', 'category': 'Intent Category'},
    title="Categories with Highest Hallucination Rate"
)
fig2.update_layout(height=400, xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)

st.divider()


st.subheader("🔍 Category Deep Dive")

selected_category = st.selectbox(
    "Select intent category to inspect:",
    options=sorted(results_df['category'].unique())
)

filtered = results_df[results_df['category'] == selected_category]

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Avg Relevance", f"{filtered['relevance_score'].mean():.2f}")
with col_b:
    st.metric("Hallucination Rate", f"{filtered['hallucination'].mean():.1%}")
with col_c:
    st.metric("Escalation Rate", f"{filtered['escalation_needed'].mean():.1%}")

st.markdown("**Sample queries and responses:**")
st.dataframe(
    filtered[['query', 'bot_response', 'relevance_score', 'hallucination', 'escalation_needed']],
    use_container_width=True,
    height=300
)


st.divider()
st.subheader("📥 Export Results")

if st.button("Export to JSON"):
    if len(results_df) > 0:
        json_data = results_df.to_json(orient='records', indent=2)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="evaluation_results.json",
            mime="application/json"
        )
    else:
        st.error("No data available for export.")