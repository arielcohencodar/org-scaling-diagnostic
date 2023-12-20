# utils/talent_recruitment_analysis.py

import pandas as pd
import plotly.graph_objects as go

def load_and_preprocess_data(incredibuild_file_path, all_profiles_file_path):
    # Load Incredibuild data
    incredibuild_data = pd.read_csv(incredibuild_file_path, delimiter=';')
    incredibuild_data['start_date'] = pd.to_datetime(incredibuild_data['start_date'], format='%d/%m/%Y', errors='coerce')
    incredibuild_data['end_date'] = pd.to_datetime(incredibuild_data['end_date'], format='%d/%m/%Y', errors='coerce')
    incredibuild_data['end_date'].fillna(pd.Timestamp('2025-01-01'), inplace=True)

    # Load All Profiles data
    all_profiles_data = pd.read_csv(all_profiles_file_path, delimiter=';')
    all_profiles_data['start_date'] = pd.to_datetime(all_profiles_data['start_date'], errors='coerce', dayfirst=True)
    all_profiles_data['end_date'] = pd.to_datetime(all_profiles_data['end_date'], errors='coerce', dayfirst=True)
    all_profiles_data['end_date'].fillna(pd.Timestamp('2025-01-01'), inplace=True)

    return incredibuild_data, all_profiles_data

def compute_attrition(data):
    # Data preprocessing to extract year
    data['Start Year'] = data['start_date'].dt.year
    data['Termination Year'] = data['end_date'].dt.year

    # Compute attrition rates
    years = sorted(data['Start Year'].unique())
    attrition_rates = {}
    for year in years:
        start_count = data[data['Start Year'] <= year].shape[0]
        term_count = data[(data['Termination Year'] == year) & (data['Start Year'] <= year)].shape[0]
        attrition_rates[year] = term_count / start_count if start_count > 0 else 0
    return attrition_rates

def create_attrition_comparison_chart(incredibuild_attrition, all_profiles_attrition):
    fig = go.Figure()
    # Incredibuild data
    fig.add_trace(go.Bar(
        x=list(incredibuild_attrition.keys()),
        y=list(incredibuild_attrition.values()),
        name='Incredibuild',
        marker_color='blue'
    ))
    # All Profiles (Benchmark) data
    fig.add_trace(go.Bar(
        x=list(all_profiles_attrition.keys()),
        y=list(all_profiles_attrition.values()),
        name='Benchmark',
        marker_color='orange'
    ))
    # Update layout
    fig.update_layout(
        title='Attrition Rate Comparison: Incredibuild vs Benchmark',
        xaxis_title='Year',
        yaxis_title='Attrition Rate',
        barmode='group'
    )
    return fig
