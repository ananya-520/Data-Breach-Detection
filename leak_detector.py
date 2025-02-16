import pandas as pd
import psycopg2

# Database connection details
db_config = {
    "host": "localhost",
    "port": "5432",
    "dbname": "FamousCompanyXYZ",
    "user": "postgres",
    "password": "Amoret@2801#"
}

def compare_csv_files(file1_path, file2_path, db_config):
    # Load data
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)
    
    # Standardize column names for comparison
    df1_renamed = df1.rename(columns={"Phone Number": "Phone", "SSN/National ID": "SSN"})
    common_columns = ["Name", "Email", "Phone", "SSN"]
    
    # Extract relevant data
    df1_common = df1_renamed[common_columns]
    df2_common = df2[common_columns]
    
    # Find matches and differences
    matches = df1_common.merge(df2_common, on=common_columns, how="inner")
    differences = pd.concat([df1_common, df2_common]).drop_duplicates(keep=False)

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"]
    )
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            Name TEXT,
            Email TEXT,
            Phone TEXT,
            SSN TEXT
        );
        CREATE TABLE IF NOT EXISTS differences (
            Name TEXT,
            Email TEXT,
            Phone TEXT,
            SSN TEXT
        );
    """)
    conn.commit()

    # Insert matches into the database
    for _, row in matches.iterrows():
        cursor.execute("""
            INSERT INTO matches (Name, Email, Phone, SSN) 
            VALUES (%s, %s, %s, %s)
        """, (row["Name"], row["Email"], row["Phone"], row["SSN"]))

    # Insert differences into the database
    for _, row in differences.iterrows():
        cursor.execute("""
            INSERT INTO differences (Name, Email, Phone, SSN) 
            VALUES (%s, %s, %s, %s)
        """, (row["Name"], row["Email"], row["Phone"], row["SSN"]))

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Exact Matches: {len(matches)} records uploaded to 'matches' table.")
    print(f"Differences: {len(differences)} records uploaded to 'differences' table.")

# Example usage
file1 = "./fake_personal_company_data.csv"
file2 = "./brokerage_data.csv"
compare_csv_files(file1, file2, db_config)
