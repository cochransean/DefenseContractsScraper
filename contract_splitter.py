import csv
import re

contracts = []
try:
    with open('consolidated_contracts.csv', 'r') as csvfile:
        contract_reader = csv.DictReader(csvfile)
        for row in contract_reader:
            contracts.append({'date': row['date'], 'announcement': row['announcement']})
except IOError:
    print("Error loading data.")
else:
    print("Data loaded.")

test1 = re.compile(r"(.{350,}\([a-zA-z0-9-]{8,}[0-9]{3,}\)).{350,}\([a-zA-z0-9-]{8,}[0-9]{3,}\)")
number_matches = 0

for contract in contracts:
    search_result = re.search(test1, contract['announcement'])
    if search_result:
        print(search_result.group(1))
        number_matches += 1
print(number_matches)
