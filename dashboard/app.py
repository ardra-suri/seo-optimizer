# dashboard/app.py

import os
import sys
import ast

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
import streamlit as st
from scraper.storage.database import ScrapeDB
import pandas as pd
import plotly.express as px
from datetime import datetime

# Initialize database
db = ScrapeDB("data/seo_optimizer.db")

# Page configuration
st.set_page_config(page_title="SEO Content Analyzer", layout="wide", initial_sidebar_state="expanded")

# Sidebar controls
st.sidebar.title("Controls")
analysis_limit = st.sidebar.slider("Recent analyses to show", min_value=5, max_value=50, value=10)

st.title("SEO Content Analysis Dashboard")

# === Section 1: Run New Analysis ===
with st.expander("🔍 Run New Analysis", expanded=True):
    col1, col2 = st.columns(2)
    your_url = col1.text_input("Your URL")
    competitor_url = col2.text_input("Competitor URL")

    if st.button("Analyze", type="primary"):
        if your_url and competitor_url:
            with st.spinner("Analyzing content..."):
                from scraper.core import compare_with_competitor
                result = compare_with_competitor(your_url, competitor_url)

                if result.get("error"):
                    st.error(f"Analysis failed: {result['error']}")
                else:
                    st.success("Analysis completed!")

                    m1, m2, m3 = st.columns(3)
                    m1.metric("Similarity Score", f"{result['analysis']['similarity_score']:.0%}")
                    m2.metric("Word Count Difference", result['analysis']['word_count_diff'])
                    m3.metric("Missing Keywords", len(result['analysis']['top_missing_keywords']))

                    st.subheader("Raw Analysis Data")
                    st.json(result)

        else:
            st.warning("Please enter both URLs")

# === Section 2: Historical Analyses ===
st.header("📈 Analysis History")
raw_analyses = db.get_recent_analyses(limit=analysis_limit)

if raw_analyses:
    # Rename keys to match table headers
    df = pd.DataFrame([{
        "Your URL": row["url1"],
        "Competitor URL": row["url2"],
        "Similarity": row["similarity"],
        "Missing Keywords": row.get("missing_keywords", []),
        "Timestamp": row["timestamp"]
    } for row in raw_analyses])

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Date"] = df["Timestamp"].dt.date

    st.dataframe(df.sort_values("Timestamp", ascending=False), use_container_width=True)

    tab1, tab2 = st.tabs(["Trends", "Keywords"])

    with tab1:
        fig = px.line(df, x="Timestamp", y="Similarity", title="Content Similarity Over Time", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Flatten missing keyword lists and count frequencies
        keyword_counts = pd.Series(
            [kw for sublist in df['Missing Keywords'] if isinstance(sublist, list) for kw in sublist]
        ).value_counts()
        if not keyword_counts.empty:
            st.bar_chart(keyword_counts.head(10))
        else:
            st.info("No missing keywords found to chart.")
else:
    st.info("No analyses found. Run your first analysis above.")

