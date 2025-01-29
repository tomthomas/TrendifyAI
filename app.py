import streamlit as st
import pandas as pd
from utils.data_loader import load_data

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

        elif isinstance(data, str):
            st.subheader("Text Preview")
            st.write(data[:500] + "....")

        else:
            st.error("Unsupported file format")


if __name__ == "__main__":
    main()
