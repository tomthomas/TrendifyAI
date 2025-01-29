import pandas as pd

def load_data(uploaded_file):
    """Handle different data types"""
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.txt'):
            return uploaded_file.read().decode()
        else:
            return None
    except Exception as e:
        raise ValueError(f"Error loading file: {str(e)}")
    