import pandas as pd

# Read all sheets into a dictionary of DataFrames
all_sheets = pd.read_excel("hazlCombined.xlsx", sheet_name=None)

# Initialize a list to store all data
all_data = []

# Process each sheet
for sheet_name, df in all_sheets.items():
    # Rename columns to standard format (adjust if your headers are different)
    df.columns = ['Part Name', 'Part Number', 'Amount on Sheet Part']
    
    # Add sheet name as a column for reference (optional)
    df['Source Sheet'] = sheet_name
    
    # Append to master list
    all_data.append(df)

# Combine all sheets into one DataFrame
combined_df = pd.concat(all_data)

# Group by part number and name, summing amounts
bom_df = combined_df.groupby(['Part Number', 'Part Name'])['Amount on Sheet Part'].sum().reset_index()

# Sort by part number (optional)
bom_df = bom_df.sort_values('Part Number')

# Create a new Excel file with BOM
with pd.ExcelWriter('BOM.xlsx') as writer:
    bom_df.to_excel(writer, index=False, sheet_name='Consolidated BOM')
    
    # Add additional sheet with raw combined data (optional)
    combined_df.to_excel(writer, sheet_name='All Raw Data', index=False)

print("BOM created successfully!")
