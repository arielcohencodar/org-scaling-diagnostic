# query_manager.py

import streamlit as st
import json
import os

# Define a path for saving query data
QUERIES_FILE_PATH = 'queries.json'

@st.cache(allow_output_mutation=True)
def load_queries():
    """
    Load existing queries from a file.
    """
    if os.path.exists(QUERIES_FILE_PATH):
        with open(QUERIES_FILE_PATH, 'r') as file:
            queries = json.load(file)
    else:
        queries = {}
    return queries

def save_query(query_name, query_data):
    """
    Save a new query to the file.
    """
    queries = load_queries()  # Load existing queries
    queries[query_name] = query_data  # Add the new query
    
    # Write the updated queries back to the file
    with open(QUERIES_FILE_PATH, 'w') as file:
        json.dump(queries, file)
    
    # Clear the cache after updating the file
    st.cache_data.clear()

def delete_query(query_name):
    """
    Delete a query and remove it from the file.
    Returns True if the query was successfully deleted.
    """
    queries = load_queries()
    if query_name in queries:
        del queries[query_name]
        with open(QUERIES_FILE_PATH, 'w') as file:
            json.dump(queries, file)
        st.cache_data.clear()
        return True
    return False
