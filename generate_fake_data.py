import pandas as pd
from faker import Faker
import random
import bcrypt

fake = Faker()
Faker.seed(42)  # Ensures reproducibility

departments = ["IT", "HR", "Finance", "Marketing", "Sales", "Operations"]

# Function to encrypt passwords
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

# Generate 100 fake employees with more personal data
data = []
for _ in range(100):
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    department = random.choice(departments)
    salary = random.randint(50000, 150000)
    address = fake.address().replace("\n", ", ")  # Make the address one line
    ssn = fake.ssn()
    bank_account = fake.iban()
    password = hash_password(fake.password())

    data.append({
        "ID": _ + 1,
        "Name": name,
        "Email": email,
        "Phone Number": phone,
        "Department": department,
        "Salary": salary,
        "Address": address,
        "SSN/National ID": ssn,
        "Bank Account": bank_account,
        "Hashed Password": password
    })

df = pd.DataFrame(data)
df.to_csv("fake_personal_company_data.csv", index=False)

print("Fake personal company data generated successfully!")
