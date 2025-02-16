from faker import Faker
import random
import pandas as pd
import numpy as np

fake = Faker()

def generate_brokerage_data(num_entries=10):
    data = []
    industries = ['Tech', 'Healthcare', 'Finance', 'Retail', 'Real Estate', 'Marketing', 'Telecom', 'Energy']

    for _ in range(num_entries):
        company_name = fake.company()
        industry = random.choice(industries)
        data_received = "Every 1.5 Hours"

        # Generate a base data amount
        base_data_amount = round(random.uniform(5.0, 5000.0), 2)

        # Create 16 columns for 1.5-hour intervals with slight variation
        data_amounts = np.random.normal(loc=base_data_amount, scale=1, size=16)  # Mean = base_data_amount, SD < 2
        data_amounts = np.round(data_amounts, 2)  # Round values to 2 decimal places

        # Store in dictionary
        company_data = {
            "Company Name": company_name,
            "Industry": industry,
            "Data Received": data_received
        }
        
        # Add generated data amount columns
        for i in range(16):
            company_data[f"Data Amount (1.5h) {i+1}"] = data_amounts[i]

        data.append(company_data)

    return data

# Generate 10 entries of fake brokerage company data
brokerage_data = generate_brokerage_data(10)

# Convert to DataFrame
df = pd.DataFrame(brokerage_data)

# Save to CSV
output_file = "brokerage_company_data_1.5h.csv"
df.to_csv(output_file, index=False)

# Print first few rows
print(df.head())
