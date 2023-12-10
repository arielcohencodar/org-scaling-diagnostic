# utils/visualization.py

import pandas as pd
import plotly.express as px

def create_pillar_score_chart(data, pillar):
    """
    Creates an interactive bar chart for the scores of a given pillar.

    Parameters:
    data (DataFrame): A pandas DataFrame containing the data to be visualized.
    pillar (str): The name of the pillar to visualize.

    Returns:
    Figure: A Plotly bar chart figure.
    """
    # Filter data for the selected pillar
    filtered_data = data[['Startup ID', pillar]]

    # Create the bar chart
    fig = px.bar(
        filtered_data,
        x='Startup ID',
        y=pillar,
        title=f'{pillar} Scores for Startups',
        labels={'Startup ID': 'Startup ID', pillar: 'Score'},
        color=pillar,  # Color the bars by score
        color_continuous_scale=px.colors.sequential.Viridis  # A color scale for the bars
    )

    # Improve layout
    fig.update_layout(
        xaxis_title='Startup ID',
        yaxis_title='Score',
        coloraxis_showscale=False  # Hide the color scale if not needed
    )

    return fig

def create_overall_score_distribution(data, pillars):
    """
    Creates an interactive histogram to visualize the overall score distribution.

    Parameters:
    data (DataFrame): A pandas DataFrame containing the data to be visualized.
    pillars (list): A list of the pillars to include in the overall score.

    Returns:
    Figure: A Plotly histogram figure.
    """
    # Calculate the overall score by averaging the scores across the specified pillars
    data['Overall Score'] = data[pillars].mean(axis=1)

    # Create the histogram
    fig = px.histogram(
        data,
        x='Overall Score',
        nbins=20,
        title='Overall Score Distribution',
        labels={'Overall Score': 'Overall Score'}
    )

    # Improve layout
    fig.update_layout(
        xaxis_title='Overall Score',
        yaxis_title='Count of Startups'
    )

    return fig

# You can add more visualization functions as needed
