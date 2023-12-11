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
    st.sidebar.title(translate("User Profile", target_language))
    # Dynamic user information
    user_name = st.session_state.get('user_name', 'ClientX')
    user_job = st.session_state.get('user_job', 'Head of Strategy')
    st.sidebar.write(translate(f"Name: {user_name}", target_language))
    st.sidebar.write(translate(f"Job: {user_job}", target_language))

    # Pillar analysis drill-down in sidebar
    st.sidebar.header(translate("Pillar Analysis", target_language))
    pillars = [
        'Market Fit', 
        'Team', 
        'Product', 
        'Growth Strategy', 
        'Financials',
        'Customer Satisfaction',
        'Operational Efficiency',
        'Technical Scalability',
        'Regulatory Compliance',
        'Innovation',
        'Funding',
        'Market Reach',
        'Customer Acquisition',
        'Brand Strength',
        'Strategic Positioning',
        'Risk Management',
        'Supply Chain',
        'Human Resources',
        'Social Impact',
        'Environmental Sustainability'
    ]
    selected_pillar = st.sidebar.selectbox(translate("Select Pillar for In-Depth Analysis", target_language), pillars)

    # Main page overview with key metrics and visualization
    st.title(translate("Startup Analysis Dashboard", target_language))
    st.markdown(translate("Overview of the startup's situation with key metrics and visualization", target_language))

    # Load mock data for development purposes
    startup_data = generate_mock_data()

    # Display overall score distribution
    st.header(translate("Overall Score Distribution", target_language))
    overall_distribution_chart = create_overall_score_distribution(startup_data, pillars)
    st.plotly_chart(overall_distribution_chart)

    # Display pillar score chart in main area when a pillar is selected
    if selected_pillar:
        st.header(translate(f"{selected_pillar} Analysis", target_language))
        pillar_chart = create_pillar_score_chart(startup_data, selected_pillar)
        st.plotly_chart(pillar_chart)

if __name__ == '__main__':
    main()
