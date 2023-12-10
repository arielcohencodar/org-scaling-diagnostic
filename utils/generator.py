# utils/generator.py

import pandas as pd
import numpy as np

def generate_mock_data(num_startups=100):
    """
    Generates mock data for development purposes.
    
    Parameters:
    num_startups (int): Number of mock startups to generate data for.

    Returns:
    DataFrame: A pandas DataFrame with mock data.
    """
    
    # Define pillars for analysis
    pillars = [
        'Market Fit', 
        'Team', 
        'Product', 
        'Growth Strategy', 
        'Financials',
        'Customer Satisfaction',
        'Operational Efficiency',
        'Technical Scalability',
        'Regulatory Compliance',
        'Innovation',
        'Funding',
        'Market Reach',
        'Customer Acquisition',
        'Brand Strength',
        'Strategic Positioning',
        'Risk Management',
        'Supply Chain',
        'Human Resources',
        'Social Impact',
        'Environmental Sustainability'
    ]

    # Generate random scores for each pillar for each startup
    scores = np.random.uniform(1, 10, (num_startups, len(pillars)))  # scores between 1 and 10

    # Create a DataFrame
    data = {
        'Startup ID': np.arange(1, num_startups + 1),
    }

    # Add the scores for each pillar to the DataFrame
    for i, pillar in enumerate(pillars):
        data[pillar] = scores[:, i]

    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generate and print a sample of mock data
    mock_data = generate_mock_data()
    print(mock_data.head())  # Print the first five rows of the mock data
