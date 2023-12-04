import openai
import pandas as pd
import streamlit as st
from utils.visualizer import draw_plot, draw_pie_chart
from legacy.data_generator import generate_data
from openai import OpenAI
from legacy.scenario_manager import load_scenarios
from legacy.metrics import display_deviation_metric
from legacy.query_manager import save_query, load_queries
from utils.translator import translate


openai.api_key = st.secrets['openai_api_key']
client = OpenAI(api_key=openai.api_key)  # Initialize the OpenAI client

def generative_ai_mode(config, target_language):
    st.sidebar.title(translate("Advanced Analytics Mode (GenAI)", target_language))
    mode = st.sidebar.radio(translate("Choose an option", target_language), [translate("Query Indicators", target_language), translate("Interpret Scenario", target_language)])

    if mode == translate("Query Indicators", target_language):
        # Existing functionality for querying indicators
        handle_query_indicators(config, target_language)
    elif mode == translate("Interpret Scenario", target_language):
        # New functionality for interpreting scenario challenges
        handle_interpret_scenario(config, target_language)

def handle_query_indicators(config, target_language):
    """
    Handles querying of indicators based on user input and generates a collective interpretation for all selected indicators.
    """
    # Allow the user to choose between creating a new query or loading an existing one
    #query_mode = st.sidebar.radio("Select action", ["Create New Query", "Load Saved Query"])

    #if query_mode == "Create New Query":
    # User input for the analysis
    instruction = st.text_area(translate("Enter the analysis you want to display:", target_language))

    if st.button(translate("Generate Indicators", target_language)):
        # Import the function within another function to avoid circular import
        def get_all_indicators_list(config):
            from dashboard import get_all_indicators_list
            return get_all_indicators_list(config)
        # Get the list of all indicators from the config
        all_indicators = get_all_indicators_list(config)

        # Process the user's instruction and get relevant indicators
        indicators, rationale = process_instructions(instruction, all_indicators)

        # Display the AI's rationale for the indicator selection
        st.write(translate("AI's rationale for selecting indicators:", target_language))
        st.write(rationale)

        # Display plots for each indicator, three per row
        for i in range(0, len(indicators), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(indicators):
                    with cols[j]:
                        indicator = indicators[i + j]
                        if indicator in all_indicators:
                            # Add a number input for setting the threshold
                            threshold = st.number_input(translate(f"Set threshold for {indicator}", target_language), key=f"threshold_{indicator}")
                            # Redraw the plot with the new threshold
                            fig = draw_plot(indicator, target_language, threshold=threshold)
                            st.plotly_chart(fig, use_container_width=True)

                            with st.expander(translate(f"Show more about {indicator}", target_language)):
                                avg_diff_checkbox = st.checkbox(translate(f"Show average difference for {indicator}", target_language), key=f"avg_diff_{indicator}")
                                pct_diff_checkbox = st.checkbox(translate(f"Show percentage difference for {indicator}", target_language), key=f"pct_diff_{indicator}")
                                if avg_diff_checkbox or pct_diff_checkbox:
                                    display_deviation_metric(indicator, avg_diff_checkbox, pct_diff_checkbox)

        # Generate and display a collective interpretation for all indicators
        if indicators:
            collective_interpretation = interpret_indicators_set(indicators, config)
            st.write(translate("Collective Interpretation for Selected Indicators:", target_language))
            st.write(collective_interpretation)

            """
            # Save the query to the session state
            query_name = st.text_input("Enter name for this query:")
            if query_name:
                save_query(query_name, {'indicators': indicators, 'interpretation': collective_interpretation})
                st.success(f"Query '{query_name}' saved!")
            """
        else:
            st.write(translate("No valid indicators were selected based on the query.", target_language))
    
    #elif query_mode == "Load Saved Query":
    #    load_saved_query()


def interpret_indicators_set(indicators, config):
    """
    Generate a collective interpretation for a set of indicators.

    Parameters:
    indicators (list): A list of indicators.
    config (dict): The configuration dictionary.

    Returns:
    str: The collective interpretation of the indicators.
    """
    narrative = "Analyzing the following indicators:\n\n"
    
    # Loop through each indicator and append its data to the narrative
    for indicator in indicators:
        dates, data = generate_data(indicator)
        data_points = list(zip([date.strftime("%Y-%m-%d") for date in dates[-12:]], data[-12:]))
        df = pd.DataFrame(data_points, columns=['Date', 'Value'])
        narrative += f"{indicator}:\n{df.to_string(index=False)}\n\n"

    # Add a prompt for the AI to interpret the collective data
    prompt = narrative + "Please provide a comprehensive interpretation of the trends and implications based on the above indicators."

    # Query OpenAI API for interpretation
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500,
            stop=None,
            n=1
        )
        interpretation = next((choice.message.content for choice in response.choices if choice.message.role == 'assistant'), '')
        return interpretation
    except openai.OpenAIError as e:
        return f"An error occurred while generating the interpretation: {str(e)}"




