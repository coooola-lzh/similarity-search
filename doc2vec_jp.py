#%%
import gensim
import os
import collections
import smart_open
import random
import pickle
import time
import sys
from gensim.test.utils import get_tmpfile
from callback import EpochLogger, EpochSaver


data_prefix = ''.join(sys.argv[1:])
rela_path = 'dataset/jp/' + data_prefix
text_path, dic_path = rela_path + '.txt', rela_path + '.dic'

# Load the dictionary (url 2 indices)
print("Load dictionary for url to indices...", flush=True)
t1 = time.time()
with open(dic_path, 'rb') as f:
    url_to_i =  pickle.load(f)

t2 = time.time()
print('Finished loading dictionary, took {:.3f} secs\n'.format(t2 - t1), flush=True)

def read_corpus(fname, token_only=False):
    with smart_open.open(fname, encoding='utf-8') as f:
        i = 0
        for line in f:
            url, *words = line.split()
            words = ' '.join(words)
            if token_only:
                yield gensim.utils.simple_preprocess(words)
            else:
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(words), [i])
                i += 1

print("Start loading the corpus...", flush=True)
t1 = time.time()
train_corpus = list(read_corpus(text_path))
t2 = time.time()
print("Finished loading the corpus, took {:.3f} secs".format(t2 - t1), flush=True)
print("The first 10 data of corpus are:\n")
for i in range(10):
    print(train_corpus[i], '\n')


total_word_cnt = sum([len(doc.words) for doc in train_corpus])
print("The corpus has {} instances in total, {} words\n".format(len(train_corpus), total_word_cnt), flush=True)






# Build a Doc2Vec model with Japanese text data crwaled on specified date.
epoch_logger = EpochLogger()
epoch_saver = EpochSaver('model/{}_doc2vec_jp'.format(data_prefix))

print("Start to train the model...", flush=True)
model = gensim.models.doc2vec.Doc2Vec(vector_size=100, min_count=5, epochs=20, callbacks=[epoch_logger, epoch_saver])
model.build_vocab(train_corpus)

t1 = time.time()
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
t2 = time.time()
print("Finished training, took {:.3f} secs\n".format(t2 - t1), flush=True)

# Save the corpus as a list.
t1 = time.time()
print("Start to pickle the training corpus.", flush=True)

with open('dataset/jp/{}_train_corpus.lst'.format(data_prefix), 'wb') as f:
    pickle.dump(train_corpus, f)

t2 = time.time()
print("Finished pickling the training, corpus, took {:.3f} secs\n".format(t2 - t1), flush=True)

