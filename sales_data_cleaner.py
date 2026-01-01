# %%
#SALES DATA CLEANER AND REPORT GENERATOR

#Importing the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import isnull

#Phase 1: Loading the csv file
print('Loading the Dataset...')
df_sales_dirty = pd.read_csv("retail_store_sales.csv")
original_rows = len(df_sales_dirty)



#Phase 2: Building the reference dictionaries
#Finding the rows that have NO duplicate values
valid_items = df_sales_dirty.dropna(subset=['Category', 'Price Per Unit', 'Item'])

#Removing ducplicates so that we have a clean list of unique products
reference_table = valid_items[['Category', 'Price Per Unit', 'Item']].drop_duplicates()

#Create Dictionaries
#Map 1: lookup Item if we know the Category + Price
category_price_to_item_map = reference_table.set_index(['Category', 'Price Per Unit'])['Item'].to_dict()

#Map 2: Lookup Price if we know the Item
item_to_price_map = reference_table.set_index('Item')['Price Per Unit'].to_dict()



#Phase 3: Reconstruction the dataset
#A: recover/fix the prices

#1. Try to find Price using Item Name(Using Map 2)
mask_has_item = df_sales_dirty['Price Per Unit'].isnull() & df_sales_dirty['Item'].notnull()
df_sales_dirty.loc[mask_has_item, 'Price Per Unit'] = df_sales_dirty.loc[mask_has_item,'Item'].map(item_to_price_map)

#2. If that didn't work try to calculate Price using Math (Total/Quantity)
mask_math = df_sales_dirty['Price Per Unit'].isnull() & df_sales_dirty['Quantity'].notnull() & df_sales_dirty['Total Spent'].notnull()
df_sales_dirty.loc[mask_math, 'Price Per Unit'] = df_sales_dirty.loc[mask_math, 'Total Spent']/df_sales_dirty.loc[mask_math, 'Quantity']


#B: fix the Item names
#1. Try to find the Item using the Price Per Unit and Category(Using Map 1)
mask_has_price_category = df_sales_dirty['Price Per Unit'].notnull() & df_sales_dirty['Category'].notnull() & df_sales_dirty['Item'].isnull()
df_sales_dirty.loc[mask_has_price_category, 'Item'] = df_sales_dirty.loc[mask_has_price_category].set_index(['Price Per Unit', 'Category']).index.map(category_price_to_item_map)


#C. Fixing the Totals
# Now that Price is fixed we can  multiply Price * Quantity
mask_total = df_sales_dirty['Total Spent'].isnull() & df_sales_dirty['Price Per Unit'].notnull() & df_sales_dirty['Quantity'].notnull()
df_sales_dirty.loc[mask_total, 'Total Spent'] = df_sales_dirty.loc[mask_total, 'Price Per Unit'] * df_sales_dirty.loc[mask_total, 'Quantity']



#Phase 4
#Removing the records that could not be recovered

#1. Droping dead rows
df_clean = df_sales_dirty.dropna(subset=['Total Spent', 'Price Per Unit', 'Quantity', 'Item']).copy()

#2. Standardizing the Formats
#Date
df_clean['Transaction Date'] = pd.to_datetime(df_clean['Transaction Date'])

#3. Discount applied(True/False)
df_clean['Discount Applied'] = df_clean['Discount Applied'].fillna(False).astype(bool)

#4. Counting the number of records removed
dropped_rows = original_rows - len(df_clean)



#Phase 5
# Validating wheteher the changes actually make sense

#Calculating the difference between the listed total and the calculated total
math_check = (df_clean['Price Per Unit'] * df_clean['Quantity']) - df_clean['Total Spent']

#Using assert the check if the diference is zero(effectively)
assert  (math_check.abs() < 0.01).all(), "CRITICAL ERROR: Math mismatch found!"

df_clean.head(10)



#Phase 6
#Analysis and Reporting
#Calculating KPIs
total_revenue   = df_clean['Total Spent'].sum()
online_rev = df_clean[df_clean['Location'] == 'Online']['Total Spent'].sum()
store_rev = df_clean[df_clean['Location'] == 'In-store']['Total Spent'].sum()
avg_full_price = df_clean[df_clean['Discount Applied'] == False]['Total Spent'].mean()
avg_dicounted = df_clean[df_clean['Discount Applied'] == True]['Total Spent'].mean()
top_category = df_clean['Category'].value_counts().idxmax()

#Creating the report
report = f"""
======== RETAIL PERFORMANCE REPORT ========
Original Rows:  {original_rows}
Cleaned Rows:   {len(df_clean)} (Dropped {dropped_rows} unrecoverable)
-------------------------------------------
Total Revenue:  R{total_revenue}
    - Online:   R{online_rev}
    - In-Store: R{store_rev}
-------------------------------------------
Average Spent:
    -Full Price: R{avg_full_price: .2f}
    -Discounted: R{avg_dicounted: .2f}
-------------------------------------------
Top Category:   "{top_category}"
-------------------------------------------
Validation: PASSED (Total == Price * Qty)
===========================================
"""
print(report) 
print("Files saved: 'retail_sales_clean.csv', 'retail_report.txt'") 

# Save Report
with open('retail_report.txt', 'w') as f:
    f.write(report)
        
# Save Cleaned Data
df_clean.to_csv('retail_sales_clean.csv', index=False)



#Phase 7
#Visualizing the results
pivot = df_clean.groupby(['Category', 'Location'])['Total Spent'].sum().unstack()
pivot.plot(kind='bar', figsize=(10, 6))
plt.title('Total Sales by Category and Location')
plt.ylabel('Sales (R)')
plt.tight_layout()
plt.savefig('sales_chart.png') # Saving instead of showing
print("Chart saved: 'sales_chart.png'")

