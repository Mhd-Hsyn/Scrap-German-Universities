import csv
import json

with open('all_university_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# Define the columns you need
columns = ["name", "logo", "web_url", "description", "High school type", "address", "phone", "email"]

# Open a CSV file to write to
with open('universities.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=columns)

    # Write the header
    writer.writeheader()

    # Write the rows
    for item in data:
        row = {
            "name": item.get("name"),
            "logo": item.get("logo"),
            "web_url": item.get("web_url", ""),
            "description": item.get("description", ""),
            "High school type": item.get("facts", {}).get("High school type", ""),
            "address": item.get("contact_info", {}).get("address", ""),
            "phone": item.get("contact_info", {}).get("phone", ""),
            "email": item.get("contact_info", {}).get("email", "")
        }
        writer.writerow(row)

print("CSV file created successfully!")
