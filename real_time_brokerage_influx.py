from faker import Faker
import random
import pandas as pd
import numpy as np

fake = Faker()

def generate_brokerage_data(num_entries=10):
    data = []
    industries = ['Tech', 'Healthcare', 'Finance', 'Retail', 'Real Estate', 'Marketing', 'Telecom', 'Energy']

    spike_row = random.randint(0, num_entries - 1)  # Choose a random row to spike

    for i in range(num_entries):
        company_name = fake.company()
        industry = random.choice(industries)
        data_received = "Every 1.5 Hours"

        # Generate base data amount
        base_data_amount = round(random.uniform(5.0, 5000.0), 2)

        # Generate 16 data points with slight variations (SD < 2)
        data_amounts = np.random.normal(loc=base_data_amount, scale=1, size=16)
        data_amounts = np.round(data_amounts, 2)

        # Introduce a massive spike in one row
        if i == spike_row:
            spike_index = random.randint(0, 15)  # Choose a random column to spike
            data_amounts[spike_index] *= random.uniform(3, 10)  # Multiply by 3x to 10x

        # Store in dictionary
        company_data = {
            "Company Name": company_name,
            "Industry": industry,
            "Data Received": data_received
        }
        
        # Add generated data amount columns
        for j in range(16):
            company_data[f"Data Amount (1.5h) {j+1}"] = data_amounts[j]

        data.append(company_data)

    return data

# Generate 10 entries of fake brokerage company data
brokerage_data = generate_brokerage_data(10)

# Convert to DataFrame
df = pd.DataFrame(brokerage_data)

# Save to CSV
output_file = "brokerage_company_data_spike.csv"
df.to_csv(output_file, index=False)

# Print first few rows
print(df.head())
