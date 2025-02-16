# Data Breach Detection

## Introduction

Data Breach Detection is a Flask-based web application designed to enhance data security by encrypting sensitive information, detecting breaches, and managing authentication. The project also includes a data processing script that analyzes numerical datasets to identify anomalies. Additionally, we generate fake sample data to simulate potential breach scenarios and test our detection mechanisms.

## Features

- **Flask API** for secure data handling.
- **PostgreSQL database integration** for secure data storage.
- **Data breach detection mechanism** through statistical analysis.
- **CSV Data Processing** script for computing standard deviations in data.
- **Role-based access control** for different user permissions.
- **Logging and monitoring** to track data access.
- **Fake Data Generation** for testing breach detection mechanisms.

## Installation Guide

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- PostgreSQL
- pip (Python package manager)
- Flask and required dependencies

### Setup

1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/data-breach-detection.git
   cd data-breach-detection
   ```
2. Create a virtual environment and activate it:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Create a `.env` file and add:
   ```
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   SECRET_ENCRYPTION_KEY=your_encryption_key
   ```

## Running the Application

1. Start PostgreSQL and ensure your database is set up.
2. Run database migrations (if applicable):
   ```sh
   flask db upgrade
   ```
3. Run the Flask application:
   ```sh
   python app.py
   ```
4. Access the web app at `http://127.0.0.1:5000/`.

## Data Processing and Fake Data Generation

### Standard Deviation Calculation

The script `calculating_sd_normal.py` processes CSV files to compute standard deviations:

```sh
python calculating_sd_normal.py
```

- Reads `brokerage_company_data_1.5h.csv`.
- Calculates row-wise standard deviations.
- Saves results in `brokerage_company_data_with_std.csv`.

### Fake Data Generation

To simulate realistic breach scenarios, we generate fake sample data. The script creates randomized records to test encryption, storage, and breach detection mechanisms effectively.

```sh
python generate_fake_data.py
```

- Generates synthetic user and transaction data.
- Stores the data securely in the PostgreSQL database.
- Ensures controlled breach simulations for testing.

## Security Considerations

- Store database credentials securely using environment variables.
- Encrypt all sensitive data before storing it in the database.
- Implement rate limiting to prevent brute-force attacks.
- Maintain detailed logs for audit purposes.
- Regularly test detection mechanisms using generated fake data.

## Future Improvements

- Implement real-time data breach alerts with AI-driven detection.
- Extend API to support data encryption from the frontend.
- Improve machine learning-based breach detection.
- Develop a user-friendly dashboard for security monitoring.
- Add multi-factor authentication for enhanced security.

## License

MIT License. See `LICENSE` for details.

## Contributors

- Your Name (@your-github)
- Other Contributors

