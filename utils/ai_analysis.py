import os
import requests
import pandas as pd

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
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
        sample_data = data.head(10).to_dict()
        prompt = f"""Analyze this data with columns {list(data.columns)}.
        Sample rows: {sample_data}.
        Identify 3 key trends in bullet points:"""
    else:
        prompt = f"""Summarize this text and find the main themes: {str(data)[:2000]}..."""

    return generate_insights(prompt)