import csv
import os

with open("benefit.csv", "r", newline="") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if float(row[1]) <= 0:
            try:
                os.remove("models/" + row[0] + ".joblib")
            except:
                pass
