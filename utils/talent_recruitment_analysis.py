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

def compute_headcount(data):
    # Compute headcount data
    years = sorted(data['Start Year'].unique())
    headcounts = {}
    for year in years:
        headcount = data[data['Start Year'] <= year].shape[0]
        headcounts[year] = headcount
    return headcounts

def create_headcount_comparison_chart(incredibuild_headcount, all_profiles_headcount):
    fig = go.Figure()
    # Incredibuild data
    fig.add_trace(go.Bar(
        x=list(incredibuild_headcount.keys()),
        y=list(incredibuild_headcount.values()),
        name='Incredibuild',
        marker_color='blue'
    ))
    # All Profiles (Benchmark) data
    fig.add_trace(go.Bar(
        x=list(all_profiles_headcount.keys()),
        y=list(all_profiles_headcount.values()),
        name='Benchmark',
        marker_color='orange'
    ))
    # Update layout
    fig.update_layout(
        title='Headcount Comparison: Incredibuild vs Benchmark',
        xaxis_title='Year',
        yaxis_title='Headcount',
        barmode='group'
    )
    return fig

def compute_attrition_by_function(data):
    # Compute attrition rates by function
    functions = data['odp_function'].unique()
    function_attrition = {function: compute_attrition(data[data['odp_function'] == function]) for function in functions}
    return function_attrition

def create_function_attrition_chart(function_attrition_data, title):
    fig = go.Figure()
    for function, attrition in function_attrition_data.items():
        fig.add_trace(go.Scatter(
            x=list(attrition.keys()),
            y=list(attrition.values()),
            mode='lines+markers',
            name=function
        ))
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title='Attrition Rate',
        legend_title='Function'
    )
    return fig