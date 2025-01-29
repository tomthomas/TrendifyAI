import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.ai_analysis import get_ai_summary

def main():
    st.set_page_config(page_title="Trendify AI", layout = "wide")
    st.title("📊 Trendify AI - Data Insight Generator")

    # File uploads
    uploaded_file = st.file_uploader("Upload your data file (csv, txt)", type = ["csv", "txt"])

    if uploaded_file:
        st.success("File uploaded successfully!")
        data = load_data(uploaded_file)

        if isinstance(data,pd.DataFrame):
            st.subheader("Data Preview")
            st.dataframe(data.head())

            if len(data) > 5000:  # Large file warning
                st.warning("⚠️ Large dataset detected! AI processing may take longer.")

        elif isinstance(data, str):
            st.subheader("Text Preview")
            st.write(data[:500] + "....")

        else:
            st.error("Unsupported file format")
            return
    
    if uploaded_file and data is not None:
        with st.spinner("🔍 Detecting trends using AI..."):
            try:
                analysis = get_ai_summary(data)
                st.subheader("AI-Powered Insights")
                st.markdown(f"**Key Trends**:\n{analysis}")
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    main()
