import gradio as gr
import pandas as pd
from utils.data_loader import load_data
from utils.ai_analysis import get_ai_summary

def process_file(uploaded_file):
    """
    Processes the uploaded file and returns a data preview and AI-generated insights.
    """
    if uploaded_file is None:
        return "Please upload a file.", None

    try:
        # Load data from the uploaded file
        data = load_data(uploaded_file)

        # Generate a preview of the data
        if isinstance(data, pd.DataFrame):
            preview = data.head().to_html()
        elif isinstance(data, str):
            preview = data[:500] + "..."
        else:
            return "Unsupported file format.", None

        # Get AI-powered insights
        analysis = get_ai_summary(data)
        return preview, analysis

    except Exception as e:
        return f"An error occurred: {str(e)}", None

# Create the Gradio interface
iface = gr.Interface(
    fn=process_file,
    inputs=gr.File(label="Upload your data file (.csv, .txt)"),
    outputs=[
        gr.HTML(label="Data Preview"),
        gr.Markdown(label="AI-Powered Insights")
    ],
    title="📊 Trendify AI - Data Insight Generator",
    description="Upload your financial data to generate trends, forecasts, and key analysis."
)

if __name__ == "__main__":
    iface.launch()
