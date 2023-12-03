import plotly.graph_objects as go
import plotly.express as px
from utils.data_generator import generate_data, generate_reservist_data
from utils.config_loader import config
from utils.translator import translate

indicator_plot_types = config['indicator_plot_types']

def draw_plot(title, target_language, detailed=False, threshold=None):
    dates, data = generate_data(indicator=title)

   # Use only the last element of data for the threshold comparison
    last_value = data[-1] if len(data) > 0 else None

    # Check if the threshold is set and determine color
    if threshold is not None and last_value is not None:
        color = "red" if data[-1] < threshold else "blue"
    else:
        color = "blue"  # Default color

    # Slice the data to display only the last 12 weeks
    if not detailed:
        last_24_weeks_index = -24  # Index for the last 12 weeks
        dates = dates[last_24_weeks_index:]
        data = data[last_24_weeks_index:]

    # Determine the type of plot from the configuration
    plot_type = indicator_plot_types.get(title, 'line')  # Default to line plot if not specified

    """# Define color based on the indicator name
    if title in ["Default among developers, contractors", 
                 "Construction work visa application", 
                 "Percentage of foreign labor", 
                 "Days on market",
                 "Home Price Index"]:
        color = "red"
    elif title in ["Companies applied for chapter 11", 
                   "Level of wages by occupation",
                   "Building Permits Issued"]:
        color = "orange"
    else:
        color = "blue"  # Default color"""

    # Initialize fig to None
    fig = None

    # Create the appropriate plot based on the plot type
    if plot_type == 'line':
        fig = go.Figure(go.Scatter(x=dates, y=data, mode='lines+markers', name=title, line=dict(color=color)))
    elif plot_type == 'bar':
        fig = go.Figure(go.Bar(x=dates, y=data, name=title, marker_color=color))
    elif plot_type == 'area':
        fig = go.Figure(go.Scatter(x=dates, y=data, fill='tozeroy', name=title, line=dict(color=color)))
    # Add more plot types if needed

    # Default case if plot_type is not recognized
    if fig is None:
        fig = go.Figure(go.Scatter(x=dates, y=data, mode='lines+markers', name=title, line=dict(color=color)))

    # Translating axis titles
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
    
    # Update hover template to show translated labels
    fig.update_traces(
        hovertemplate=translate("<b>Date</b>: %{x}<br><b>Value</b>: %{y}", target_language)
    )

    return fig

def draw_pie_chart(target_language):
    """
    Draw a pie chart from the given data.
    :param data: A dictionary of data to be displayed in the pie chart
    :return: A plotly pie chart
    """
    data = generate_reservist_data()
    labels = list(data.keys())
    values = list(data.values())

    fig = go.Figure(data=[go.Pie(labels=[translate(label, target_language) for label in labels], values=values, hole=.3)])

    # Set the dimensions of the pie chart
    fig.update_layout(width=800, height=400)  # You can adjust these values as needed

    return fig

def draw_map(indicator, target_language):
    latitudes, longitudes = generate_data(indicator)
    data = {'lat': latitudes, 'lon': longitudes}
    fig = px.scatter_geo(data,
                         lat='lat',
                         lon='lon',
                         projection="natural earth",
                         title=translate("Map of Construction Sites in Israel", target_language))
    return fig
