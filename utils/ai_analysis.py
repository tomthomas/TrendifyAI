import os
import requests
import pandas as pd

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}

def validate_prompt_length(prompt):
    avg_token_length = 4  # Conservative estimate
    max_tokens = 30000  # Leave 2k tokens for response
    if len(prompt) / avg_token_length > max_tokens:
        raise ValueError("Input too large - please upload smaller dataset")


def generate_insights(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400,
            "temperature": 0.7,
            "truncation": True,
            "return_full_text": False
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
        means_str = ", ".join(f"{col}: {val:.2f}" 
                             for col, val in data.mean(numeric_only=True).items())
        
        stdevs_str = ", ".join(f"{col}: {val:.2f}" 
                              for col, val in data.std(numeric_only=True).items())
        
        top_cats_str = ""
        for col in data.select_dtypes(include="object").columns:
            top_3 = data[col].value_counts().index[:3]
            top_cats_str += f"{col}: {', '.join(top_3)}\n"

        if num_rows <= 10_000:
            sample_data = data.to_csv(index=False)
            sample_size = num_rows
            text_output = "Using the entire dataset for analysis"
        else:
            # For datasets with 10,000+ rows, use just first 10,000 rows
            sample_data = data.head(10_000).to_csv(index=False)
            sample_size = 10_000
            text_output = "Dataset size too large. Using just the first 10,000 rows for analysis."

        prompt = f"""
        You are an expert data analyst. Analyze the dataset with columns: {", ".join(data.columns)}.
        {text_output}
        
        Summary statistics:
        - Means: {means_str}
        - Standard Deviations" {stdevs_str}
        - Top Categories (if applicable): {top_cats_str}
        
        Data used for analysis: {sample_size} rows.
        
        
        Sample Data (first {sample_size} rows):{sample_data}
        
        Identify key insights, trends, and anomalies:
        - Detect patterns in numerical values.
        - Identify outliers or unusual variations.
        - Summarize how key metrics change over time.
        - If categories exist, highlight which perform best or worst.
        - Present findings in a clear, structured format.
        """
    else:
        max_text_length = 25000  # Leave room for prompt
        truncated_text = str(data)[:max_text_length]

        prompt = f"""
        You are an expert content analyst. Analyze the following text and extract key insights, including numerical analysis where possible:
        
        {truncated_text}...
        
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
