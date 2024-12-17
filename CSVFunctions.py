
import glob
import os
import shutil
import csv


def merge_csv() -> None:
    if os.path.isdir('Output'):
        shutil.rmtree('Output')
        os.mkdir('Output')
    else:
        os.mkdir('Output')

    files = glob.glob(f"CSV_temp/*_file.csv")
    print(files)

    with open(f"Output/out.csv", "ab") as f_out:
        for num in range(len(files)):
            try:
                with open(f"CSV_temp/{num}_file.csv", "rb") as f:
                    f_out.writelines(f)
            except:
                continue
    print("merging done!")


def repeat_count(process_index: int) -> int:
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


def get_rows_count(filename: str) -> int:
    with open(filename, mode='r', encoding='utf8') as file:
        row_count = sum(1 for row in file)
        return row_count


def delete_from_end(filename: str, iters: int) -> None:
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    data = data[:-iters]
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"The last {iters} rows have been removed from {filename}.")


def reverse_csv(filename: str, out: str) -> None:
    with open(filename) as f:
        data = f.readlines()
    data.reverse()
    with open(out, 'w') as f:
        f.writelines(data)


def csv_to_txt_cai(csv_filepath, txt_filepath, delimiter=',') -> None:
    try:
        with open(csv_filepath, 'r', newline='', encoding='utf-8') as csvfile, \
                open(txt_filepath, 'w', encoding='utf-8') as txtfile:

            reader = csv.reader(csvfile, delimiter=delimiter)
            for row in reader:
                txtfile.write(' '.join(row).replace(';',' ') + '\n')

    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_filepath}'")
    except Exception as e:
        print(f"An error occurred: {e}")

