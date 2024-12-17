
from UI import *
from VkApiFunc import *
from CSVFunctions import delete_from_end, get_rows_count, reverse_csv, csv_to_txt_cai
import subprocess
import sys
import pathlib


if __name__ == '__main__':

    data = InputForm().response

    token = str(data[0])
    user_id = int(data[3])
    start_message = int(data[4])
    message_count = int(data[5])
    user_dir = str(data[6])

    parse_vk = VkParser(token, user_id)
    parse_vk.parse(start_message, message_count)
    print(parse_vk.get_message_count())
    delete_from_end('Output/out.csv', get_rows_count('Output/out.csv')-message_count)
    reverse_csv('Output/out.csv', 'Output/final.csv')
    csv_to_txt_cai('Output/final.csv', 'Output/cai.txt')
    os.remove('Output/out.csv')

    print('DONE!!!')

    if sys.platform == 'linux':
        subprocess.Popen("nautilus --browser 'Output' ", shell=True)
    else:
        subprocess.Popen(f"explorer {pathlib.Path().resolve()}\Output ", shell=True)

