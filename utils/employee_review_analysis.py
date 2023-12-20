# utils/employee_review_analysis.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import openai
from openai import OpenAI

# Assuming 'client' is an OpenAI client instance for GPT-4 communication

openai.api_key = st.secrets['openai_api_key']
client = OpenAI(api_key=openai.api_key)  # Initialize the OpenAI client

def load_review_data(file_path):
    """
    Load and preprocess employee review data from an Excel file.
    """
    df = pd.read_excel(file_path)
    df['Rating'] = pd.to_numeric(df['Rating'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month_Year'] = df['Date'].dt.to_period('M')
    return df

def get_basic_statistics(df):
    """
    Return basic statistics of the reviews DataFrame.
    """
    return df.describe()

def get_data_quality_info(df):
    """
    Return data quality information of the reviews DataFrame.
    """
    return df.info()

def get_number_of_reviews_and_date_range(df):
    """
    Return the number of reviews and the date range of the reviews DataFrame.
    """
    return df.shape[0], df['Date'].min(), df['Date'].max()

def get_average_rating(df):
    """
    Return the average rating of the reviews DataFrame.
    """
    return df['Rating'].mean()

def create_rating_distribution_chart(df):
    """
    Create and return a Plotly chart for the distribution of ratings.
    """
    fig = px.histogram(df, x='Rating', nbins=30, title='Distribution of Ratings')
    fig.update_layout(bargap=0.1)
    return fig

def create_score_over_time_charts(df, score_columns):
    """
    Create and return a list of Plotly charts for each score category over time.
    """
    charts = []
    for column in score_columns:
        # Group by 'Month_Year' and calculate the mean, ignoring NaN values
        monthly_scores = df.groupby('Month_Year')[column].mean()

        # Calculate the cumulative average
        cumulative_avg = monthly_scores.expanding().mean()

        # Resample to fill missing months with the last known cumulative average
        cumulative_avg_filled = cumulative_avg.resample('M').ffill()

        # Create the figure
        fig = go.Figure(data=go.Scatter(x=cumulative_avg_filled.index.astype(str), y=cumulative_avg_filled.values, mode='lines', name='Cumulative Average'))

        # Update layout
        fig.update_layout(title=f'Cumulative Average of {column} Over Time', xaxis_title='Month and Year', yaxis_title=f'Cumulative Average {column} Score')

        charts.append(fig)
    return charts

# Additional functions for other visualizations and analyses...

def get_model_response(messages, model='gpt-4', temperature=0.5, max_tokens=500):
    """
    Get a model response from OpenAI's GPT-4.
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1
    )
    interpretation = next((choice.message.content for choice in response.choices if choice.message.role == 'assistant'), '')
    return interpretation

# Function to generate detailed analysis using GPT-4
def generate_detailed_analysis(df, analysis_topics):
    """
    Generate a detailed analysis of the reviews DataFrame using GPT-4.
    """
    concatenated_reviews = ' '.join(df['Pros'] + ' ' + df['Cons'])
    prompt_text = f"Analyze these employee reviews and provide detailed insights on the following topics: {', '.join(analysis_topics)}: {concatenated_reviews}"
    analysis_messages = [
        {'role': 'system', 'content': 'You are a helpful assistant that analyzes text sentiment and content.'},
        {'role': 'user', 'content': prompt_text}
    ]
    return get_model_response(analysis_messages)
