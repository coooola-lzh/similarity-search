# This script is to have a glimpse at dataset.
# Print some instances from the url2idx dictionary, or url-and-words dataset.

import sys
import pickle
import os


def main():
    data_type = input('Input dic to print url to index dictionary, or txt to look at url and its words data.\n')
    if data_type != 'dic' and data_type != 'txt': 
        print('Input error!\n')
        return

    date = input("Input the collected date of the data, as the prefix of the data file name\n")
    path = 'dataset/jp/' + date + '.' + data_type
    if not os.path.isdir(path):
        print("The path doesn't exist!")
        return

    output_num = input("Please input the number of instances you want to check:\n")
    output_num = int(output_num)

# If check dictionary, we have to use pickle.
    if data_type == 'dic':
        with open(path, 'rb') as f:
            dic = pickle.load(f)
        cnt = 0
        for k, v in dic.items():
            if cnt >= output_num: break
            print(k, v)
            cnt += 1

# Else, just open the txt file.
    else:
        with open(path, 'r', encoding='utf-8') as f:
            cnt = 0
            for line in f:
                if cnt >= output_num: break
                print(line)
                cnt += 1
    return

if __name__ == '__main__':
    main()
