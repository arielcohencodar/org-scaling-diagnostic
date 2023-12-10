import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.config_loader import config
from utils.translator import translate

# Read data from Excel file (assuming a function load_excel_data is defined)
def load_excel_data(file_path, sheet_name='Sheet1'):
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"Error loading Excel data: {e}")
        return pd.DataFrame()

# Assuming the Excel file has columns 'Date', 'Indicator', and 'Value'
def get_data_for_indicator(dataframe, indicator):
    return dataframe[dataframe['Indicator'] == indicator][['Date', 'Value']]

def draw_plot(config, title, target_language, dataframe, detailed=False, threshold=None):
    dates, data = get_data_for_indicator(dataframe, title)

    # Threshold logic
    last_value = data.iloc[-1] if not data.empty else None
    color = "red" if last_value < threshold else "blue" if threshold is not None else "blue"

    # Determine plot type
    indicator_plot_types = config['indicator_plot_types']
    plot_type = indicator_plot_types.get(title, 'line')
    fig = None

    # Plot creation based on type
    if plot_type == 'line':
        fig = go.Figure(go.Scatter(x=dates, y=data, mode='lines+markers', name=title, line=dict(color=color)))
    elif plot_type == 'bar':
        fig = go.Figure(go.Bar(x=dates, y=data, name=title, marker_color=color))
    # Add more plot types as needed

    if fig:
        xaxis_title = translate("Date", target_language) if detailed else translate("Time", target_language)
        yaxis_title = translate("Value", target_language)
        fig.update_layout(
            title=translate(title, target_language),
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            margin=dict(t=20, b=20, l=30, r=30),
            height=150, font=dict(size=10),
            title_font=dict(size=12),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_color='#0038A8')
        fig.update_traces(hovertemplate=translate("<b>Date</b>: %{x}<br><b>Value</b>: %{y}", target_language))
    else:
        # Fallback for unrecognized plot type
        fig = go.Figure()

    return fig
