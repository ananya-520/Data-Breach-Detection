from faker import Faker
import random
import csv

fake = Faker()

def generate_brokerage_data(num_entries=10, file_path="brokerage_company_data.csv"):
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
    
    # Save the generated brokerage data into a CSV file
    header = ["Company Name", "Industry", "Data Received", "Data Amount (GB)"]

    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

# Example usage
file_path = 'brokerage_company_data.csv'
generate_brokerage_data(10, file_path)

print(f"Data has been saved to {file_path}")
