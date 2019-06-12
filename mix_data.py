# This script is to shuffle the amazon review data, in case that the same class documents are with similar indices.
# (as the order of the file stream)

import random
data = []
data_file = 'dataset/merge_amz_data.dat'
with open(data_file, 'r', encoding='utf-8') as f:
    for line in f:
        data.append(line)

random.shuffle(data)

with open('dataset/amz_data_shuffled.dat', 'w', encoding='utf-8') as f:
    for line in data:
        f.write(line)
