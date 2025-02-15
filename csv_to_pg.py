import pandas as pd
import psycopg2
from psycopg2 import sql

# Step 1: Connect to PostgreSQL Database
conn = psycopg2.connect(
    dbname="company_data",  # Your database name
    user="postgres",        # Your username
    password="your_password",  # Your password
    host="localhost",       # Host (use 'localhost' if local)
    port="5432"             # Default PostgreSQL port
)

cursor = conn.cursor()

# Step 2: Read the CSV File
csv_file = "fake_personal_company_data.csv"  # Path to your CSV
df = pd.read_csv(csv_file)

# Step 3: Insert CSV Data into PostgreSQL Table
for index, row in df.iterrows():
    insert_query = sql.SQL("""
        INSERT INTO company_data (
            Name, Email, "Phone Number", Department, Salary, Address, "SSN/National ID", "Bank Account", "Hashed Password"
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """)
    
    cursor.execute(insert_query, (
        row['Name'], row['Email'], row['Phone Number'], row['Department'], 
        row['Salary'], row['Address'], row['SSN/National ID'], row['Bank Account'], row['Hashed Password']
    ))

# Step 4: Commit the Transaction
conn.commit()

# Step 5: Close the Connection
cursor.close()
conn.close()

print("CSV data has been successfully imported into PostgreSQL!")
