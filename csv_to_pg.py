# import pandas as pd
# import psycopg2
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Fetch PostgreSQL credentials from .env
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# # Step 1: Connect to PostgreSQL Database
# try:
#     conn = psycopg2.connect(
#         user=POSTGRES_USER,
#         password=POSTGRES_PASSWORD,
#         dbname=POSTGRES_DB,
#         host=POSTGRES_HOST,
#         port=POSTGRES_PORT
#     )
#     print(f"Connected to database {POSTGRES_DB} as {POSTGRES_USER}")
# except Exception as e:
#     print(f"Error connecting to database: {e}")
#     exit()

# cursor = conn.cursor()

# # Step 2: Read the CSV File
# csv_file = "fake_personal_company_data.csv"  # Ensure the correct file path
# try:
#     df = pd.read_csv(csv_file)
#     print(f"Loaded CSV with {df.shape[0]} rows and {df.shape[1]} columns.")
# except Exception as e:
#     print(f"Error reading CSV file: {e}")
#     conn.close()
#     exit()

# # Step 3: Insert CSV Data into PostgreSQL Table
# insert_query = """
#     INSERT INTO company_data (
#         Name, Email, "Phone Number", Department, Salary, Address, 
#         "SSN", "Bank Account", "Hashed Password"
#     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
# """

# try:
#     for index, row in df.iterrows():
#         cursor.execute(insert_query, (
#             row['Name'], row['Email'], row['Phone Number'], row['Department'], 
#             row['Salary'], row['Address'], row['SSN'], 
#             row['Bank Account'], row['Hashed Password']
#         ))
    
#     # Step 4: Commit the Transaction
#     conn.commit()
#     print("CSV data has been successfully imported into PostgreSQL!")

# except Exception as e:
#     print(f"Error inserting data: {e}")
#     conn.rollback()

# # Step 5: Close the Connection
# cursor.close()
# conn.close()


import pandas as pd
import psycopg2

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

# Identify the company (assuming a "Company Name" column exists)
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

# PostgreSQL Database Credentials
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_HOST = "your_db_host"
DB_PORT = "your_db_port"

# Connect to PostgreSQL and store the output message
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS data_spike_alerts (
            id SERIAL PRIMARY KEY,
            company_name TEXT,
            spike_amount FLOAT,
            affected_time TEXT,
            alert_message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert the data
    cur.execute("""
        INSERT INTO data_spike_alerts (company_name, spike_amount, affected_time, alert_message)
        VALUES (%s, %s, %s, %s)
    """, (', '.join(company_detected), average_spike, spike_column_name, output_message))

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()
    print("Data successfully inserted into PostgreSQL.")

except Exception as e:
    print("Error inserting into PostgreSQL:", e)
