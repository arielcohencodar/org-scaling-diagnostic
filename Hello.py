# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import numpy as np

# Modularized imports
from utils.config_loader import load_config
from utils.hash_utils import get_industry_hash
from utils.dashboard_functions import show_main_dashboard, display_detailed_view
from utils.authenticator import authenticator
from utils.scenario_manager import create_scenario, load_scenarios, save_scenario, delete_scenario
from utils.visualizer import draw_plot, draw_pie_chart
from utils.metrics import display_deviation_metric
from utils.styling import set_global_style, set_width_style
# Additional import for handling the Generative AI mode
from utils.generative_mode_manager import generative_ai_mode
from utils.translator import translate

# Load the updated configuration
config = load_config()

# Extract configurations
industries = config['industries']['names']
indicators_grouped = {key: config['indicators_grouped'][key] for key in config['indicators_grouped']}


def run():

    # Styling

    #set_global_style()
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
        st.write(translate("Name: Noa", target_language))  # TO DO - Replace with dynamic user information if available
        st.write(translate("Job: Ministry of Economy", target_language))

    # Initialize scenario mode active state if it doesn't exist
    if 'scenario_mode_active' not in st.session_state:
        st.session_state['scenario_mode_active'] = False

    mode = st.sidebar.radio(
        translate("Mode", target_language),
        [
            translate("Standard", target_language),
            translate("Scenario", target_language),
            translate("Advanced Analytics", target_language)
        ]
    )
    
    # Check if in detailed view and display appropriate layout
    if st.session_state.get('view_detailed_metric', False):
        display_detailed_view()
    elif mode == translate("Scenario", target_language):
        scenario_flow(target_language)
    elif mode == translate("Advanced Analytics", target_language):
        generative_ai_mode(config, target_language)
    else:
        standard_mode_flow(target_language)

def standard_mode_flow(target_language):
    # Only show new indicator selection UI in overview mode
    selected_industry, selected_industry_indicators, selected_shared_indicators = display_new_indicator_selection_ui(target_language)
    
    # Use the selected industry hash for consistent random data generation
    industry_hash = get_industry_hash(selected_industry)
    np.random.seed(industry_hash)
    
    # Display the main dashboard with the chosen industry and indicators
    show_main_dashboard(selected_industry, selected_industry_indicators, selected_shared_indicators, indicators_grouped, target_language)

def display_new_indicator_selection_ui(target_language):

    st.sidebar.title(translate("Sector Overview", target_language))

    # Allow user to select an industry
    selected_industry = st.sidebar.selectbox(translate('Select Industry:', target_language), industries, 0)

    # Filter industry-specific indicators based on search query
    all_industry_specific_indicators = config['industry_specific'].get(selected_industry, [])
    # Display filtered industry-specific indicators for selection
    selected_industry_specific_indicators = st.sidebar.multiselect(translate("Select Industry Specific Indicators", target_language), all_industry_specific_indicators, key='industry_specific')

    # Filter shared indicators based on search query
    all_shared_indicators = config['shared_indicators']['Indicators']
    # Display filtered shared indicators for selection
    selected_shared_indicators = st.sidebar.multiselect(translate("Select Shared Indicators", target_language), all_shared_indicators, key='shared_indicators')

    return selected_industry, selected_industry_specific_indicators, selected_shared_indicators

    
