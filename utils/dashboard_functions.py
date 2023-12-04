# utils/dashboard_functions.py
import streamlit as st
from utils.visualizer import draw_plot, load_excel_data
from utils.translator import translate

excel_data_path = './data/business_analysis_data.xlsx'

def show_main_dashboard(selected_startup, selected_indicators, target_language):
    st.title(translate(f"Dashboard for {selected_startup}", target_language))

    dataframe = load_excel_data(excel_data_path)  # Load Excel data

    if 'display_states' not in st.session_state:
        st.session_state['display_states'] = {indicator: 'graph' for indicator in selected_indicators}

    for i in range(0, len(selected_indicators), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(selected_indicators):
                indicator = selected_indicators[i + j]
                with col:
                    threshold = st.number_input(translate(f"Set threshold for {indicator}", target_language), key=f"threshold_{indicator}")
                    fig = draw_plot(indicator, target_language, dataframe, threshold=threshold)
                    st.plotly_chart(fig, use_container_width=True)
