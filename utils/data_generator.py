import numpy as np
import datetime
import pandas as pd

# Helper function to generate date ranges
def generate_dates(start_date, num_weeks):
    return [start_date + datetime.timedelta(weeks=i) for i in range(num_weeks)]

# Helper functions for applying crisis effects
def apply_sharp_increase(data, index, scale=2.0):
    adjustment_factor = np.linspace(1, scale, len(data) - index)
    data[index:] *= adjustment_factor
    return data

def apply_sharp_decrease(data, index, scale=0.5):
    adjustment_factor = np.linspace(1, scale, len(data) - index)
    data[index:] *= adjustment_factor
    return data

# Function to generate data based on the indicator with the crisis starting on November 8th, 2023
def generate_data(indicator):
    """
    Generate data for the specified indicator with a crisis starting on November 8th, 2023.
    """

    if indicator == "Map of Construction Sites":
        # Dummy data for construction sites
        data = {
            'lat': [32.0853, 31.7683, 32.7940, 31.2518, 29.5581],  # Latitudes for Tel Aviv, Jerusalem, Haifa, Beersheba, Eilat
            'lon': [34.7818, 35.2137, 34.9896, 34.7913, 34.9519],
        }
        return pd.DataFrame(data)

    # Number of weeks for 12 years
    num_weeks = 12 * 52

    # Start date set to 12 years ago
    start_date = datetime.date.today() - datetime.timedelta(weeks=num_weeks)

    dates = generate_dates(start_date, num_weeks)

    # Generate baseline data based on the indicator
    data_generators = {
        "GDP": lambda size: np.linspace(350, 400, size),
        "FDI inflows": lambda size: np.random.uniform(200, 400, size),
        "Real labor participation rate accounting for reserve duty unpaid leave and open vacancies": lambda size: np.random.uniform(4, 7, size),
        "10 year bond yield": lambda size: np.random.uniform(0.5, 3, size),
        "Interest rate": lambda size: np.random.uniform(0.1, 3, size),
        "Level of wages": lambda size: np.linspace(2000, 3000, size),
        "Foreign trade (Import and Export)": lambda size: np.random.uniform(-500, 500, size),
        "Stock market volatility (VIX)": lambda size: np.random.uniform(10, 60, size),
        "CPI (overall, core)": lambda size: np.random.uniform(0, 5, size),
        "PMI Manufacturing": lambda size: np.random.normal(loc=55, scale=2, size=size),
        "Loans defaults/Nonperforming loans to total loans": lambda size: np.random.uniform(0, 10, size),
        "Personal consumption spending and disposable household income": lambda size: np.random.uniform(5, 50, size),
        "Personal consumption spending by category": lambda size: np.random.uniform(5, 50, size),
        "Government tax revenue": lambda size: np.random.uniform(100, 200, size),
        "Home Price Index": lambda size: np.linspace(300, 600, size),
        "Consumer confidence index": lambda size: np.random.uniform(50, 150, size),
        "Sales CAGR of industry leaders": lambda size: np.random.uniform(0, 20, size),
        "Net working capital and cash reserves as a percentage of turnover": lambda size: np.random.uniform(10, 60, size),
        "OpEx CAGR of industry leaders": lambda size: np.random.uniform(0, 20, size),
        "Companies closed": lambda size: np.random.randint(0, 100, size),
        "Foreign trade": lambda size: np.random.uniform(100, 200, size),
        "Ability to work remotely": lambda size: np.random.uniform(0, 10, size),  # Assuming a score between 0-10
        "Raw material delays": lambda size: np.linspace(1, 30, size) + np.random.normal(0, 2, size),
        "Government support program utilization": lambda size: np.linspace(50, 20, size) + np.random.normal(0, 2, size),
        "Companies applied for chapter 11": lambda size: np.linspace(10, 100, size),  # Assuming an increasing trend
        "Percentage of foreign labor": lambda size: np.linspace(30, 10, size),  # Assuming a decreasing trend

        # Unique indicators for Overall_economy
        "GDP Growth Rate": lambda size: np.random.uniform(1, 5, size),
        "Unemployment Rate Trends": lambda size: np.random.uniform(3, 10, size),
        "Inflation Rate Changes": lambda size: np.random.uniform(0, 4, size),
        "Consumer Spending Patterns": lambda size: np.random.uniform(200, 500, size),
        "Foreign Direct Investment Flows": lambda size: np.random.uniform(100, 300, size),
        "Currency Strength and Exchange Rates": lambda size: np.random.uniform(0.8, 1.2, size),
        "Interest Rate Fluctuations": lambda size: np.random.uniform(0.5, 2, size),
        "Economic Policy Impact Assessment": lambda size: np.random.uniform(-2, 2, size), # Can be positive or negative
        "National Debt Levels": lambda size: np.linspace(1000, 1500, size),
        "Business Confidence Survey Results": lambda size: np.random.normal(loc=50, scale=10, size=size),


        # Unique indicators for Agriculture
        "Soil Moisture Levels": lambda size: np.random.uniform(10, 60, size),
        "Rainfall Averages vs Historical Data": lambda size: np.random.uniform(0, 200, size),
        "Temperature Anomalies": lambda size: np.random.normal(loc=20, scale=5, size=size),
        "Greeness Index (NDVI)": lambda size: np.random.uniform(0.3, 0.8, size),
        "Planting and Harvest Dates": lambda size: np.random.choice([100, 120, 140], size),
        "Crop Yield Forecasts and Actuals": lambda size: np.random.uniform(1000, 5000, size),
        "Water Usage Rates": lambda size: np.random.uniform(100, 500, size),
        "Agricultural Inputs (Seeds, Fertilizer)": lambda size: np.random.uniform(50, 150, size),
        "Commodity Price and Price Volatility": lambda size: np.random.uniform(20, 100, size),
        "Export Volumes and Destinations": lambda size: np.random.uniform(50, 300, size),
        "Food Stock Levels": lambda size: np.random.uniform(100, 500, size),
        "Labor Availability and Costs": lambda size: np.random.uniform(1000, 5000, size),
        "Farm Machinery Sales and Utilization Rates": lambda size: np.random.uniform(10, 50, size),
        "Energy Costs for Farming Operations": lambda size: np.random.uniform(5, 25, size),
        "Farm Loan Defaults and Support Levels": lambda size: np.random.uniform(1, 10, size),
        "Agricultural Subsidies and Support Levels": lambda size: np.random.uniform(100, 500, size),
        "Insurance Claim Rates": lambda size: np.random.uniform(0, 100, size),


        # Unique indicators for Construction
        "Building Permits Issued": lambda size: np.random.randint(100, 500, size),
        "Construction Output and Volume": lambda size: np.random.uniform(500, 1500, size),
        "Housing Starts and Completions": lambda size: np.random.randint(50, 300, size),
        "Infrastructure Project Pipelines": lambda size: np.random.choice([10, 20, 30, 40], size),
        "Material Costs Trends": lambda size: np.random.uniform(100, 200, size),
        "Construction Equipment Sales": lambda size: np.random.uniform(30, 80, size),
        "Labor Force Statistics in Construction": lambda size: np.random.uniform(1000, 3000, size),
        "Construction Loan Interest Rates": lambda size: np.random.uniform(1, 5, size),
        "Safety Incident Rates and Regulations Compliance": lambda size: np.random.uniform(0, 100, size),
        "Default among developers, contractors": lambda size: np.random.uniform(10, 100, size),
        "Online announcements of delayed projects": lambda size: np.random.randint(0, 100, size),
        "Construction work visa application": lambda size: np.random.randint(50, 500, size),
        "Level of wages by occupation": lambda size: np.linspace(3000, 5000, size),
        "Evacuees housing demand": lambda size: np.random.uniform(100, 1000, size),
        "Days on market": lambda size: np.random.uniform(30, 180, size),

        # Unique indicators for Manufacturing
        "Production Output Volume": lambda size: np.linspace(500, 1000, size),
        "Inventory Levels and Turnover Rates": lambda size: np.random.uniform(5, 20, size),
        "Manufacturing Employment Rates": lambda size: np.random.uniform(1000, 5000, size),
        "Machine Utilization Rates": lambda size: np.random.uniform(60, 90, size),
        "Input Costs": lambda size: np.random.uniform(50, 150, size),
        "Product Demand Forecasts": lambda size: np.random.uniform(100, 500, size),
        "Export and Import Volumes": lambda size: np.random.uniform(200, 500, size),
        "Factory Downtime and Efficiency Metrics": lambda size: np.random.uniform(0, 100, size), # Efficiency can be 0-100%
        "Supply Chain Disruption Impacts": lambda size: np.random.uniform(-10, 10, size), # Can be positive or negative
        "Quality Control Metrics": lambda size: np.random.uniform(80, 100, size), # Quality score as a percentage

        # Unique indicators for Retail
        "Consumer Foot Traffic Data": lambda size: np.random.randint(1000, 10000, size),
        "Sales Volume and Revenue Trends": lambda size: np.random.uniform(500, 2000, size),
        "Inventory Turnover Rates": lambda size: np.random.uniform(2, 10, size),
        "E-commerce Penetration and Growth": lambda size: np.random.uniform(0, 100, size),
        "Retail Price Inflation": lambda size: np.random.uniform(1, 5, size),
        "Customer Satisfaction and Loyalty Metrics": lambda size: np.random.uniform(50, 100, size),
        "Brand Value and Market Share": lambda size: np.random.uniform(5, 30, size),
        "Seasonal Sales Performance": lambda size: np.random.uniform(-20, 20, size),
        "Retail Space Costs": lambda size: np.random.uniform(10, 100, size),
        "Omnichannel Retail Adoption Rates": lambda size: np.random.uniform(0, 100, size),

        # Unique indicators for Health and Social Sector
        "Patient Admission Rates": lambda size: np.random.uniform(50, 500, size),
        "Healthcare Workforce Statistics": lambda size: np.random.uniform(1000, 5000, size),
        "Medical Equipment Utilization and Sales": lambda size: np.random.uniform(50, 200, size),
        "Healthcare Policy Changes and Impacts": lambda size: np.random.normal(loc=0, scale=1, size=size),
        "Public Health Expenditure": lambda size: np.linspace(500, 1500, size),
        "Pharmaceutical Sales and Innovation Rates": lambda size: np.random.uniform(100, 500, size),
        "Health Insurance Coverage Rates": lambda size: np.random.uniform(70, 95, size),
        "Disease Incidence and Prevalence Rates": lambda size: np.random.uniform(0, 100, size),
        "Telemedicine Adoption Trends": lambda size: np.random.uniform(0, 100, size),
        "Patient Outcome Statistics": lambda size: np.random.uniform(80, 100, size),

        # Unique indicators for Retail_Wholesale
        "Wholesale Sales Volumes": lambda size: np.random.uniform(1000, 7000, size),
        "B2B Customer Satisfaction Indices": lambda size: np.random.uniform(0, 100, size),
        "Inventory Carrying Costs": lambda size: np.random.uniform(10, 50, size),
        "Wholesale Market Price Trends": lambda size: np.random.uniform(-10, 10, size),
        "Retailer Demand Forecasts": lambda size: np.random.uniform(100, 500, size),
        "Distribution Network Efficiency": lambda size: np.random.uniform(75, 95, size),
        "Vendor Management Effectiveness": lambda size: np.random.uniform(0, 100, size),
        "Credit Terms and Payment Periods": lambda size: np.random.uniform(30, 90, size),
        "Return Rates and Processing Costs": lambda size: np.random.uniform(1, 10, size),
        "Trade Promotion Effectiveness": lambda size: np.random.uniform(0, 100, size),

        # Unique indicators for Education
        "Student Enrollment and Graduation Rates": lambda size: np.random.uniform(50, 500, size),
        "Education Funding Levels": lambda size: np.linspace(200, 500, size),
        "Teacher to Student Ratios": lambda size: np.random.uniform(10, 30, size),
        "Academic Performance Metrics": lambda size: np.random.uniform(0, 100, size),
        "Technology Adoption in Classrooms": lambda size: np.random.uniform(0, 100, size),
        "Education Infrastructure Investments": lambda size: np.linspace(100, 300, size),
        "Special Education Program Availability": lambda size: np.random.uniform(0, 100, size),
        "School Operation Costs": lambda size: np.random.uniform(100, 500, size),
        "Workforce Skills Gap Analysis": lambda size: np.random.uniform(0, 100, size),
        "Online Education Engagement Rates": lambda size: np.random.uniform(0, 100, size),

        # Unique indicators for Transportation and Storage
        "Freight Volumes and Transport Efficiency": lambda size: np.random.uniform(100, 1000, size),
        "Logistics Costs Trends": lambda size: np.random.uniform(5, 25, size),
        "Fuel Price Fluctuations and Impact": lambda size: np.random.normal(loc=1, scale=0.2, size=size),
        "Transportation Infrastructure Development": lambda size: np.random.choice([100, 200, 300], size),
        "Vehicle Fleet Age and Maintenance Costs": lambda size: np.random.uniform(1, 5, size),
        "Warehouse Space Availability and Utilization": lambda size: np.random.uniform(50, 200, size),
        "Carrier Performance Metrics": lambda size: np.random.uniform(75, 100, size),
        "Regulatory Changes Affecting Transportation": lambda size: np.random.uniform(0, 100, size),
        "Transportation Safety and Accident Rates": lambda size: np.random.uniform(0, 100, size),
        "Digitalization of Supply Chain Operations": lambda size: np.random.uniform(0, 100, size),

        # Shared indicators
        "Economic Growth Rate": lambda size: np.random.uniform(1, 5, size),
        "Unemployment Rate": lambda size: np.random.uniform(4, 10, size),
        "Inflation Rate": lambda size: np.random.uniform(0.1, 4, size),
        "Interest Rates": lambda size: np.random.uniform(0.5, 5, size),
        "Consumer Confidence": lambda size: np.random.uniform(20, 100, size),
        "Exchange Rates": lambda size: np.random.uniform(0.8, 1.5, size),

    }

    # Generate the data for the given indicator
    baseline_data = data_generators.get(indicator, lambda size: np.zeros(size))(num_weeks)
    baseline_data = baseline_data.astype(float)
    
    # Adding noise proportional to the linear components
    if indicator in ["GDP", "Level of wages", "Home Price Index", "National Debt Levels", 
                     "Public Health Expenditure", "Education Funding Levels", 
                     "Education Infrastructure Investments", "Raw material delays", 
                     "Government support program utilization", "Companies applied for chapter 11", 
                     "Percentage of foreign labor"]:
        noise_scale = 0.03  # 3% of the main component
        noise = np.random.normal(0, baseline_data * noise_scale, len(baseline_data))
        baseline_data += noise

    # Find the index of the closest date to the crisis start date
    crisis_start_date = datetime.date(2023, 10, 7)
    closest_date = min(dates, key=lambda date: abs(date - crisis_start_date))
    crisis_index = dates.index(closest_date)

    # Apply specific crisis impacts
    if indicator in ["Default among developers, contractors",
                     "Days on market",
                     "Companies applied for chapter 11",
                     "Level of wages by occupation",
                     "Evacuees housing demand",
                     "Online announcements of delayed projects",
                     "Home Price Index",
                    ]:
        baseline_data = apply_sharp_increase(baseline_data, crisis_index)

    elif indicator in ["Construction work visa application",
                       "Percentage of foreign labor",
                    ]:
        baseline_data = apply_sharp_decrease(baseline_data, crisis_index)

    # Normalize data to prevent negative values
    baseline_data = np.maximum(baseline_data, 0)

    return dates, baseline_data

def generate_reservist_data():
    """
    Example distribution - adjust based on your actual data or desired simulation
    """
    distribution = {
        "Agriculture": 5,
        "Construction": 30,
        "Manufacturing": 15,
        "Retail": 10,
        "Health_social_sector": 8,
        "Retail_Wholesale": 12,
        "Education": 5,
        "Transportation_and_storage": 15
    }
    return distribution

