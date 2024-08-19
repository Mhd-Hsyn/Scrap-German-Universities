import csv
import json

with open('all_uni_program_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Define the columns you need
columns = ["university", "program", "rating", "period_of_study", "Start_of_studies", "Diploma", "language", "Total_costs", "location", "program_link"]

# Open a CSV file to write to
with open('universities_program.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=columns)

    # Write the header
    writer.writeheader()

    # Write the rows
    for item in data:
        row = {
            "university": item.get("university_name"),
            "program": item.get("full_name"),
            "rating": item.get("rating", ""),
            "period_of_study": item.get("information", {}).get("Standard_period_of_study", ""),
            "Diploma": item.get("information", {}).get("Diploma", ""),
            "language": item.get("information", {}).get("Languages_​​of_instruction", ""),
            "Start_of_studies": item.get("information", {}).get("Start_of_studies", ""),
            "location": item.get("information", {}).get("Locations", ""),
            "Total_costs": item.get("information", {}).get("Total_costs", ""),
            "program_link": item.get("program_link")
        }
        writer.writerow(row)

print("CSV file created successfully!")