import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetch PostgreSQL credentials from .env
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Step 1: Connect to PostgreSQL Database
try:
    conn = psycopg2.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    print(f"Connected to database {POSTGRES_DB} as {POSTGRES_USER}")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

cursor = conn.cursor()

# Step 2: Read the CSV File
csv_file = "fake_personal_company_data.csv"  # Ensure the correct file path
try:
    df = pd.read_csv(csv_file)
    print(f"Loaded CSV with {df.shape[0]} rows and {df.shape[1]} columns.")
except Exception as e:
    print(f"Error reading CSV file: {e}")
    conn.close()
    exit()

# Step 3: Insert CSV Data into PostgreSQL Table
insert_query = """
    INSERT INTO company_data (
        Name, Email, "Phone Number", Department, Salary, Address, 
        "SSN", "Bank Account", "Hashed Password"
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

try:
    for index, row in df.iterrows():
        cursor.execute(insert_query, (
            row['Name'], row['Email'], row['Phone Number'], row['Department'], 
            row['Salary'], row['Address'], row['SSN/National ID'], 
            row['Bank Account'], row['Hashed Password']
        ))
    
    # Step 4: Commit the Transaction
    conn.commit()
    print("CSV data has been successfully imported into PostgreSQL!")

except Exception as e:
    print(f"Error inserting data: {e}")
    conn.rollback()

# Step 5: Close the Connection
cursor.close()
conn.close()
