from UI import *
from VkApiFunc import *
from CSVFunctions import delete_from_end, get_rows_count, reverse_csv
import subprocess
import sys
import pathlib


if __name__ == '__main__':

    data = InputForm().response

    token = str(data[0])
    user_id = int(data[3])
    start_message = int(data[4])
    message_count = int(data[5])

    parse_vk = VkParser(token, user_id)
    parse_vk.Parse(start_message, message_count)
    print(parse_vk.get_message_count())
    delete_from_end('CSV/out.csv', get_rows_count('CSV/out.csv')-message_count)
    reverse_csv('CSV/out.csv', 'CSV/final.csv')
    print('DONE!!!')

    if sys.platform == 'linux':
        subprocess.Popen("nautilus --browser 'CSV' ", shell=True)
    else:
        subprocess.Popen(f"explorer {pathlib.Path().resolve()}\CSV ", shell=True)

