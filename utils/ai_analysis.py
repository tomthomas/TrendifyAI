import os
import requests
import pandas as pd

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B"
HEADERS = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}

def generate_insights(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 400,
            "temperature": 0.7
        }
    }

    response = requests.post(API_URL, headers= HEADERS, json= payload)
    
    # check if request was succesfull
    if response.status_code != 200:
        raise ValueError(f"API request failed: {response.text}")
    
    result = response.json()
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]['generated_text']
    
    raise ValueError(f"Unexpected API response: {result}")

def get_ai_summary(data):
    if isinstance(data, pd.DataFrame):
        num_rows = len(data)

        # summary statistics
        summary_stats = {
            "column_means": data.mean(numeric_only=True).to_dict(),
            "column_stdev": data.std(numeric_only=True).to_dict(),
            "top_categories": {col: data[col].value_counts().nlargest(3).to_dict()
                               for col in data.select_dtypes(include=["object"]).columns}
        
        }

        if num_rows <= 10_000:
            sample_data = data.to_dict()
            sample_size = num_rows
            text_output = "Using the entire dataset for analysis"
        else:
            # For datasets with 10,000+ rows, use just first 10,000 rows
            sample_data = data.head(10_000).to_dict()
            sample_size = 10_000
            text_output = "Dataset size too large. Using just the first 10,000 rows for analysis."

        prompt = f"""
        You are an expert data analyst. Analyze the dataset with columns {list(data.columns)}.
        {text_output}
        
        Summary statistics:
        - Means: {summary_stats['column_means']}
        - Standard Deviations" {summary_stats['column_stdev']}
        - Top Categories (if applicable): {summary_stats['top_categories']}
        
        Data used for analysis: {sample_size} rows.
        
        
        {sample_data}
        
        Identify key insights, trends, and anomalies:
        - Detect patterns in numerical values.
        - Identify outliers or unusual variations.
        - Summarize how key metrics change over time.
        - If categories exist, highlight which perform best or worst.
        - Present findings in a clear, structured format.
        """
    else:
        prompt = f"""
        You are an expert content analyst. Analyze the following text and extract key insights, including numerical analysis where possible:
        
        {str(data)[:2000]}...
        
        - Identify the main themes or topics.
        - Highlight any patterns or recurring keywords.
        - Extract and analyze any numerical data (percentages, averages, trends, etc.).
        - Identify any trends, outliers, or anomalies in the numbers.
        - Detect any relationships between numerical figures and other data points (e.g., correlations between sales and dates).
        - List important entities (e.g., dates, places, people, or events) mentioned in the text.
        - Summarize any actionable insights or conclusions that can be drawn from the content.
        - If the text relates to a specific topic (e.g., business, science, technology), highlight the relevant points.

        Provide a clear summary of your findings, including both **textual insights** and **numerical analysis**.
        """

    return generate_insights(prompt)