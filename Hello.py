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
from utils.styling import set_global_style, set_width_style
from utils.translator import translate

# Load the updated configuration
config = load_config()

# Extract configurations
startups = config['startups']['names']
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
        st.write(translate("Name: Consultant", target_language))  # TO DO - Replace with dynamic user information if available
        st.write(translate("Company: StartUp Nation", target_language))

    # Initialize scenario mode active state if it doesn't exist
    if 'scenario_mode_active' not in st.session_state:
        st.session_state['scenario_mode_active'] = False

    mode = st.sidebar.radio(
        translate("Mode", target_language),
        [
            translate("Standard", target_language),
            #translate("Scenario", target_language),
            #translate("Advanced Analytics", target_language)
        ]
    )
    
    # Check if in detailed view and display appropriate layout
    if st.session_state.get('view_detailed_metric', False):
        display_detailed_view()
    #elif mode == translate("Scenario", target_language):
    #    scenario_flow(target_language)
    #elif mode == translate("Advanced Analytics", target_language):
    #    generative_ai_mode(config, target_language)
    else:
        standard_mode_flow(target_language)

def standard_mode_flow(target_language):
    # Standard mode UI for startup selection
    selected_startup, selected_indicators = display_startup_selection_ui(target_language)

    # Use the selected industry hash for consistent random data generation
    #industry_hash = get_industry_hash(selected_industry)
    #np.random.seed(industry_hash)
    
    # Display the main dashboard with the chosen startup and indicators
    show_main_dashboard(selected_startup, selected_indicators, target_language)

def display_startup_selection_ui(target_language):
    # Sidebar UI for startup selection
    st.sidebar.title(translate("Startup Overview", target_language))
    selected_startup = st.sidebar.selectbox(translate('Select Startup:', target_language), startups, 0)

    return selected_startup

if __name__ == '__main__':
    run()
