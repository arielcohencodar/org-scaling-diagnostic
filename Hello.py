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
from utils.visualizer import plot_data
from utils.dashboard_functions import show_dashboard
from utils.data_loader import load_data, get_sheet_names

# Main file of the Streamlit app

def main():
    st.title('Business Analysis Dashboard')

    # Load sheet names
    sheet_names = get_sheet_names()

    # Dropdown menu for sheet selection
    sheet_name = st.sidebar.selectbox('Select a Sheet', sheet_names)

    # Load and display the data
    data = load_data(sheet_name)
    st.write(data)

    # Show the dashboard
    show_dashboard(sheet_name, data)

if __name__ == '__main__':
    main()

