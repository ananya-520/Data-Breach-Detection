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
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="Amoret@2801#"
POSTGRES_DB="FamousCompanyXYZ"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"

# Connect to PostgreSQL and store the output message
try:
    conn = psycopg2.connect(
        dbname = POSTGRES_DB,
        user = POSTGRES_USER,
        password= POSTGRES_PASSWORD,
        host= POSTGRES_HOST,
        port= POSTGRES_PORT
    )
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS brokerage_spike_alert (
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
    INSERT INTO brokerage_spike_alert (company_name, spike_amount, affected_time, alert_message)
    VALUES (%s, %s, %s, %s)
""", (', '.join(company_detected), float(average_spike), spike_column_name, output_message))

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()
    print("Data successfully inserted into PostgreSQL.")

except Exception as e:
    print("Error inserting into PostgreSQL:", e)
