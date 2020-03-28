from datetime import datetime
import csv

def writeRecordToFile(args):
    with open('record.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        data = [datetime.now()] + [d for d in args]
        writer.writerow(data)