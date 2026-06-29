import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from datetime import datetime
import json
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Feedback Dashboard",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Data helpers ──────────────────────────────────────────────────────────────
DATA_FILE = "data/feedbacks.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return polarity, subjectivity, label

# ── Seed sample data if empty ─────────────────────────────────────────────────
def seed_sample_data():
    samples = [
        ("Alice Johnson", "Product", "The product quality is outstanding! Really happy with my purchase.", 5),
        ("Bob Smith", "Support", "Support team was slow to respond. Took 3 days to get a reply.", 2),
        ("Carol Davis", "Delivery", "Delivery was super fast and packaging was perfect.", 5),
        ("David Lee", "Product", "Average product. Nothing special but does the job.", 3),
        ("Eva Martinez", "Support", "Absolutely terrible customer service experience.", 1),
        ("Frank Wilson", "Delivery", "Package arrived late and was damaged. Very disappointed.", 1),
        ("Grace Kim", "Product", "Love it! Best purchase I have made this year.", 5),
        ("Henry Brown", "Support", "The support team was incredibly helpful and resolved my issue instantly.", 5),
        ("Irene Clark", "Delivery", "Neutral experience. Delivery was on time, nothing more.", 3),
        ("James White", "Product", "Product broke after a week. Horrible quality.", 1),
    ]
    data = []
    for i, (name, category, text, rating) in enumerate(samples):
        pol, sub, label = analyze_sentiment(text)
        data.append({
            "id": i + 1,
            "name": name,
            "category": category,
            "feedback": text,
            "rating": rating,
            "polarity": pol,
            "subjectivity": sub,
            "sentiment": label,
            "timestamp": f"2024-0{(i % 9) + 1}-{(i * 3 + 1):02d} 10:00:00",
        })
    save_data(data)
    return data

# ── Load or seed ──────────────────────────────────────────────────────────────
feedbacks = load_data()
if not feedbacks:
    feedbacks = seed_sample_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/speech-bubble.png", width=64)
    st.title("Feedback Dashboard")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "➕ Add Feedback", "📋 All Feedbacks"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption(f"Total Feedbacks: **{len(feedbacks)}**")

