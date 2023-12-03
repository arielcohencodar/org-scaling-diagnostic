# utils/dashboard_functions.py
import streamlit as st
from utils.visualizer import draw_plot, draw_pie_chart, draw_map
from utils.metrics import display_deviation_metric
from utils.data_generator import generate_data
from utils.translator import translate

# Define filter options
GEOGRAPHY_OPTIONS = ["All", "Central district", "South district", "North district"]
DEMOGRAPHY_OPTIONS = ["All", "Haredi", "Secular"]
BUSINESS_SIZE_OPTIONS = ["All", "SMBs", "Large enterprises"]

def show_main_dashboard(selected_industry,
                        selected_industry_indicators,
                        selected_shared_indicators,
                        indicators_grouped,
                        target_language
                        ):
    """
    Display the main dashboard with the default indicators and any additional indicators specific to the selected industry.
    
    :param selected_industry: The industry chosen by the user
    :param selected_industry_indicators: Additional industry-specific indicators chosen by the user
    :param selected_shared_indicators: Additional shared indicators chosen by the user
    :param indicators_grouped: The dictionary of default indicators grouped by industry
    """
    st.title(translate(f"Dashboard for {selected_industry}", target_language))

    # Filters title
    st.sidebar.title(translate("Filters", target_language))

    # Set filters for the dashboard view
    selected_geography = st.sidebar.selectbox(translate("Geography", target_language), GEOGRAPHY_OPTIONS, index=0)
    selected_demography = st.sidebar.selectbox(translate("Demography", target_language), DEMOGRAPHY_OPTIONS, index=0)
    selected_business_size = st.sidebar.selectbox(translate("Business Size", target_language), BUSINESS_SIZE_OPTIONS, index=0)

    # Combine default indicators with selected industry-specific and shared indicators
    default_indicators = []
    if selected_industry in indicators_grouped:
        for group in indicators_grouped[selected_industry].values():
            default_indicators.extend(group)
    all_selected_indicators = default_indicators + selected_industry_indicators + selected_shared_indicators

    # Initialize a dictionary in the session state to track the display state of indicators
    if 'display_states' not in st.session_state:
        st.session_state['display_states'] = {indicator: 'graph' for indicator in all_selected_indicators}

    # Create rows of indicators, with up to 3 indicators per row
    for i in range(0, len(all_selected_indicators), 3):
        cols = st.columns(3)  # Create 3 columns
        for j, col in enumerate(cols):
            if i + j < len(all_selected_indicators):
                indicator = all_selected_indicators[i + j]
                with col:
                    # Check if the indicator is "Percentage of Reservists per Industry"
                    if indicator == translate("Percentage of Reservists per Industry", target_language):
                        fig = draw_pie_chart(target_language)
                        st.plotly_chart(fig, use_container_width=True)
                    elif indicator == translate("Map of Construction Sites", target_language):
                        construction_sites_df = generate_data(indicator)
                        st.map(construction_sites_df)
                    else:
                        # Add a number input for setting the threshold
                        threshold = st.number_input(translate(f"Set threshold for {indicator}", target_language), key=f"threshold_{indicator}")

                        # Redraw the plot with the new threshold
                        fig = draw_plot(indicator, target_language, threshold=threshold)
                        st.plotly_chart(fig, use_container_width=True)
                        with st.expander(translate(f"Show more about {indicator}", target_language)):
                            avg_diff_checkbox = st.checkbox(translate(f"Show average difference for {indicator}", translate), key=f"avg_diff_{indicator}")
                            pct_diff_checkbox = st.checkbox(translate(f"Show percentage difference for {indicator}", target_language), key=f"pct_diff_{indicator}")
                            if avg_diff_checkbox or pct_diff_checkbox:
                                display_deviation_metric(indicator, avg_diff_checkbox, pct_diff_checkbox)

def display_detailed_view(target_language):
    """
    Display the detailed view for a selected metric.
    """
    detailed_metric = st.session_state.get('detailed_metric_name', '')
    display_deviation_metric(detailed_metric)
    st.plotly_chart(draw_plot(detailed_metric, target_language, detailed=True, threshold=None), use_container_width=True)

    # Button to return to the main dashboard
    if st.button(translate('Go back to dashboard', target_language), key='back_dashboard'):
        st.session_state['view_detailed_metric'] = False
        st.experimental_rerun()
