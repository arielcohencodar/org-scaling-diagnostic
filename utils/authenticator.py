import streamlit as st
from utils.translator import translate

# Hardcoded user credentials (for demonstration purposes)
USER_CREDENTIALS = {
    "username": "Noa",
    "password": "ministryofdata"
}

def check_credentials(username, password):
    """Check if the entered credentials match the hardcoded ones."""
    return USER_CREDENTIALS["username"] == username and USER_CREDENTIALS["password"] == password

def authenticator(target_language):
    """Create an authentication page."""

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    # If the user is not authenticated, show login form
    if not st.session_state['authenticated']:
        st.title(translate("Login to Dashboard", target_language))
        with st.form("login_form"):
            username = st.text_input(translate("Username", target_language))
            password = st.text_input(translate("Password", target_language), type="password")
            submitted = st.form_submit_button(translate("Login", target_language))
            if submitted:
                if check_credentials(username, password):
                    st.session_state['authenticated'] = True
                    st.experimental_rerun()
                else:
                    st.error(translate("Authentication failed. Please check your credentials.", target_language))
    
    return st.session_state['authenticated']
