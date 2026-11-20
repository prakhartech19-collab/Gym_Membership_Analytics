"""
Interactive Streamlit Dashboard: Gym & Fitness Center Membership Analytics
========================================================================
Interactive operational dashboard allowing facility managers and retention
teams to filter check-in patterns, inspect peak congestion, analyze tier
performance, and identify at-risk low-engagement members.

Run with:
    streamlit run dashboard.py
"""

import os
import tempfile
from pathlib import Path

# Ensure Matplotlib config dir is writable on Windows
os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

try:
    import streamlit as st
except ImportError:
    st = None


def main():
    if st is None:
        print("Streamlit is not installed in the active environment.")
        print("To run the interactive dashboard, install streamlit: pip install streamlit")
        print("Then run: streamlit run dashboard.py")
        return

    st.set_page_config(
        page_title="Gym Membership Analytics",
        page_icon="🏋️‍♂️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🏋️‍♂️ Gym & Fitness Center Membership Analytics")
    st.markdown("### Operational Intelligence, Utilization Patterns & Retention Dashboard")

    # Locate dataset
    base_dir = Path(__file__).resolve().parent
    cleaned_csv_path = base_dir / "outputs" / "cleaned_12_gym_membership.csv"
    raw_csv_path = base_dir / "12_gym_membership.csv"

    if cleaned_csv_path.exists():
        df = pd.read_csv(cleaned_csv_path)
    elif raw_csv_path.exists():
        df = pd.read_csv(raw_csv_path)
        df = df.drop_duplicates(subset=["Checkin_ID"], keep="first")
        df["Workout_Duration_Mins"] = df["Workout_Duration_Mins"].fillna(
            df.groupby("Membership_Tier")["Workout_Duration_Mins"].transform("median")
        )
        df["Checkin_Time"] = pd.to_datetime(df["Checkin_Time"])
        df["Weekday"] = df["Checkin_Time"].dt.day_name()
        df["Visit_Hour"] = df["Checkin_Time"].dt.hour
    else:
        st.error("Dataset not found. Please run gym_analytics.py first.")
        return

    df["Checkin_Time"] = pd.to_datetime(df["Checkin_Time"])

    # Sidebar Filters
    st.sidebar.header("🔍 Analytical Filters")
    
    tier_options = ["All"] + sorted(list(df["Membership_Tier"].dropna().unique()))
    selected_tier = st.sidebar.selectbox("Membership Tier", tier_options)

    gender_options = ["All"] + sorted(list(df["Gender"].dropna().unique()))
    selected_gender = st.sidebar.selectbox("Member Gender", gender_options)

    day_options = ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected_day = st.sidebar.selectbox("Day of Week", day_options)

    # Filter data
    filtered_df = df.copy()
    if selected_tier != "All":
        filtered_df = filtered_df[filtered_df["Membership_Tier"] == selected_tier]
    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]
    if selected_day != "All":
        filtered_df = filtered_df[filtered_df["Weekday"] == selected_day]

    # Core Metrics
    total_checkins = len(filtered_df)
    unique_members = filtered_df["Member_ID"].nunique()
    avg_duration = filtered_df["Workout_Duration_Mins"].mean() if total_checkins > 0 else 0
    median_duration = filtered_df["Workout_Duration_Mins"].median() if total_checkins > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Valid Check-Ins", f"{total_checkins:,}")
    col2.metric("Unique Active Members", f"{unique_members:,}")
    col3.metric("Avg Workout Duration", f"{avg_duration:.1f} mins")
    col4.metric("Median Workout Duration", f"{median_duration:.1f} mins")

    st.markdown("---")

    # Tabs for analytics
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⏰ Peak Hours & Congestion",
        "🎯 Class Popularity",
        "📊 Tier Breakdown",
        "⚠️ Retention & Inactivity",
        "📋 Data Explorer"
    ])

    with tab1:
        st.subheader("Hourly & Weekly Check-In Congestion")
        if total_checkins > 0:
            day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            available_days = [d for d in day_order if d in filtered_df["Weekday"].unique()]
            if available_days:
                pivot = filtered_df.pivot_table(
                    index="Weekday", columns="Visit_Hour", values="Checkin_ID", aggfunc="count", fill_value=0
                ).reindex(available_days)
                
                fig, ax = plt.subplots(figsize=(12, 4))
                sns.heatmap(pivot, cmap="YlOrRd", annot=True, fmt="d", cbar=True, ax=ax)
                ax.set_title("Check-In Density Heatmap (Weekday vs. 24h Clock)", fontsize=12, fontweight="bold")
                ax.set_xlabel("Hour of Day (24h)")
                ax.set_ylabel("Day of Week")
                st.pyplot(fig)
                plt.close()

    with tab2:
        st.subheader("Fitness Class & Studio Attendance")
        if total_checkins > 0:
            class_df = filtered_df.copy()
            class_df["Fitness_Class"] = class_df["Fitness_Class"].fillna("Open Gym (No Class)")
            class_counts = class_df["Fitness_Class"].value_counts()
            
            fig, ax = plt.subplots(figsize=(8, 4))
            palette = sns.color_palette("viridis", len(class_counts))
            bars = ax.bar(class_counts.index, class_counts.values, color=palette, edgecolor="black")
            ax.set_title("Attendance Ranking by Fitness Class", fontsize=12, fontweight="bold")
            ax.set_xlabel("Class / Activity")
            ax.set_ylabel("Total Attendance")
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., h + 1, f"{int(h)}", ha="center", va="bottom", fontsize=9)
            plt.xticks(rotation=15)
            st.pyplot(fig)
            plt.close()

    with tab3:
        st.subheader("Workout Duration Spread by Membership Tier")
        if total_checkins > 0:
            tier_order = ["Basic", "Gold", "Platinum"]
            available_tiers = [t for t in tier_order if t in filtered_df["Membership_Tier"].unique()]
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.boxplot(
                data=filtered_df,
                x="Membership_Tier",
                y="Workout_Duration_Mins",
                hue="Membership_Tier",
                order=available_tiers,
                palette="Set2",
                legend=False,
                ax=ax
            )
            ax.set_title("Workout Duration Distribution by Tier", fontsize=12, fontweight="bold")
            ax.set_xlabel("Membership Tier")
            ax.set_ylabel("Duration (Mins)")
            st.pyplot(fig)
            plt.close()

    with tab4:
        st.subheader("Low-Engagement & Inactivity Monitoring (<2 visits/month)")
        max_date = df["Checkin_Time"].max()
        member_stats = df.groupby("Member_ID").agg(
            Membership_Tier=("Membership_Tier", "last"),
            Monthly_Fee=("Monthly_Fee", "last"),
            Total_Visits=("Checkin_ID", "count"),
            First_Checkin=("Checkin_Time", "min"),
            Last_Checkin=("Checkin_Time", "max")
        ).reset_index()
        months_span = df["Checkin_Time"].dt.to_period("M").nunique()
        member_stats["Avg_Monthly_Visits"] = (member_stats["Total_Visits"] / months_span).round(2)
        member_stats["Days_Since_Last_Visit"] = (max_date - member_stats["Last_Checkin"]).dt.days
        member_stats["Engagement_Status"] = np.where(
            member_stats["Avg_Monthly_Visits"] < 2.0, "At-Risk / Low-Engagement", "Engaged / Regular"
        )
        
        st.dataframe(
            member_stats.sort_values(by="Days_Since_Last_Visit", ascending=False),
            use_container_width=True
        )

    with tab5:
        st.subheader("Filtered Check-In Records Explorer")
        st.dataframe(filtered_df, use_container_width=True)
        st.download_button(
            "📥 Download Filtered Data as CSV",
            data=filtered_df.to_csv(index=False),
            file_name="filtered_gym_checkins.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
