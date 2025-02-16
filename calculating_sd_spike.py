import pandas as pd

# Load the CSV file
file_path = "brokerage_company_data_spike.csv"  # Update with your actual file path
df = pd.read_csv(file_path)

# Calculate standard deviation for each row (excluding non-numeric columns)
df['Row_Std_Dev'] = df.select_dtypes(include=['number']).std(axis=1)

# Save the new DataFrame to a new file
new_file_path = "brokerage_company_data_spike_with_std.csv"
df.to_csv(new_file_path, index=False)

print(f"Processed file saved as: {new_file_path}")
