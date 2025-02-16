from faker import Faker
import random

fake = Faker()

def generate_brokerage_data(num_entries=10):
    # List to hold fake data
    data = []
    
    # Example company industries (you can expand this list)
    industries = ['Tech', 'Healthcare', 'Finance', 'Retail', 'Real Estate', 'Marketing', 'Telecom', 'Energy']

    for _ in range(num_entries):
        company_name = fake.company()
        industry = random.choice(industries)
        data_received = random.choice(['Daily', 'Weekly', 'Monthly', 'Annually'])
        data_amount = round(random.uniform(5.0, 5000.0), 2)  # Random data between 5GB to 5000GB
        
        company_data = {
            "Company Name": company_name,
            "Industry": industry,
            "Data Received": data_received,
            "Data Amount (GB)": data_amount
        }
        
        data.append(company_data)
    
    return data

# Generate 10 entries of fake brokerage company data
brokerage_data = generate_brokerage_data(10)

# Print the generated data
for entry in brokerage_data:
    print(entry)
