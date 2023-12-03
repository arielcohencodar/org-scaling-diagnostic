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
from pages import overall_analysis, customer_sentiment, seo_analysis, sales_efficiency, organizational_structure

# App title
st.title("Startup Scaling Analysis Dashboard")

# Sidebar navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ("Overall Analysis", "Customer Sentiment", "SEO Analysis", "Sales Efficiency", "Organizational Structure"))

# Page routing
if choice == "Overall Analysis":
    overall_analysis.show()
elif choice == "Customer Sentiment":
    customer_sentiment.show()
elif choice == "SEO Analysis":
    seo_analysis.show()
elif choice == "Sales Efficiency":
    sales_efficiency.show()
elif choice == "Organizational Structure":
    organizational_structure.show()
