# CO2 Emissions Analysis with Pandas

# Goal: Clean the data, find the top emitting countries in most recent year

import pandas as pd
import matplotlib.pyplot as plt

# 1 Loading and inspecting
df = pd.read_csv('owid-co2-data.csv')

print(df.info())
print(df.columns)
print(df.head(277))
print(df.tail(10))

# Notes:
# 79 columns, 50191 rows
# A lot of NaN in most of the columns
# Each country has ~274 entries (from 1750 to 2023)
# Some entries are regions (like 'Africa', 'Asia'), not countries
# these could be omitted by excluding entries without iso code of country

#new_df = df["iso_code"].dropna() # this just gives us one column without NaN
#print(new_df)
#print(new_df.info())

# 2 Removing rows without iso code -> therefore not real countries
new_df = df.dropna(subset=["iso_code"])
print(df['co2'].isna().sum())

# Notes:
# isna() would give False or True for every entry, sum will sum up F and T
# after dropping rows index could be reseted if needed with new_df = new_df.reset_index(drop=True)
# why drop=True? otherwise it saves the old index as a new column

# 3 Filtering out the most recent year
latest_year = new_df["year"].max()
latest_df = new_df[new_df["year"] == latest_year].reset_index(drop=True)

# Dropping rows with missing data
latest_df = latest_df.dropna(subset=['co2', 'co2_per_capita'])

# 5 Getting Top 10 CO2 emitters
top_emitters = latest_df[['country', 'co2', 'co2_per_capita']].sort_values(by='co2', ascending=False).head(10)
print(top_emitters.to_string())

# Getting Top 10 CO2 emitters per capita
top_emitters_per_capita = latest_df[['country','co2', 'co2_per_capita']].sort_values(by='co2_per_capita', ascending=False).head(10)
print(top_emitters_per_capita.to_string())

# 6 Visualizing with bar plot
top_emitters.plot(kind='bar', x='country', y='co2', title='Top 10 CO2 Emitters')
plt.tight_layout()
plt.show()

# Insight:
# Total emissions are dominated by large economies like China, the US, and India.
# Per capita emissions highlight wealthy, small-population countries (Qatar, Brunei, etc.)
# Different conclusions depending on which metric we look at.

# 7 Combining both groups into on DF and sorting by total emissions to showcase differences
combined_df = pd.concat([top_emitters, top_emitters_per_capita]).sort_values(by='co2', ascending=False)
print(combined_df.to_string())



# TODO: practicing loc and iloc

# iloc - index location, gives the row at position X
# uses number-based indexing, always integers, starts from 0 - like a list
print(combined_df.iloc[:3]) # 0, 1, 2 -> without 3
print(df.iloc[1:5]) # without 5 so rows 1, 2, 3 and 4

# loc - label based, gives the row with index label X
# uses actual labels (like names or years), can be integers if index is integer-labeled
# df.loc[2023]    # Row with index label = 2023
# df.loc['Germany']   # If country is set as index
# df.loc[[0, 2, 4]]   # If those are index labels, not positions!

# TODO: familiarize with boolean masks

# series of  True/False values that we use to filter rows in a DataFrame
mask = latest_df.co2 > 800
df_filtered = latest_df[mask]
print(df_filtered)

# combining boolean masks with loc
df = pd.DataFrame({
    'country': ['China', 'USA', 'India', 'Germany'],
    'co2': [11902, 4911, 3062, 596],
    'co2_per_capita': [8.5, 15.5, 2.2, 9.8]
})

# df.loc[df['co2'] > 3000] == df[df['co2'] > 3000] but it gives option to select columns
df_new = df.loc[df['co2'] > 3000, ['country', 'co2']]
print(df_new)