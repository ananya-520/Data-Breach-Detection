# # import math
# # # Identify if the value from db is within standard deviation
# # x=35   #This value is modified based on latest data from db
# # sd=4
# # avg=30
# # #Code to identify likelihood of data breach
# # if x>avg+1*sd:
# #     if x > 2*sd+avg:
# #         likelihood=3
# #         #Return a message to front end requesting mod team to verify
# #     elif x>1.75*sd+avg:
# #         likelihood=2
# #         #Return a message to front end saying medium priotiy
# #     elif x>1.5*sd+avg:
# #         likelihood=1
# #         #Message saying low possiblity of a data breach 
# #     else:
# #         likelihood=0
# #         #Message saying higher than normal but little to no possiblity of data breach
# # import pandas as pd

# # df = pd.read_csv('fake_personal_company_data.csv')
# # print(df)  # Displays as a DataFrame




# import pandas as pd
# import numpy as np

# # Load the CSV file
# file_path = "brokerage_company_data.csv"  # Update this with the correct path
# df = pd.read_csv(file_path)

# # Function to compute standard deviation based on data frequency
# def compute_std(row):
#     avg_data = row["Data Amount (GB)"]
#     frequency = row["Data Received"]

#     if frequency == "Daily":
#         data_points = np.full(30, avg_data)  # 30 daily values per month
#     elif frequency == "Weekly":
#         data_points = np.full(4, avg_data)   # 4 weekly values per month
#     elif frequency == "Monthly":
#         data_points = np.array([avg_data])   # 1 value per month
#     elif frequency == "Annually":
#         data_points = np.array([avg_data])   # 1 value per year
#     else:
#         return np.nan  # Handle unexpected cases

#     return np.std(data_points, ddof=1) if len(data_points) > 1 else 0

# # Apply function to each row
# df["Standard Deviation"] = df.apply(compute_std, axis=1)

# # Display results
# print(df[["Company Name", "Industry", "Data Received", "Data Amount (GB)", "Standard Deviation"]])



# import pandas as pd

# # Load the CSV file
# file_path = "brokerage_company_data_1.5h.csv"  # Update with your actual file path
# df = pd.read_csv(file_path)

# # Calculate standard deviation for each row (excluding non-numeric columns)
# df['Row_Std_Dev'] = df.select_dtypes(include=['number']).std(axis=1)

# # Save the new DataFrame to a new file
# new_file_path = "brokerage_company_data_with_std.csv"
# df.to_csv(new_file_path, index=False)

# print(f"Processed file saved as: {new_file_path}")

import pandas as pd

# Load the two CSV files
file_path_regular = "brokerage_company_data_1.5h.csv"  # Regular data file
file_path_spike = "brokerage_company_data_spike.csv"  # File with potential spikes

df_regular = pd.read_csv(file_path_regular)
df_spike = pd.read_csv(file_path_spike)

# Ensure both dataframes have the same structure
if not df_regular.columns.equals(df_spike.columns):
    raise ValueError("The two CSV files have different column structures.")

# Calculate standard deviation for each row (excluding non-numeric columns)
df_regular['Row_Std_Dev'] = df_regular.select_dtypes(include=['number']).std(axis=1)
df_spike['Row_Std_Dev'] = df_spike.select_dtypes(include=['number']).std(axis=1)

# Compare standard deviations and detect spikes
df_spike['Spike_Amount'] = df_spike['Row_Std_Dev'] - df_regular['Row_Std_Dev']
df_spike['Spike_Detected'] = df_spike['Spike_Amount'] > 1  # Threshold for spike detection

# Identify the columns where the spike is most significant
numeric_cols = df_regular.select_dtypes(include=['number']).columns
spike_columns = (df_spike[numeric_cols] - df_regular[numeric_cols]).abs().mean(axis=0)
spike_column_name = spike_columns.idxmax()  # Column with the highest average spike

# Identify the company (assuming a "Company" column exists)
if "Company Name" in df_spike.columns:
    company_detected = df_spike.loc[df_spike['Spike_Detected'], 'Company Name'].unique()
else:
    company_detected = ["Unknown"]

# Compute the average spike
average_spike = df_spike.loc[df_spike['Spike_Detected'], 'Spike_Amount'].mean()

# Generate output message
output_message = f"Company detected with unusual data influx: {', '.join(company_detected)}\n" \
                 f"Average spike amount: {average_spike:.2f} GB\n" \
                 f"Most affected time: {spike_column_name}"

print(output_message)
