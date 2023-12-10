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
from utils.authenticator import authenticator
from utils.styling import set_width_style
from utils.translator import translate

# Main file of the Streamlit app

def main():
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
        st.write(translate("Name: ClientX", target_language))  # TO DO - Replace with dynamic user information if available
        st.write(translate("Job: Head of strategy", target_language))

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

if __name__ == '__main__':
    main()

