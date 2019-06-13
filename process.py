# This is a script to process and merge the Japanese website data, write them into one file.
# This script takes 1 argument as the prefix of the data folders you want to process with, for example, input '20190209' will result
# it only process the data inside folders which their names has a prefix '20190209

import os
import gzip
import pickle
import sys
import time
import collections

process_dir = []
assert(len(sys.argv) == 2)
prefix = sys.argv[1]

print("Import data paths with specified path prefix:{}".format(prefix), flush=True)
for dire in os.listdir('./dataset/jp/exclude_ml'):
    if dire[:len(prefix)] == prefix:
        process_dir.append(dire)

# Modify the directories into complete version
process_dir = ['dataset/jp/exclude_ml/' + d for d in process_dir]
print("Finished importing data paths\n", flush=True)

# data_path is the path of data file
# Only process the data obtained on 20190209, as a test. 
# Also, make a dictionary to convert urls into indices.

# The format of raw data is : 
#                             "url"     "word1"
#                             "url1"    "word2"
#                             ....
#                             "urlN"    "wordN"

# Merge the text which owns same url into 1 line
# The output data file should look like: 
#                             "url1"    "word11 word12 word13 ... word1N"
#                             "url2"    "word21 word22 word23 ... word2N"
#                             ....
#                             "urlN"    "wordN1 wordN2 wordN3 ... wordNN"


dic = {}
word_buf = []
prev_url, index = None, 0
out_path = 'dataset/jp/' + prefix
out_path_txt = out_path + '.txt'

def cut_url(url):
    if 'www.' in url:
        start = url.find('www.') + len('www.')
    else:
        start = url.find('//') + len('//')
    if 'co.jp' in url:
        end = url.find('co.jp') + len('co.jp')
    else:
        end = url.find('.jp') + len('.jp')
    return url[start:end]

url2words = collections.defaultdict(list)
print("Start merging the data files...", flush=True)
t1 = time.time()
finished_word_cnt = 0
for dire in process_dir:
    for data_name in os.listdir(dire):
            # Only process compressed data file.
        if data_name[-3:] != '.gz': continue
        data_path = dire + '/' + data_name
        with gzip.open(data_path, 'rt', encoding='utf-8') as fin:
            for line in fin:
                if finished_word_cnt % 1000000 == 0:
                    print("{} words processed.".format(finished_word_cnt), flush=True)
                url, *word = line.split()
                url = cut_url(url)
                if '.' not in url: continue
                url2words[url] += word
                finished_word_cnt += len(word)


t2 = time.time()
print("Finished merging all the data with specified prefix name.\nTook {:.3f} secs, processed {} words with total {} urls.\n".format(t2 - t1, finished_word_cnt, len(url2words)), flush=True)

print('Start to save the url-words documents.', flush=True)
t1 = time.time()
with open(out_path_txt, 'w', encoding='utf-8') as f:
    i = 0
    for url, words in url2words.items():
        f.write(url + ' ' + ' '.join(words) + '\n')
        dic[url] = i
        i += 1
t2 = time.time()
print("Finished saving the url-words documents, took {:.3f} secs.\n".format(t2 - t1), flush=True)
# Pickle the dictionary (url 2 index) and save it.

print("Start pickling the dictionary (from url to index).", flush=True)
t1 = time.time()
out_path_dic = out_path + '.dic'
with open(out_path_dic, 'wb') as f:
    pickle.dump(dic, f)
t2 = time.time()
print("Finished pickling the dictionary, took {:.3f} secs\n".format(t2 - t1), flush=True)