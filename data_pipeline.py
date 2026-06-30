#importing libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

coffee = pd.read_csv('coffee.csv')

print("--- Dataset Shape ---")
print(coffee.shape)
print("\n--- Column Names ---")
print(coffee.columns)
print("\n--- Dataset Info ---")
# coffee.info() prints automatically, so we just run it directly
coffee.info()
print("\n--- Missing Values Count ---")
print(coffee.isnull().sum())
print("\n--- First 5 Rows ---")
print(coffee.head())

print("--- Attribute Description Value Counts ---")
print(coffee['Attribute_Description'].value_counts())

# Population file using

population = pd.read_csv('Population.csv')


print("--- Dataset Shape ---")
print(population.shape)

print("\n--- Dataset Info ---")
# .info() prints directly to the screen on its own
population.info()

print("\n--- First 5 Rows ---")
print(population.head())

codes = pd.read_excel('countries-codes.xlsx', engine='openpyxl')

print("--- Dataset Shape ---")
print(codes.shape)

print("\n--- Column Names ---")
print(codes.columns)

print("\n--- First 5 Rows ---")
print(codes.head())

# ******************************************************************************
# ** STEP 3: DATA ENGINEERING (CLEANING) **
# ******************************************************************************

# COFFEE CLEANING

# Filter the coffee DataFrame to only include rows where 'Attribute_Description' equals 'Domestic Consumption'
coffee = coffee[coffee['Attribute_Description'] == 'Domestic Consumption']
print("After filtering for Domestic Consumption:")
print(coffee)

# Select only the relevant columns: 'Country_Name', 'Market_Year', and 'Value'
coffee = coffee[['Country_Name', 'Market_Year', 'Value']]
print("\nAfter selecting relevant columns:")
print(coffee)

# Rename the columns for better readability
coffee.columns = ['country', 'year', 'consumption']
print("\nAfter renaming columns:")
print(coffee)

# Clean the 'country' column: convert to lowercase and strip whitespace
coffee['country'] = coffee['country'].str.lower().str.strip()
print("\nAfter cleaning the country column:")
print(coffee)

# Convert the 'year' column to integer type
coffee['year'] = coffee['year'].astype(int)
print("\nAfter converting year to integer:")
print(coffee)

# Convert the 'consumption' column to numeric type
coffee['consumption'] = pd.to_numeric(coffee['consumption'])
print("\nAfter converting consumption to numeric:")
print(coffee)

# Population Cleansing

population = population.melt(
    id_vars=['Country Name'],
    var_name='year',
    value_name='population'
)

population.columns = ['country', 'year', 'population']

population['country'] = population['country'].str.lower().str.strip()
population = population[population['year'].str.isnumeric()]
population['year'] = population['year'].astype(int)
population['population'] = pd.to_numeric(population['population'], errors='coerce')

#Country Code Cleaning

# Select only the relevant columns: 'LABEL EN' and 'ISO3 CODE'
codes = codes[['LABEL EN', 'ISO3 CODE']]
print("After selecting relevant columns:")
print(codes)

# Rename the columns for better readability
codes.columns = ['country', 'iso3_code']
print("\nAfter renaming columns:")
print(codes)

# Clean the 'country' column: convert to lowercase and strip whitespace
codes['country'] = codes['country'].str.lower().str.strip()
print("\nAfter cleaning the 'country' column:")
print(codes)

# Country Mapping

# Define the mapping dictionary
mapping = {
    'united states of america': 'united states',
    'russian federation': 'russia',
    'korea, republic of': 'south korea'
}

# Replace values in the 'country' column of the population DataFrame
population['country'] = population['country'].replace(mapping)
print("After replacing country names in the population DataFrame:")
print(population)

# Replace values in the 'country' column of the codes DataFrame
codes['country'] = codes['country'].replace(mapping)
print("\nAfter replacing country names in the codes DataFrame:")
print(codes)

# Removing Null & Duplicates

# Remove rows with null values in the population DataFrame
population = population.dropna()
print("After removing null values from the population DataFrame:")
print(population)

# Remove duplicate rows in the population DataFrame
population = population.drop_duplicates()
print("\nAfter removing duplicate rows from the population DataFrame:")
print(population)

# Remove rows with null values in the codes DataFrame
codes = codes.dropna()
print("\nAfter removing null values from the codes DataFrame:")
print(codes)

# Remove duplicate rows in the codes DataFrame
codes = codes.drop_duplicates()
print("\nAfter removing duplicate rows from the codes DataFrame:")
print(codes)

# Merge Data

# Merge the coffee DataFrame with the population DataFrame on 'country' and 'year' using an inner join
merged = coffee.merge(population, on=['country', 'year'], how='inner')
print("After merging coffee and population DataFrames:")
print(merged.head())

# Merge the resulting DataFrame with the codes DataFrame on 'country' using a left join
merged = merged.merge(codes, on='country', how='left')
print("\nAfter merging with codes DataFrame:")
print(merged.head())

# Feature Engineering

# Calculate coffee consumption per capita
merged['coffee_per_capita'] = merged['consumption'] / merged['population']
print("After calculating coffee consumption per capita:")
print(merged[['country', 'year', 'consumption', 'population', 'coffee_per_capita']].head())

# Fill missing values in the 'iso3_code' column with 'UNK'
merged['iso3_code'] = merged['iso3_code'].fillna('UNK')
print("\nAfter filling missing ISO3 codes with 'UNK':")
print(merged[['country', 'iso3_code']].head())

# Final Data

import os

# Define the directory path
directory = '../data'

# Check if the directory exists, and create it if it doesn't
if not os.path.exists(directory):
    os.makedirs(directory)

# Save the DataFrame to the CSV file
merged.to_csv('../data/final_cleaned.csv', index=False)
import os
print(os.getcwd())

merged.to_csv('final_cleaned.csv', index=False)\
