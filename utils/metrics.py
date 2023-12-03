import streamlit as st

from utils.data_generator import generate_data
from utils.config_loader import config
import numpy as np
from utils.translator import translate


def display_deviation_metric(title, show_avg_diff, show_pct_diff, target_language):
    """
    Display the deviation metrics for the given indicator.
    """
    try:
        dates, data = generate_data(indicator=title)
        # Ensure there's enough data to compare
        if len(data) >= 55:
            avg_last_3_weeks = np.mean(data[-3:])
            avg_last_52_weeks = np.mean(data[-55:-3])
            avg_difference = avg_last_3_weeks - avg_last_52_weeks
            pct_difference = (avg_difference / avg_last_52_weeks) * 100 if avg_last_52_weeks != 0 else 0

            if show_avg_diff:
                st.metric(
                    label=translate(f"{title} - Avg Diff", target_language),
                    value=f"{avg_difference:.2f}",
                    delta=f"{avg_difference:.2f} Avg difference last 3 weeks vs last 52 weeks"
                )
            if show_pct_diff:
                st.metric(
                    label=translate(f"{title} - Pct Diff", target_language),
                    value=f"{pct_difference:.2f}%",
                    delta=f"{pct_difference:.2f}% Percentage difference last 3 weeks vs last 52 weeks"
                )
    except Exception as e:
        st.error(translate(f"An error occurred while generating the metric for {title}: {e}", target_language))
