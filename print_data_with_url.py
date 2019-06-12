# This script is to print the document under a specific url
# It takes 1 argument, which is the url you want to print the document with.

import pickle
import sys

dic_path = 'dataset/jp/20190209.dic'
with open(dic_path, 'rb') as f:
    dic = pickle.load(f)

doc_path = 'dataset/jp/20190209.txt'
docs = []
with open(doc_path, 'r', encoding='utf-8') as f:
    for line in f:
        url, *words = line.split()
        docs.append(words)

url = sys.argv[1]
print(docs[dic[url]])
