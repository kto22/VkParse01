from CSVFunctions import mergeCSV
import csv

#mergeCSV()

with open(f"CSV/out.csv", mode='r', encoding='utf8') as file:
    csvFile = csv.reader(file)
    num = 61000
    count = 0
    for lines in csvFile:
        cur_num = int(lines[-1].split(';')[-1])
        if cur_num != num:
            print(cur_num, num)
            num = cur_num
            count += 1
        num -= 1
print(count - 1)