# utils/talent_recruitment_analysis.py

import pandas as pd
import plotly.graph_objects as go

def load_and_preprocess_data(incredibuild_file_path, all_profiles_file_path):
    # Load and preprocess Incredibuild data
    incredibuild_data = pd.read_csv(incredibuild_file_path, delimiter=';')
    incredibuild_data['start_date'] = pd.to_datetime(incredibuild_data['start_date'], format='%d/%m/%Y', errors='coerce')
    incredibuild_data['end_date'] = pd.to_datetime(incredibuild_data['end_date'], format='%d/%m/%Y', errors='coerce')
    incredibuild_data['end_date'].fillna(pd.Timestamp('2025-01-01'), inplace=True)

    # Load and preprocess All Profiles data
    all_profiles_data = pd.read_csv(all_profiles_file_path, delimiter=';')
    all_profiles_data['start_date'] = pd.to_datetime(all_profiles_data['start_date'], errors='coerce', dayfirst=True)
    all_profiles_data['end_date'] = pd.to_datetime(all_profiles_data['end_date'], errors='coerce', dayfirst=True)
    all_profiles_data['end_date'].fillna(pd.Timestamp('2025-01-01'), inplace=True)

    return incredibuild_data, all_profiles_data

def compute_attrition_and_headcount(data):
    data['Start Year'] = data['start_date'].dt.year
    data['Termination Year'] = data['end_date'].dt.year
    years = sorted(data['Start Year'].unique())
    attrition_rates = {}
    headcounts = {}

    for year in years:
        start_count = data[data['Start Year'] <= year].shape[0]
        term_count = data[(data['Termination Year'] == year) & (data['Start Year'] <= year)].shape[0]
        attrition_rates[year] = term_count / start_count if start_count > 0 else 0
        headcounts[year] = start_count

    return attrition_rates, headcounts

def create_comparison_chart(data_incredibuild, data_benchmark, title, yaxis_title):
    fig = go.Figure()
    for label, data in [("Incredibuild", data_incredibuild), ("Benchmark", data_benchmark)]:
        fig.add_trace(go.Bar(
            x=list(data.keys()),
            y=list(data.values()),
            name=label
        ))

    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title=yaxis_title,
        barmode='group'
    )
    return fig

def compute_function_wise_attrition(data):
    functions = data['odp_function'].unique()
    function_wise_attrition = {}
    for function in functions:
        function_data = data[data['odp_function'] == function]
        function_attrition_rates, _ = compute_attrition_and_headcount(function_data)
        function_wise_attrition[function] = function_attrition_rates
    return function_wise_attrition

def create_function_wise_chart(function_wise_attrition, title):
    fig = go.Figure()
    for function, attrition in function_wise_attrition.items():
        fig.add_trace(go.Scatter(
            x=list(attrition.keys()),
            y=list(attrition.values()),
            mode='lines+markers',
            name=function
        ))

    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title='Attrition Rate',
        legend_title='Function'
    )
    return fig