df = pd.DataFrame(feedbacks) if feedbacks else pd.DataFrame()

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.title("📊 Customer Feedback Dashboard")
    st.markdown("Real-time sentiment analysis powered by TextBlob")
    st.markdown("---")

    if df.empty:
        st.info("No feedback yet. Add some from the sidebar!")
    else:
        # ── KPI cards ─────────────────────────────────────────────────────────
        total = len(df)
        pos   = len(df[df["sentiment"] == "Positive"])
        neg   = len(df[df["sentiment"] == "Negative"])
        neu   = len(df[df["sentiment"] == "Neutral"])
        avg_r = round(df["rating"].mean(), 2)
        avg_p = round(df["polarity"].mean(), 3)

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Total Feedbacks", total)
        c2.metric("Avg Rating", f"{avg_r} ⭐")
        c3.metric("Avg Polarity", avg_p)
        c4.metric("😊 Positive", pos)
        c5.metric("😐 Neutral",  neu)
        c6.metric("😞 Negative", neg)

        st.markdown("---")

        # ── Row 1: Sentiment pie + Rating bar ─────────────────────────────────
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Sentiment Distribution")
            sent_counts = df["sentiment"].value_counts().reset_index()
            sent_counts.columns = ["Sentiment", "Count"]
            color_map = {"Positive": "#2ecc71", "Neutral": "#f39c12", "Negative": "#e74c3c"}
            fig_pie = px.pie(
                sent_counts,
                names="Sentiment",
                values="Count",
                color="Sentiment",
                color_discrete_map=color_map,
                hole=0.45,
            )
            fig_pie.update_traces(textinfo="percent+label", textfont_size=13)
            fig_pie.update_layout(showlegend=True, margin=dict(t=20, b=20))
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.subheader("Ratings Breakdown")
            rating_counts = df["rating"].value_counts().sort_index().reset_index()
            rating_counts.columns = ["Rating", "Count"]
            fig_bar = px.bar(
                rating_counts,
                x="Rating",
                y="Count",
                color="Rating",
                color_continuous_scale="RdYlGn",
                text="Count",
            )
            fig_bar.update_traces(textposition="outside")
            fig_bar.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Star Rating",
                yaxis_title="Number of Feedbacks",
                margin=dict(t=20, b=20),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # ── Row 2: Category breakdown + Polarity scatter ───────────────────────
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Feedbacks by Category")
            cat_sent = df.groupby(["category", "sentiment"]).size().reset_index(name="Count")
            fig_cat = px.bar(
                cat_sent,
                x="category",
                y="Count",
                color="sentiment",
                barmode="group",
                color_discrete_map=color_map,
            )
            fig_cat.update_layout(
                xaxis_title="Category",
                yaxis_title="Count",
                legend_title="Sentiment",
                margin=dict(t=20, b=20),
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        with col4:
            st.subheader("Polarity vs Subjectivity")
            fig_scatter = px.scatter(
                df,
                x="polarity",
                y="subjectivity",
                color="sentiment",
                size="rating",
                hover_data=["name", "category", "feedback"],
                color_discrete_map=color_map,
            )
            fig_scatter.update_layout(
                xaxis_title="Polarity (Negative ← 0 → Positive)",
                yaxis_title="Subjectivity (Objective → Subjective)",
                margin=dict(t=20, b=20),
            )
            fig_scatter.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
            fig_scatter.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.5)
            st.plotly_chart(fig_scatter, use_container_width=True)

        # ── Row 3: Polarity trend ──────────────────────────────────────────────
        st.subheader("Polarity Trend Over Time")
        df_sorted = df.copy()
        df_sorted["timestamp"] = pd.to_datetime(df_sorted["timestamp"])
        df_sorted = df_sorted.sort_values("timestamp")
        fig_line = px.line(
            df_sorted,
            x="timestamp",
            y="polarity",
            color="sentiment",
            markers=True,
            color_discrete_map=color_map,
            hover_data=["name", "feedback"],
        )
        fig_line.update_layout(
            xaxis_title="Date",
            yaxis_title="Polarity Score",
            legend_title="Sentiment",
            margin=dict(t=20, b=20),
        )
        fig_line.add_hline(y=0, line_dash="dot", line_color="gray")
        st.plotly_chart(fig_line, use_container_width=True)

        # ── Row 4: Average polarity per category ───────────────────────────────
        st.subheader("Average Polarity by Category")
        avg_pol = df.groupby("category")["polarity"].mean().reset_index()
        avg_pol.columns = ["Category", "Avg Polarity"]
        avg_pol["Color"] = avg_pol["Avg Polarity"].apply(
            lambda x: "#2ecc71" if x > 0.1 else ("#e74c3c" if x < -0.1 else "#f39c12")
        )
        fig_hbar = go.Figure(go.Bar(
            x=avg_pol["Avg Polarity"],
            y=avg_pol["Category"],
            orientation="h",
            marker_color=avg_pol["Color"],
            text=avg_pol["Avg Polarity"].round(3),
            textposition="outside",
        ))
        fig_hbar.update_layout(
            xaxis_title="Average Polarity",
            yaxis_title="",
            margin=dict(t=20, b=20),
        )
        fig_hbar.add_vline(x=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_hbar, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — ADD FEEDBACK
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Add Feedback":
    st.title("➕ Add New Feedback")
    st.markdown("Submit customer feedback and instantly analyze its sentiment.")
    st.markdown("---")

    with st.form("feedback_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Customer Name *", placeholder="e.g. Jane Doe")
            category = st.selectbox("Category *", ["Product", "Support", "Delivery", "Billing", "Other"])
        with col2:
            rating = st.slider("Star Rating *", 1, 5, 3)
            st.write("Rating: " + "⭐" * rating)

        feedback_text = st.text_area(
            "Feedback *",
            placeholder="Write the customer's feedback here…",
            height=150,
        )

        submitted = st.form_submit_button("🔍 Analyze & Save Feedback", use_container_width=True)

    if submitted:
        if not name.strip() or not feedback_text.strip():
            st.error("Customer name and feedback are required.")
        else:
            polarity, subjectivity, label = analyze_sentiment(feedback_text)

            # Display live result
            st.markdown("---")
            st.subheader("📝 Sentiment Analysis Result")

            r1, r2, r3, r4 = st.columns(4)
            emoji = "😊" if label == "Positive" else ("😞" if label == "Negative" else "😐")
            r1.metric("Sentiment", f"{emoji} {label}")
            r2.metric("Polarity", polarity, help="-1 (very negative) to +1 (very positive)")
            r3.metric("Subjectivity", subjectivity, help="0 (objective) to 1 (subjective)")
            r4.metric("Rating", "⭐" * rating)

            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=polarity,
                delta={"reference": 0},
                gauge={
                    "axis": {"range": [-1, 1]},
                    "bar": {"color": "#2ecc71" if polarity > 0.1 else ("#e74c3c" if polarity < -0.1 else "#f39c12")},
                    "steps": [
                        {"range": [-1, -0.1], "color": "#fadbd8"},
                        {"range": [-0.1, 0.1], "color": "#fef9e7"},
                        {"range": [0.1, 1],  "color": "#d5f5e3"},
                    ],
                    "threshold": {"line": {"color": "black", "width": 4}, "thickness": 0.75, "value": polarity},
                },
                title={"text": "Polarity Score"},
            ))
            fig_gauge.update_layout(height=300, margin=dict(t=40, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Save
            new_entry = {
                "id": len(feedbacks) + 1,
                "name": name.strip(),
                "category": category,
                "feedback": feedback_text.strip(),
                "rating": rating,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "sentiment": label,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            feedbacks.append(new_entry)
            save_data(feedbacks)
            st.success(f"✅ Feedback from **{name}** saved successfully!")
            st.balloons()


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — ALL FEEDBACKS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋 All Feedbacks":
    st.title("📋 All Feedbacks")
    st.markdown("Browse, filter, and search all customer feedback entries.")
    st.markdown("---")

    if df.empty:
        st.info("No feedbacks yet.")
    else:
        # Filters
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            sent_filter = st.multiselect("Sentiment", ["Positive", "Neutral", "Negative"], default=["Positive", "Neutral", "Negative"])
        with fc2:
            cat_filter = st.multiselect("Category", df["category"].unique().tolist(), default=df["category"].unique().tolist())
        with fc3:
            search = st.text_input("Search feedback text", placeholder="keyword…")

        filtered = df[
            df["sentiment"].isin(sent_filter) &
            df["category"].isin(cat_filter)
        ]
        if search:
            filtered = filtered[filtered["feedback"].str.contains(search, case=False)]

        st.markdown(f"**{len(filtered)}** feedbacks found")
        st.markdown("---")

        # Cards
        for _, row in filtered.sort_values("timestamp", ascending=False).iterrows():
            color = "#2ecc71" if row["sentiment"] == "Positive" else ("#e74c3c" if row["sentiment"] == "Negative" else "#f39c12")
            emoji = "😊" if row["sentiment"] == "Positive" else ("😞" if row["sentiment"] == "Negative" else "😐")
            with st.container():
                st.markdown(
                    f"""
                    <div style="border-left: 4px solid {color}; padding: 12px 16px; margin-bottom: 12px;
                                background: #f9f9f9; border-radius: 6px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong>{row['name']}</strong>
                            <span style="font-size:12px; color:#888;">{row['timestamp']}</span>
                        </div>
                        <div style="margin: 4px 0; font-size:13px; color:#555;">
                            📂 {row['category']} &nbsp;|&nbsp; {'⭐' * int(row['rating'])} &nbsp;|&nbsp;
                            {emoji} {row['sentiment']} &nbsp;|&nbsp; Polarity: <b>{row['polarity']}</b>
                        </div>
                        <div style="margin-top:6px;">{row['feedback']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Export
        st.markdown("---")
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Filtered CSV",
            data=csv,
            file_name="feedbacks_filtered.csv",
            mime="text/csv",
            use_container_width=True,
        )
