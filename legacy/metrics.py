import streamlit as st
import numpy as np
from legacy.data_generator import generate_data
from utils.translator import translate

def display_deviation_metric(title, show_avg_diff, show_pct_diff, target_language):
    """
    Display the deviation metrics for the given startup scaling indicator.
    """
    try:
        dates, data = generate_data(indicator=title)
        # Ensure there's enough data to compare
        if len(data) >= 55:
            # Custom logic for analyzing startup data
            # Example: Compare the average of the last 3 data points against the last 52 weeks
            avg_last_3 = np.mean(data[-3:])
            avg_last_52 = np.mean(data[-55:-3])
            avg_difference = avg_last_3 - avg_last_52
            pct_difference = (avg_difference / avg_last_52) * 100 if avg_last_52 != 0 else 0

            # Display the average difference
            if show_avg_diff:
                st.metric(
                    label=translate(f"{title} - Avg Difference", target_language),
                    value=f"{avg_difference:.2f}",
                    delta=f"{avg_difference:.2f} compared to last year"
                )

            # Display the percentage difference
            if show_pct_diff:
                st.metric(
                    label=translate(f"{title} - Percentage Difference", target_language),
                    value=f"{pct_difference:.2f}%",
                    delta=f"{pct_difference:.2f}% compared to last year"
                )
    except Exception as e:
        st.error(translate(f"Error generating metric for {title}: {e}", target_language))
