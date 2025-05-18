import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Public Sentiment Tracker", layout="wide")

# -------------------------
# Simulated Data
# -------------------------
# Load or simulate sample sentiment data
@st.cache_data
def load_data():
    data = {
        "date": pd.date_range(start="2025-01-01", periods=100),
        "sentiment": ["Positive", "Neutral", "Negative"] * 33 + ["Positive"],
        "platform": ["Twitter", "Facebook", "Survey"] * 33 + ["Twitter"],
        "region": ["Kigali", "Northern", "Southern", "Western", "Eastern"] * 20,
        "text": ["Affordable", "Too expensive", "Unclear fare", "Tap&Go working", "Confusing pricing"] * 20
    }
    df = pd.DataFrame(data)
    return df

df = load_data()

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.title("Filter Options")
platform_filter = st.sidebar.multiselect("Select Platform", options=df['platform'].unique(), default=df['platform'].unique())
sentiment_filter = st.sidebar.multiselect("Select Sentiment", options=df['sentiment'].unique(), default=df['sentiment'].unique())

filtered_df = df[(df['platform'].isin(platform_filter)) & (df['sentiment'].isin(sentiment_filter))]

# -------------------------
# Main Dashboard
# -------------------------
st.title("\U0001F68C Public Sentiment Tracker – Distance-Based Fare in Rwanda")

st.markdown("""
Welcome to the Public Sentiment Tracker for Rwanda's new distance-based fare system. 
This dashboard allows you to explore sentiment trends and public feedback across various platforms.
""")

# Data preview toggle
if st.checkbox("Show raw data"):
    st.dataframe(filtered_df.head())

# Layout with columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("\U0001F4C8 Sentiment Over Time")
    sentiment_time = filtered_df.groupby(['date', 'sentiment']).size().reset_index(name='counts')
    fig_time = px.line(sentiment_time, x='date', y='counts', color='sentiment', markers=True)
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    st.subheader("\U0001F5FA\uFE0F Sentiment by Region")
    region_sentiment = filtered_df.groupby(['region', 'sentiment']).size().unstack().fillna(0)
    st.dataframe(region_sentiment)

# Word Cloud of Common Terms
st.subheader("\u2601\ufe0f Common Terms from Public Feedback")
text = " ".join(filtered_df['text'].tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

fig_wc, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig_wc)

# Recommendation Section
st.subheader("\U0001F4DD Insights & Recommendations")
st.markdown("""
- **Clarify Fare Rules**: High confusion around how fares are calculated.
- **Improve Communication**: Negative sentiment spikes align with major announcements lacking follow-up.
- **Watch Misinformation**: Some posts falsely claim doubling of fares in certain areas.
""")

# Footer
st.markdown("---")
st.caption("Developed as a prototype to support transport policy decisions in Rwanda.")
