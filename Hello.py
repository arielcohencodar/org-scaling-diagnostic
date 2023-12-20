# Hello.py

import streamlit as st
from utils.config_loader import load_config
from utils.authenticator import authenticator
from utils.styling import set_width_style
from utils.translator import translate
from utils.employee_review_analysis import load_review_data, get_basic_statistics, create_rating_distribution_chart, generate_detailed_analysis, create_score_over_time_charts
from utils.talent_recruitment_analysis import (
    load_and_preprocess_data, 
    compute_attrition_and_headcount, 
    compute_headcount_by_company, 
    create_company_headcount_chart, 
    compute_function_wise_attrition, 
    create_function_wise_chart, 
    create_comparison_chart
)


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

            # Compute attrition rates and headcount
            incredibuild_attrition, incredibuild_headcount = compute_attrition_and_headcount(incredibuild_data)
            benchmark_attrition, _ = compute_attrition_and_headcount(all_profiles_data)
            benchmark_headcounts = compute_headcount_by_company(all_profiles_data)

            # Add Incredibuild's headcount to the benchmark_headcounts for comparison
            benchmark_headcounts['Incredibuild'] = incredibuild_headcount

            # Create and display comparison charts
            attrition_chart = create_comparison_chart(incredibuild_attrition, benchmark_attrition, 'Attrition Rate Comparison', 'Attrition Rate')
            headcount_chart = create_company_headcount_chart(benchmark_headcounts, 'Company Headcount Comparison')
            st.plotly_chart(attrition_chart)
            st.plotly_chart(headcount_chart)

            # Compute and display function-wise attrition charts
            incredibuild_function_attrition = compute_function_wise_attrition(incredibuild_data)
            incredibuild_function_chart = create_function_wise_chart(incredibuild_function_attrition, 'Incredibuild Function-Wise Attrition')
            st.plotly_chart(incredibuild_function_chart)

        # Inside the 'Company Culture Assessment' section
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
