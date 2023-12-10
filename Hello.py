import streamlit as st

# Modularized imports
from utils.authenticator import authenticator
from utils.styling import set_width_style
from utils.translator import translate
from utils.generator import generate_mock_data
from utils.visualization import create_pillar_score_chart, create_overall_score_distribution

# Main file of the Streamlit app

def main():
    # Styling
    set_width_style()

    # Translation
    language = st.sidebar.selectbox("Choose Language", ["English", "Hebrew"])
    target_language = "iw" if language == "Hebrew" else "en"

    # Check for user authentication
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        authenticator(target_language)
        return
    
    # Add user profile in sidebar
    with st.sidebar:
        st.title(translate("User Profile", target_language))
        # Dynamic user information
        user_name = st.session_state.get('user_name', 'ClientX')
        user_job = st.session_state.get('user_job', 'Head of Strategy')
        st.write(translate(f"Name: {user_name}", target_language))
        st.write(translate(f"Job: {user_job}", target_language))

    # Initialize scenario mode active state if it doesn't exist
    if 'scenario_mode_active' not in st.session_state:
        st.session_state['scenario_mode_active'] = False

    mode = st.sidebar.radio(
        translate("Mode", target_language),
        [
            translate("Standard", target_language),
            translate("Review Insight", target_language),
            translate("Advanced Analytics", target_language)
        ]
    )

    # Main page overview with key metrics and visualization
    st.title(translate("Startup Analysis Dashboard", target_language))
    st.markdown(translate("Overview of the startup's situation with key metrics and visualization", target_language))

    # Load mock data for development purposes
    startup_data = generate_mock_data()

    # Display overall score distribution
    st.header(translate("Overall Score Distribution", target_language))
    pillars = ['Market Fit', 'Team', 'Product', 'Growth Strategy', 'Financials']  # Define your actual pillars here
    overall_distribution_chart = create_overall_score_distribution(startup_data, pillars)
    st.plotly_chart(overall_distribution_chart)

    # Pillar analysis section
    st.header(translate("Pillar Analysis", target_language))
    selected_pillar = st.selectbox(translate("Choose Pillar", target_language), pillars)
    pillar_chart = create_pillar_score_chart(startup_data, selected_pillar)
    st.plotly_chart(pillar_chart)

if __name__ == '__main__':
    main()
