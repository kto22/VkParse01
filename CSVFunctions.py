
import glob
import os
import shutil
import csv


def mergeCSV() -> None:

    if not os.path.isdir('CSV'):
        os.mkdir('CSV')

    files = glob.glob(f"CSV_temp/*_file.csv")
    print(files)

    with open(f"CSV/out.csv", "ab") as f_out:
        for num in range(len(files)):
            try:
                with open(f"CSV_temp/{num}_file.csv", "rb") as f:
                    f_out.writelines(f)
            except:
                continue
    #shutil.rmtree('CSV_temp')

    print("merging done!")


def repeatCount(process_index: int) -> int:

    with open(f"CSV_temp/{process_index}_file.csv", mode='r', encoding='utf8') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            num = int(lines[-1].split(';')[-1])
            break
        count = 0
        for lines in csvFile:
            cur_num = int(lines[-1].split(';')[-1])
            if cur_num != num:
                print(cur_num, num)
                num = cur_num
                count += 1
            num -= 1
    return count-1


def repeatDelete(process_index: int, iters: int) -> None:
    for _ in range(iters):
        f = open(f'CSV_temp/{process_index}_file.csv', "r+", encoding='utf8')
        lines = f.readlines()
        lines.pop()
        f = open(f'CSV_temp/{process_index}_file.csv', "w+", encoding='utf8')
        f.writelines(lines)


#----------------------------TESTS----------------------------

#mergeCSV()

#repeatDelete(89, repeatCount(89))