def handle_interpret_scenario(config, target_language):
    """
    Allows the user to select a scenario and a challenge within it to perform advanced analytics.
    """
    # Load existing scenarios
    scenarios = load_scenarios()

    # UI to select a scenario
    selected_scenario = st.sidebar.selectbox(translate("Select a Scenario", target_language), list(scenarios.keys()))

    if selected_scenario:
        scenario_data = scenarios[selected_scenario]

        # UI to select a challenge within the scenario
        challenge_names = list(scenario_data['challenges'].keys())
        selected_challenge = st.sidebar.selectbox(translate("Select a Challenge", target_language), challenge_names)

        # Button to generate analytics for the selected challenge
        if st.sidebar.button(translate("Analyze Challenge", target_language)):
            st.header(translate(f"Advanced Analytics for Challenge: {selected_challenge}", target_language))

            # Get the indicators for the selected challenge
            indicators = scenario_data['challenges'][selected_challenge]

            # Display plots for each indicator, three per row
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
                                threshold = st.number_input(translate(f"Set threshold for {indicators[i + j]}", target_language), key=f"threshold_{indicators[i + j]}")

                                # Redraw the plot with the new threshold
                                fig = draw_plot(indicators[i + j], target_language, threshold=threshold)
                                st.plotly_chart(fig, use_container_width=True)

                                with st.expander(translate(f"Show more about {indicators[i + j]}", target_language)):
                                    avg_diff_checkbox = st.checkbox(translate(f"Show average difference for {indicators[i + j]}", target_language), key=f"avg_diff_{indicators[i + j]}")
                                    pct_diff_checkbox = st.checkbox(translate(f"Show percentage difference for {indicators[i + j]}", target_language), key=f"pct_diff_{indicators[i + j]}")
                                    if avg_diff_checkbox or pct_diff_checkbox:
                                        display_deviation_metric(indicators[i + j], avg_diff_checkbox, pct_diff_checkbox)

            # Generate and display a comprehensive interpretation for the challenge
            interpretation = interpret_scenario_challenge(selected_challenge, indicators, config)
            st.write(translate("Comprehensive Interpretation:", target_language))
            st.write(translate(interpretation, target_language))



def process_instructions(instruction, all_indicators, target_language):
    # Creating a prompt for the AI to understand that it should choose from a list
    prompt = f"Based on the following instruction: '{instruction}', " \
             f"which of these indicators would be most relevant to focus on? " \
             f"Please provide a list of indicators listed with '- ' prefix.\n\n" \
             f"Options: {', '.join(all_indicators)}\n\n" \
             f"Selected indicators:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Specify the GPT-3.5 chat model
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )

    exclude_indicators = {"Map of Construction Sites", "Percentage of Reservists per Industry"}

    # Check if the response has a 'choices' attribute and if it's not empty
    if hasattr(response, 'choices') and response.choices:
        # Extract the full content from the assistant's message for rationale
        assistant_message = next((choice.message.content for choice in response.choices if choice.message.role == 'assistant'), '')

        # Initialize an empty list for indicators
        indicators = []
        rationale = assistant_message  # Store the full assistant message as rationale

        # Assume the AI's response contains a comma-separated list of indicators
        lines = assistant_message.split(',')
        for line in lines:
            # Remove any leading or trailing whitespace
            indicator = line.strip()
            # Attempt to match the extracted indicator with the application's known indicators
            matched_indicator = next((known_indicator for known_indicator in all_indicators
                                    if known_indicator.lower() == indicator.lower()), None)
            if matched_indicator:
                indicators.append(matched_indicator)

        # # Assumes indicators are listed with '- ' prefix
        lines = assistant_message.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("- ") or line.startswith("• "):
                indicator = line[2:]  # Remove the '- ' prefix
                if indicator in all_indicators:  # Check if the indicator is recognized
                    indicators.append(indicator)
        
        # Filter out specific indicators
        indicators = [ind for ind in indicators if ind not in exclude_indicators]

        return indicators, rationale
    else:
        # Handle the case where response.choices is empty or not as expected
        return [], translate("No response received from AI.", target_language)

def interpret_scenario_challenge(challenge_name, indicators, config):
    """
    Interpret a set of indicators for a challenge using OpenAI's language model.

    Parameters:
    challenge_name (str): The name of the challenge.
    indicators (list): A list of indicators for the challenge.
    config (dict): The configuration dictionary.

    Returns:
    str: The collective interpretation of the indicators for the challenge.
    """
    
    exclude_indicators = {"Map of Construction Sites", "Percentage of Reservists per Industry"}
    # Filter out specific indicators
    indicators = [ind for ind in indicators if ind not in exclude_indicators]

    narrative = f"Challenge: {challenge_name}\n\n"
    
    # Loop through each indicator and append its data to the narrative
    for indicator in indicators:
        dates, data = generate_data(indicator)
        data_points = list(zip([date.strftime("%Y-%m-%d") for date in dates[-12:]], data[-12:]))
        df = pd.DataFrame(data_points, columns=['Date', 'Value'])
        narrative += f"Here is the data for the indicator '{indicator}' over time:\n{df.to_string(index=False)}\n\n"

    # Add a prompt for the AI to interpret the collective data
    prompt = narrative + "Based on the trends in this data for all indicators, please provide a comprehensive interpretation of the situation for this challenge."

    # Query OpenAI API for interpretation
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500,
            stop=None,
            n=1
        )
        interpretation = next((choice.message.content for choice in response.choices if choice.message.role == 'assistant'), '')
        return interpretation
    except openai.OpenAIError as e:
        return f"An error occurred while generating the interpretation: {str(e)}"
    

def load_saved_query(target_language):
    """
    Loads and displays a saved query from the file using Streamlit's interface.
    """
    queries = load_queries()  # Always load the latest queries

    if queries:
        selected_query = st.selectbox(target_language("Select a saved query", target_language), list(queries.keys()), index=0)
        if st.button(translate("Load Query", target_language)):
            query_data = queries[selected_query]
            st.write(translate(f"Loaded Query: {selected_query}", target_language))
            st.write(translate("Selected Indicators:", target_language))
            st.write(translate(query_data['indicators'], target_language))
            st.write(translate("Collective Interpretation:", target_language))
            st.write(translate(query_data['interpretation'], target_language))
    else:
        st.write(translate("No saved queries available.", target_language))
