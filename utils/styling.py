import streamlit as st

def set_global_style():
    style = """
    <style>
        /* Global style settings */
        html, body, .stApp {
            color: #0038A8;  /* Blue text */
            background-color: #FFFFFF;  /* White background */
        }

        /* Styling the sidebar with darker blue color */
        [data-testid="stSidebarContent"] {
            background-color: #002080; /* Darker blue color */
        }

        /* Titles and labels in the sidebar are white */
        [data-testid="stSidebarContent"] .st-bd,
        [data-testid="stSidebarContent"] .css-145kmo2 {
            color: #FFFFFF; /* White text */
        }

        /* Interactive widgets text should be dark for readability */
        [data-testid="stSidebarContent"] .stSelectbox .css-2b097c-container,
        [data-testid="stSidebarContent"] .stRadio .css-1e6y48t-container,
        [data-testid="stSidebarContent"] .stMultiSelect .css-2b097c-container,
        [data-testid="stSidebarContent"] .stTextInput,
        [data-testid="stSidebarContent"] .stSlider .css-1a6whwp-container {
            color: #0038A8; /* Blue text */
            background-color: #FFFFFF; /* White background for widgets */
        }

        /* Button styles */
        .stButton>button {
            color: #FFFFFF;  /* White text */
            background-color: #0038A8;  /* Blue background */
            border: none;
            border-radius: 5px;
            padding: 10px 24px;
        }

        .stButton>button:hover {
            background-color: #001040;  /* Even darker blue on hover */
        }

        /* Custom style for a specific element */
        .st-emotion-cache-1y4p8pa {
            flex: 1 1 0%;
            width: 100%;
            padding: 5rem 1rem 1rem;
            max-width: 100rem;
        }

        /* Custom styles for other Streamlit elements if needed */
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

def set_width_style():
    style = """
    <style>
        /* Custom style for a specific element */
        .st-emotion-cache-1y4p8pa {
            flex: 1 1 0%;
            width: 100%;
            padding: 5rem 1rem 1rem;
            max-width: 100rem;
        }

        /* Custom styles for other Streamlit elements if needed */
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)
