import csv

with open('Symptom2Disease.csv', 'r') as csvfile, open('Symptom2Disease_B.bin', 'wb') as binfile:
    reader = csv.reader(csvfile)
    for row in reader:
        binfile.write(bytes(','.join(row), 'utf-8'))
