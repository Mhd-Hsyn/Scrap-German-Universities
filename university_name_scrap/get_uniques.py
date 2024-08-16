import json

with open("uniersities.json", "r") as file:
    all_data = json.load(file)
    
unique_data= set(tuple(data) for data in all_data)

print(len(unique_data))

unique_data = list(unique_data)

with open("unique_universities.json", "w") as file:
    json.dump(unique_data, file, indent=4)

