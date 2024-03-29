# This is a script to process and merge the Japanese website data, write them into one file.
# This script takes 1 argument as the prefix of the data folders you want to process with, for example, input '20190209' will result
# it only process the data inside folders which their names has a prefix '20190209

import os
import gzip
import pickle
import sys
import time
import collections
from url import cut_url

process_dir = []


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

# Merge the words which own the same url into 1 line
# The output data file should look like: 
#                             "url1"    "word11 word12 word13 ... word1N"
#                             "url2"    "word21 word22 word23 ... word2N"
#                             ....
#                             "urlN"    "wordN1 wordN2 wordN3 ... wordNN"



# .txt file is the merged data file, with url-words pairs as introduced above.
out_path = 'dataset/jp/' + prefix
out_path_txt = out_path + '.txt'

# Maintain a dictionary to merge words which have a same url into one list.
# So we initialize a defaultdict with list.
url2words = collections.defaultdict(list)

# A list containing urls in the order which we meet them.
url_ordered = []

print("Start merging the data files...", flush=True)

# Counting the number of words we processed, for statistical purpose.
finished_word_cnt = 0

t1 = time.time()
for dire in process_dir:
    for data_name in os.listdir(dire):
        # Only process compressed data file.
        if data_name[-3:] != '.gz': continue
        data_path = dire + '/' + data_name
        
        with gzip.open(data_path, 'rt', encoding='utf-8') as fin:
            for line in fin:
                # Print some information for tracking the process.
                if finished_word_cnt % 1000000 == 0:
                    print("{} words processed.".format(finished_word_cnt), flush=True)
                
                # The string before the first space is recognized as url, following parts are words.
                url, *word = line.split()

                # Cut the url prefix, such as "http://" or "www", and the suffix after ".co.jp/" or ".com/", as 
                # we recognize them as sub urls of 1 main url.
                url = cut_url(url)

                # If meet some invalid url.
                if '.' not in url and len(sys.argv) < 3: continue
                
                # Record the order of urls we meet, for the purpose of query in the next.
                if url not in url2words:
                    url_ordered.append(url)

                # Merge words which are belonging to the same urls into the same list.
                url2words[url] += word
                finished_word_cnt += len(word)
t2 = time.time()

print("Finished merging all the data with specified prefix name.\nTook {:.3f} secs, processed {} words with total {} urls.\n".format(t2 - t1, finished_word_cnt, len(url2words)), flush=True)

# Save the merged data file, with the format below:
#           url1           word11, word12, word13 ... word1n
#           url2           word21, word22, word23 ... word2m
#           ...            ...
# For each line, the string before the first space is the url, followed by words inside it, seperated by spaces.

print('Start to save the url-words documents.', flush=True)
dic = {}
t1 = time.time()
with open(out_path_txt, 'w', encoding='utf-8') as f:
    for i, url in enumerate(url_ordered):
        f.write(url + ' ' + ' '.join(url2words[url]) + '\n')
        dic[url] = i
t2 = time.time()

print("Finished saving the url-words documents, took {:.3f} secs.\n".format(t2 - t1), flush=True)


# Pickle the dictionary (url to index) and save it.
# .dic file is a binary file of dictionary, mapping urls to indices (for the fast query purpose in the next parts.)
out_path_dic = out_path + '.dic'


print("Start pickling the dictionary (from url to index).", flush=True)
t1 = time.time()

with open(out_path_dic, 'wb') as f:
    pickle.dump(dic, f)

t2 = time.time()
print("Finished pickling the dictionary, took {:.3f} secs\n".format(t2 - t1), flush=True)

# Pickle the reversed dictionary (index to url) and save it.
out_path_rev_dic = out_path + '_' + '.dic'
rev_dic = {}

for url, i in dic.items():
    rev_dic[i] = url

print("Start pickling the dictionary (from index to url).", flush=True)
t1 = time.time()

with open(out_path_rev_dic, 'wb') as f:
    pickle.dump(rev_dic, f)

t2 = time.time()
print("Finished pickling the dictionary, took {:.3f} secs\n".format(t2 - t1), flush=True)