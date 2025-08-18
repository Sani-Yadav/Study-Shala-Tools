import pandas as pd
import os
from datetime import datetime, timedelta

# Define the directory where the sample file will be saved
STATIC_DIR = os.path.join('static', 'samples')
os.makedirs(STATIC_DIR, exist_ok=True)

# Create sample data
sample_data = [
    {
        'Username': 'student1',
        'First Name': 'John',
        'Last Name': 'Doe',
        'Email': 'john@example.com',
        'Student ID': 'STU001',
        'College': 'ABC College',
        'Course': 'BCA',
        'Year': '2023',
        'Contact Number': '9876543210',
        'Address': 'Delhi, India',
        'DOB': '2000-01-15'
    },
    {
        'Username': 'student2',
        'First Name': 'Jane',
        'Last Name': 'Smith',
        'Email': 'jane@example.com',
        'Student ID': 'STU002',
        'College': 'XYZ College',
        'Course': 'BTech',
        'Year': '2022',
        'Contact Number': '8765432109',
        'Address': 'Mumbai, India',
        'DOB': '2001-05-20'
    },
    # Add more sample entries
    {
        'Username': 'student3',
        'First Name': 'Amit',
        'Last Name': 'Kumar',
        'Email': 'amit@example.com',
        'Student ID': 'STU003',
        'College': 'PQR Institute',
        'Course': 'MCA',
        'Year': '2023',
        'Contact Number': '7654321098',
        'Address': 'Bangalore, India',
        'DOB': '1999-08-10'
    },
    {
        'Username': 'student4',
        'First Name': 'Priya',
        'Last Name': 'Sharma',
        'Email': 'priya@example.com',
        'Student ID': 'STU004',
        'College': 'LMN University',
        'Course': 'BSc',
        'Year': '2024',
        'Contact Number': '6543210987',
        'Address': 'Chennai, India',
        'DOB': '2002-03-25'
    },
    {
        'Username': 'student5',
        'First Name': 'Rahul',
        'Last Name': 'Singh',
        'Email': 'rahul@example.com',
        'Student ID': 'STU005',
        'College': 'ABC College',
        'Course': 'BBA',
        'Year': '2023',
        'Contact Number': '5432109876',
        'Address': 'Hyderabad, India',
        'DOB': '2001-11-05'
    }
]

# Create DataFrame
df = pd.DataFrame(sample_data)

# Save to Excel
file_path = os.path.join(STATIC_DIR, 'sample_id_cards.xlsx')
df.to_excel(file_path, index=False)

print(f"Sample Excel file created at: {file_path}")