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
st.title("🚌 Public Sentiment Tracker – Distance-Based Fare in Rwanda")

# Sentiment over time
st.subheader("📈 Sentiment Over Time")
sentiment_time = filtered_df.groupby(['date', 'sentiment']).size().reset_index(name='counts')
fig_time = px.line(sentiment_time, x='date', y='counts', color='sentiment', markers=True)
st.plotly_chart(fig_time, use_container_width=True)

# Sentiment by Region
st.subheader("🗺️ Sentiment by Region")
region_sentiment = filtered_df.groupby(['region', 'sentiment']).size().unstack().fillna(0)
st.dataframe(region_sentiment)

# Word Cloud of Common Terms
st.subheader("☁️ Common Terms from Public Feedback")
text = " ".join(filtered_df['text'].tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

fig_wc, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig_wc)

# Recommendation Section
st.subheader("📝 Insights & Recommendations")
st.markdown("""
- **Clarify Fare Rules**: High confusion around how fares are calculated.
- **Improve Communication**: Negative sentiment spikes align with major announcements lacking follow-up.
- **Watch Misinformation**: Some posts falsely claim doubling of fares in certain areas.
""")

# Footer
st.markdown("---")
st.caption("Developed as a prototype to support transport policy decisions in Rwanda.")
