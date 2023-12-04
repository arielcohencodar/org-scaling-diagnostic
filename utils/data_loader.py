import pandas as pd

# Function to load data
file_path = './data/business_analysis_data.xlsx'  # Update with the actual path

def get_sheet_names():
    excel_data = pd.ExcelFile(file_path)
    return excel_data.sheet_names

def load_data(sheet_name):
    return pd.read_excel(file_path, sheet_name)