def scenario_flow(target_language):
    """
    Handles the flow of creating, selecting, or deleting a scenario.
    """
    st.sidebar.title(translate("Scenario Mode", target_language))
    # Load existing scenarios from the session state or the source
    scenarios = st.session_state.get('scenarios', load_scenarios())

    # If a scenario has just been selected/created, show its details
    if 'selected_scenario' in st.session_state:
        display_scenario_dashboard(scenarios[st.session_state['selected_scenario']], target_language)

    # Otherwise, provide options to select, create, or delete scenarios
    else:
        # Radio button for selecting the action
        scenario_action = st.sidebar.radio(
            translate("Choose an action:", target_language),
            [
                translate("Select", target_language),
                translate("Create", target_language),
                translate("Delete", target_language)
            ]
        )

        if scenario_action == translate("Select", target_language):
            # Dropdown to select an existing scenario
            selected_scenario = st.sidebar.selectbox(translate("Select a Scenario", target_language), list(scenarios.keys()), key='scenario_select')
            if st.sidebar.button(translate("Display Scenario", target_language)):
                st.session_state['selected_scenario'] = selected_scenario
                st.experimental_rerun()

        elif scenario_action == translate("Create", target_language):
            # UI elements to input details for a new scenario
            scenario_name = st.sidebar.text_input(translate("Enter Scenario Name", target_language), key='scenario_name')
            scenario_goal = st.sidebar.text_input(translate("Enter Scenario Goal", target_language), key='scenario_goal')

            # Initialize challenges in session state
            if 'challenges' not in st.session_state:
                st.session_state['challenges'] = {}

            # UI to add a challenge
            challenge_name = st.sidebar.text_input(translate("Enter Challenge Name", target_language), key='new_challenge_name')
            selected_indicators = st.sidebar.multiselect(translate("Select Indicators for the Challenge", target_language), all_indicators_list, key='new_challenge_indicators')

            if st.sidebar.button(translate("Add Challenge", target_language), on_click=add_challenge_callback):
                if challenge_name and selected_indicators:
                    # Add the challenge and its indicators to the session state
                    st.session_state['challenges'][challenge_name] = selected_indicators
                    # Clear inputs for adding the next challenge
                    st.session_state['new_challenge_name'] = ""
                    st.session_state['new_challenge_indicators'] = []
                    st.experimental_rerun()
            # Display existing challenges and allow adding indicators
            for challenge in st.session_state.get('challenges', {}):
                st.sidebar.subheader(translate(f"Challenge: {challenge}", target_language))

            # Save scenario
            if st.sidebar.button(translate("Save New Scenario", target_language)):
                scenario_data = {
                    "name": scenario_name,
                    "goal": scenario_goal,
                    "challenges": st.session_state.get('challenges', {})
                }
                save_scenario(scenario_data)
                st.sidebar.success(translate("Scenario saved!", target_language))
                # Clear session state
                st.session_state.pop('challenges', None)  # Clear challenges after saving
                st.session_state.pop('selected_scenario', None)  # Reset selected scenario
                st.experimental_rerun()

        elif scenario_action == translate("Delete", target_language):
            # Dropdown to select a scenario to delete
            scenario_to_delete = st.sidebar.selectbox(translate("Select a Scenario to Delete", target_language), list(scenarios.keys()), key='scenario_delete')
            if st.sidebar.button(translate("Delete Scenario", target_language)):
                # Delete the selected scenario
                if delete_scenario(scenario_to_delete):
                    # Clear session state related to scenarios and rerun
                    st.session_state.pop('selected_scenario', None)
                    st.session_state.pop('scenarios', None)  # To refresh the list of scenarios
                    st.experimental_rerun()
                else:
                    st.sidebar.error("Failed to delete the scenario.")

    # Add a button to exit scenario mode and return to the standard dashboard
    if st.sidebar.button(translate("Exit Scenario Mode", target_language)):
        st.session_state.pop('selected_scenario', None)  # Remove the selected scenario from session state
        st.experimental_rerun()

def add_challenge_callback():
    # Add the challenge and its indicators to the session state
    challenge_name = st.session_state['new_challenge_name']
    selected_indicators = st.session_state['new_challenge_indicators']
    if challenge_name and selected_indicators:
        st.session_state['challenges'][challenge_name] = selected_indicators
        # Reset the input fields for the next challenge
        st.session_state['new_challenge_name'] = ""
        st.session_state['new_challenge_indicators'] = []

