# Hello.py

import streamlit as st
from utils.config_loader import load_config
from utils.authenticator import authenticator
from utils.styling import set_width_style
from utils.translator import translate
from utils.visualization import create_pillar_score_chart, create_overall_score_distribution
from utils.employee_review_analysis import load_review_data, get_basic_statistics, create_rating_distribution_chart, generate_detailed_analysis, create_score_over_time_charts
from utils.talent_recruitment_analysis import load_and_preprocess_data, compute_attrition, create_attrition_comparison_chart


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


    # Display analysis or under construction message
    if selected_pillar:
        st.header(translate(f"{selected_pillar} Analysis", target_language))
        under_construction = config['under_construction'].get(selected_pillar, False)
        if under_construction:
            st.warning(translate("This analysis is currently under construction.", target_language))
        # Inside the 'Talent Excellence and Recruitment' section
        elif selected_pillar == "Talent Excellence and Recruitment":
            # Load and preprocess the recruitment data
            incredibuild_file_path = './data/Incredibuild/HRIS/001_INCREDIBUILD_ALL_PROFILES.csv'  # Replace with the actual path
            all_profiles_file_path = './data/Incredibuild/HRIS/001_ALL_PROFILES.csv'  # Replace with the actual path
            incredibuild_data, all_profiles_data = load_and_preprocess_data(incredibuild_file_path, all_profiles_file_path)

            # Compute attrition rates
            incredibuild_attrition = compute_attrition(incredibuild_data)
            all_profiles_attrition = compute_attrition(all_profiles_data)

            # Create and display attrition rate comparison chart
            attrition_comparison_chart = create_attrition_comparison_chart(incredibuild_attrition, all_profiles_attrition)
            st.plotly_chart(attrition_comparison_chart)
        elif selected_pillar == "Company Culture Assessment":
            # Company Culture Assessment
            review_data_path = './data/Incredibuild/Employees Reviews/reviews_Incredibuild_processed.xlsx' #TODO: change to config
            review_data = load_review_data(review_data_path)
            basic_stats = get_basic_statistics(review_data)
            rating_dist_chart = create_rating_distribution_chart(review_data)
            detailed_analysis = generate_detailed_analysis(review_data, ["Company Culture"])

            st.write(translate("Basic Statistics:", target_language))
            st.write(basic_stats)
            # Displaying rating distribution chart
            st.plotly_chart(rating_dist_chart)
            # Displaying score over time charts
            score_columns = ["Work/Life Balance", "Diversity & Inclusion", "Career Opportunities", "Compensation and Benefits", "Senior Management"]
            score_time_charts = create_score_over_time_charts(review_data, score_columns)
            for chart in score_time_charts:
                st.plotly_chart(chart)
            st.write(translate("Detailed Analysis:", target_language))
            st.write(detailed_analysis)
        else:
            st.info(translate("Analysis details will be displayed here.", target_language))

if __name__ == '__main__':
    main()
