import pandas as pd

# Define the data for each section
years_in_ARR = {
    "ARR Phase": ["0-10M", "10-20M", "20-40M", "40-80M", "80-120M"],
    "Leading": [1.00, 1.00, 1.00, 1.00, 1.00],
    "Average": [5.08, 1.10, 1.20, 1.50, 1.17],
    "Lagging": [8.00, 2.00, 2.00, 3.00, 2.00]
}

average_sales_speed = {
    "ARR Phase": ["0-10M", "10-20M", "20-40M", "40-80M", "80-120M"],
    "Average": [4, 1.33, 1, 1.33, 1.33]
}

average_tech_speed = {
    "ARR Phase": ["0-10M", "10-20M", "20-40M", "40-80M", "80-120M"],
    "Tech Led Average": [6.8, 1, 1.25, 1.75, 1]
}

average_product_speed = {
    "ARR Phase": ["0-10M", "10-20M", "20-40M", "40-80M", "80-120M"],
    "Average": [4.33, 1, 1.5, 1, 1.33]
}

average_headcount = {
    "ARR Phase": ["0-10M", "10-20M", "20-40M", "40-80M", "80-120M", ">120M"],
    "Product Led": [63.87, 106.67, 245, 505, 502.75, 981.39],
    "Sales Led": [132.48, 379.5, 601.33, 854.33, 764.67, 1099.39],
    "Tech Led": [61.97, 315.5, 306, 556.17, 779.6, 1104.1]
}

headcount_timeline = {
    "Time": ["2 years before", "1 year before", "First Large/Account Enterprise", "1 year post", "2 years post"],
    "Overall": [153.5, 221.75, 322.75, 467, 538.25]
}

attrition_mna = {
    "Time": ["2 years before", "1 year before", "M&A", "1 year post", "2 years post"],
    "Attrition": ["10%", "11%", "12%", "11%", "16%"]
}

attrition_product_launch = {
    "Time": ["2 years before", "1 year before", "New Product Launch", "1 year post"],
    "Attrition": ["13%", "9%", "8%", "8%"]
}

attrition_geo_expansion = {
    "Time": ["2 years before", "1 year before", "Geographical Expansion", "1 year post", "2 years post"],
    "Overall": [215.33, 299.83, 443.67, 624.67, 806.67]
}

leadership_geo_expansion = {
    "Time": ["2 years before", "1 year before", "Geographical Expansion", "1 year post", "2 years post"],
    "Leadership": [55.1, 77.72, 113.47, 162.15, 222.68]
}

# Create DataFrames
df_years_in_ARR = pd.DataFrame(years_in_ARR)
df_average_sales_speed = pd.DataFrame(average_sales_speed)
df_average_tech_speed = pd.DataFrame(average_tech_speed)
df_average_product_speed = pd.DataFrame(average_product_speed)
df_average_headcount = pd.DataFrame(average_headcount)
df_headcount_timeline = pd.DataFrame(headcount_timeline)
df_attrition_mna = pd.DataFrame(attrition_mna)
df_attrition_product_launch = pd.DataFrame(attrition_product_launch)
df_attrition_geo_expansion = pd.DataFrame(attrition_geo_expansion)
df_leadership_geo_expansion = pd.DataFrame(leadership_geo_expansion)

# Creating an Excel writer
with pd.ExcelWriter('./data/business_analysis_data.xlsx') as writer:
    df_years_in_ARR.to_excel(writer, sheet_name='Years in ARR', index=False)
    df_average_sales_speed.to_excel(writer, sheet_name='Average Sales Speed', index=False)
    df_average_tech_speed.to_excel(writer, sheet_name='Average Tech Speed', index=False)
    df_average_product_speed.to_excel(writer, sheet_name='Average Product Speed', index=False)
    df_average_headcount.to_excel(writer, sheet_name='Average Headcount', index=False)
    df_headcount_timeline.to_excel(writer, sheet_name='Headcount Timeline', index=False)
    df_attrition_mna.to_excel(writer, sheet_name='Attrition M&A', index=False)
    df_attrition_product_launch.to_excel(writer, sheet_name='Attrition Product Launch', index=False)
    df_attrition_geo_expansion.to_excel(writer, sheet_name='Attrition Geo Expansion', index=False)
    df_leadership_geo_expansion.to_excel(writer, sheet_name='Leadership Geo Expansion', index=False)

# The Excel file 'business_analysis_data.xlsx' will be saved in your current working directory.
