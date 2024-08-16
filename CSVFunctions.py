
import glob
import os
import shutil


def mergeCSV() -> None:

    if not os.path.isdir('CSV'):
        os.mkdir('CSV')

    files = glob.glob(f"CSV_temp/*_file.csv")
    print(files)

    with open(f"CSV/out.csv", "ab") as f_out:
        for num in range(len(files)):
            with open(f"CSV_temp/{num}_file.csv", "rb") as f:
                f_out.writelines(f)
    shutil.rmtree('CSV_temp')

    print("merging done!")


#----------------------------TESTS----------------------------

mergeCSV()
