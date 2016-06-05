import csv
import time
import random

consolidated_contracts = []

# import data
with open('contract_announcements.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['announcement']:
            consolidated_contracts.append([row['announcement'], row['date']])
with open('contract_announcements_recent_items.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['announcement']:
            consolidated_contracts.append([row['announcement'], row['date']])

# randomly shuffle array for selection of random test data
random.shuffle(consolidated_contracts)

# convert string dates into date objects and sort and then back to date
for contract in consolidated_contracts:
    contract[1] = time.strptime(contract[1], "%B %d, %Y")
for contract in consolidated_contracts:
    contract[1] = time.strftime("%B %d, %Y", contract[1])

with open('randomized_consolidated_contracts.csv', 'w') as csvfile:
    fieldnames = ['date', 'announcement']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for row in consolidated_contracts:
        writer.writerow([row[1], row[0]])
