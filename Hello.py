# Hello.py

import streamlit as st
from utils.config_loader import load_config
from utils.authenticator import authenticator
from utils.styling import set_width_style
from utils.translator import translate
from utils.generator import generate_mock_data
from utils.visualization import create_pillar_score_chart, create_overall_score_distribution

# Load the configuration
config = load_config()

def main():
    # Apply custom styling
    set_width_style()

    # Translation selection
    language = st.sidebar.selectbox("Choose Language", ["English", "Hebrew"])
    target_language = "iw" if language == "Hebrew" else "en"

    # Authentication check
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        authenticator(target_language)
        return

    # Display user profile information
    st.sidebar.title(translate("User Profile", target_language))
    user_name = st.session_state.get('user_name', 'ClientX')
    user_job = st.session_state.get('user_job', 'Head of Strategy')
    st.sidebar.write(translate(f"Name: {user_name}", target_language))
    st.sidebar.write(translate(f"Job: {user_job}", target_language))

    # Sidebar for pillar analysis selection
    st.sidebar.header(translate("Pillar Analysis", target_language))
    pillars = config['pillars']['names']
    selected_pillar = st.sidebar.selectbox(
        translate("Select Pillar for In-Depth Analysis", target_language), pillars)

    # Main dashboard overview
    st.title(translate("Startup Analysis Dashboard", target_language))
    st.markdown(translate("Overview of the startup's situation with key metrics and visualization", target_language))

    # Mock data loading
    startup_data = generate_mock_data()

    # Overall score distribution chart
    st.header(translate("Overall Score Distribution", target_language))
    overall_distribution_chart = create_overall_score_distribution(startup_data, pillars)
    st.plotly_chart(overall_distribution_chart)

    # Display analysis or under construction message
    if selected_pillar:
        st.header(translate(f"{selected_pillar} Analysis", target_language))
        under_construction = config['under_construction'].get(selected_pillar, False)
        if under_construction:
            st.warning(translate("This analysis is currently under construction.", target_language))
        else:
            st.info(translate("Analysis details will be displayed here.", target_language))

if __name__ == '__main__':
    main()
