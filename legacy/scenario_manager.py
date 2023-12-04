# utils/scenario_manager.py

import os
import json
import streamlit as st

# Define a path for saving scenario data
SCENARIOS_FILE_PATH = 'scenarios.json'

@st.cache(allow_output_mutation=True)
def load_scenarios():
    """
    Load existing scenarios from a file.
    """
    if os.path.exists(SCENARIOS_FILE_PATH):
        with open(SCENARIOS_FILE_PATH, 'r') as file:
            scenarios = json.load(file)
    else:
        scenarios = {}
    return scenarios

def save_scenario(scenario_data):
    """
    Save a new scenario to the file.
    """
    scenarios = load_scenarios()  # Load existing scenarios
    scenario_name = scenario_data['name']
    
    # Add the new scenario to the scenarios dictionary
    scenarios[scenario_name] = scenario_data
    
    # Write the updated scenarios back to the file
    with open(SCENARIOS_FILE_PATH, 'w') as file:
        json.dump(scenarios, file)
    
    # Clear the cache after updating the file
    st.cache_data.clear()

def create_scenario(name, goal, challenges):
    """
    Create a new scenario and add it to the scenarios file.
    """
    scenario_data = {
        'name': name,
        'goal': goal,
        'challenges': challenges
    }
    save_scenario(scenario_data)

def delete_scenario(scenario_name):
    """
    Delete a scenario and remove it from the scenarios file.
    Returns True if the scenario was successfully deleted.
    """
    scenarios = load_scenarios()
    if scenario_name in scenarios:
        del scenarios[scenario_name]
        with open(SCENARIOS_FILE_PATH, 'w') as file:
            json.dump(scenarios, file)
        st.cache_data.clear()
        return True
    return False
