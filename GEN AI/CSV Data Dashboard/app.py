import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
st.set_page_config(page_title="AI CSV Dashboard", layout="wide")

# Optional CSS to maximize layout
st.markdown("""
    <style>
        .main .block-container {
            max-width: 100% !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 CSV Data Dashboard")

uploaded_file = st.file_uploader("📂 Upload your CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # --- KPIs
    st.subheader("📌 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", len(df))
    col2.metric("Missing Values", df.isnull().sum().sum())
    col3.metric("Avg Unique Values", round(df.nunique().mean(), 2))

    # --- Column detection
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    datetime_cols = []

    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
            datetime_cols.append(col)
        except:
            pass

    # --- Date Range Filter
    if datetime_cols:
        st.subheader("📅 Date Range Filter")
        date_col = st.selectbox("Select datetime column", datetime_cols)
        min_date = df[date_col].min()
        max_date = df[date_col].max()
        start, end = st.date_input("Filter by Date Range", [min_date, max_date])
        df = df[(df[date_col] >= pd.to_datetime(start)) & (df[date_col] <= pd.to_datetime(end))]

    # --- Visualization
    st.subheader("📊 Visualizations")
    chart_type = st.selectbox("Chart Type", ["Histogram", "Bar", "Scatter", "Boxplot", "Time Series Line"])

    if chart_type == "Histogram" and numeric_cols:
        col = st.selectbox("Choose column", numeric_cols)
        fig = px.histogram(df, x=col)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar" and categorical_cols:
        col = st.selectbox("Choose column", categorical_cols)
        bar_data = df[col].value_counts().reset_index()
        bar_data.columns = [col, "count"]
        fig = px.bar(bar_data, x=col, y="count")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter" and len(numeric_cols) >= 2:
        x = st.selectbox("X-axis", numeric_cols)
        y = st.selectbox("Y-axis", [col for col in numeric_cols if col != x])
        fig = px.scatter(df, x=x, y=y)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Boxplot" and numeric_cols and categorical_cols:
        num = st.selectbox("Numeric column", numeric_cols)
        cat = st.selectbox("Category column", categorical_cols)
        fig = px.box(df, x=cat, y=num)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Time Series Line" and datetime_cols and numeric_cols:
        dt_col = st.selectbox("Datetime column", datetime_cols)
        val_col = st.selectbox("Value column", numeric_cols)
        filtered_df = df[[dt_col, val_col]].dropna().sort_values(dt_col)
        fig = px.line(filtered_df, x=dt_col, y=val_col)
        st.plotly_chart(fig, use_container_width=True)

    # --- Correlation Heatmap
    if len(numeric_cols) >= 2:
        st.subheader("📉 Correlation Heatmap")
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    # --- Column-Specific Summary
    st.subheader("🔍 Column Summary")
    selected_col = st.selectbox("Choose a column to analyze", df.columns)
    if selected_col:
        st.write(f"**Column Type:** {df[selected_col].dtype}")
        st.write(f"**Missing Values:** {df[selected_col].isnull().sum()}")
        st.write(f"**Unique Values:** {df[selected_col].nunique()}")
        if df[selected_col].dtype in ['int64', 'float64']:
            st.write(df[selected_col].describe())
        else:
            st.write(df[selected_col].value_counts().head(10))

    # --- Export filtered data
    st.subheader("⬇ Export Filtered Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")