def display_scenario_dashboard(scenario, target_language):
    st.title(translate(f"Scenario: {scenario['name']}", target_language))
    st.write(translate(f"Goal: {scenario['goal']}", target_language))

    for challenge, indicators in scenario['challenges'].items():
        st.header(translate(f"Challenge: {challenge}", target_language))
        # Display indicators in rows of 3
        for i in range(0, len(indicators), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(indicators):
                    with cols[j]:
                        if indicators[i+j]=="Percentage of Reservists per Industry":
                            fig = draw_pie_chart(target_language)
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            # Add a number input for setting the threshold
                            threshold = st.number_input(translate(f"Set threshold for {indicators[i+j]}", target_language), key=f"threshold_{indicators[i+j]}")

                            # Redraw the plot with the new threshold
                            fig = draw_plot(indicators[i+j], target_language, threshold=threshold)
                            st.plotly_chart(fig, use_container_width=True)
                            with st.expander(translate(f"Show more about {indicators[i + j]}", target_language)):
                                avg_diff_checkbox = st.checkbox(translate(f"Show average difference for {indicators[i + j]}", target_language), key=f"avg_diff_{indicators[i + j]}")
                                pct_diff_checkbox = st.checkbox(translate(f"Show percentage difference for {indicators[i + j]}", target_language), key=f"pct_diff_{indicators[i + j]}")
                                if avg_diff_checkbox or pct_diff_checkbox:
                                    display_deviation_metric(indicators[i + j], avg_diff_checkbox, pct_diff_checkbox)



def get_all_indicators_list(config):
    """
    Extract all unique indicator names from the indicator_plot_types section of the config.

    :param config: The configuration dictionary loaded from config.toml
    :return: A list of unique indicator names
    """
    # The indicators are the keys in the 'indicator_plot_types' section of the config
    all_indicators = list(config['indicator_plot_types'].keys())
    return all_indicators

# Load the configuration
config = load_config()

# Now get the all_indicators_list
all_indicators_list = get_all_indicators_list(config)

def create_new_scenario_flow(target_language):
    st.sidebar.subheader(translate("Create New Scenario", target_language))
    scenario_name = st.sidebar.text_input(translate("Enter Scenario Name", target_language))
    goal = st.sidebar.text_input(translate("Enter the goal for the scenario:", target_language))

    if scenario_name and goal:
        st.sidebar.subheader(translate("Define Challenges and Indicators", target_language))
        # Initialize or get the existing challenges
        if 'challenges' not in st.session_state:
            st.session_state['challenges'] = {}

        # Interface to add new challenge
        new_challenge = st.sidebar.text_input(translate("Enter a new challenge", target_language))
        if new_challenge and st.sidebar.button(translate("Add Challenge", target_language)):
            st.session_state['challenges'][new_challenge] = []

        # Display existing challenges and allow adding indicators
        for challenge in st.session_state['challenges']:
            st.sidebar.subheader(f"Challenge: {challenge}")
            selected_indicators = st.sidebar.multiselect(translate(f"Select indicators for {challenge}", target_language), all_indicators_list, key=f'indicators_{challenge}')
            st.session_state['challenges'][challenge] = selected_indicators

        # Save scenario
        if st.sidebar.button(translate("Save Scenario", target_language)):
            scenario_data = {
                "name": scenario_name,
                "goal": goal,
                "challenges": st.session_state['challenges']
            }
            save_scenario(scenario_data)
            st.sidebar.success(translate("Scenario saved!", target_language))
            # Clear session state
            del st.session_state['challenges']
            # Redirect to scenario selection
            st.session_state['scenario_mode_active'] = True
            st.session_state['scenario_selected'] = True
            st.session_state['selected_scenario'] = scenario_name
            st.experimental_rerun()

def select_existing_scenario(scenarios, target_language):
    """
    Handles the selection of an existing scenario.
    """
    selected_scenario = st.sidebar.selectbox(translate("Select a Scenario", target_language), scenarios)
    if selected_scenario:
        # Display the selected scenario's data
        scenario_data = scenarios[selected_scenario]
        st.sidebar.text(translate(f"Goal: {scenario_data['goal']}", target_language))
        display_scenario_indicators(scenario_data['indicators'], target_language)

def display_scenario_indicators(selected_indicators, target_language):
    """
    Display the dashboard for a set of scenario cross-sector chosen indicators.

    :param selected_indicators: A list of indicators chosen by the user when creating the scenario.
    """
    # No need for filters here as we are displaying a custom scenario across sectors
    st.title(translate("Scenario Dashboard", target_language))
    
    # Check if there are any selected indicators
    if not selected_indicators:
        st.write(translate("No indicators selected for this scenario.", target_language))
        return

    # Initialize a dictionary in the session state to track the display state of indicators
    if 'display_states' not in st.session_state:
        st.session_state['display_states'] = {indicator: 'graph' for indicator in selected_indicators}

    # Display each selected indicator with a toggle button
    for indicator in selected_indicators:
        # Create a container for each graph/metric
        container = st.container()
        with container:
            # Check the current state and display accordingly
            if st.session_state['display_states'].get(indicator, 'graph') == 'graph':
                # Add a number input for setting the threshold
                threshold = st.number_input(translate(f"Set threshold for {indicator}", target_language), key=f"threshold_{indicator}")

                # Redraw the plot with the new threshold
                fig = draw_plot(indicator, target_language, threshold=threshold)
                st.plotly_chart(fig, use_container_width=True)
                if st.button(translate(f"Show Metric for {indicator}", target_language), key=f"btn_{indicator}"):
                    st.session_state['display_states'][indicator] = 'metric'
            else:
                display_deviation_metric(indicator)
                if st.button(translate(f"Show Graph for {indicator}", target_language), key=f"btn_{indicator}"):
                    st.session_state['display_states'][indicator] = 'graph'

if __name__ == '__main__':
    run()
