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
from gensim.models.callbacks import CallbackAny2Vec

data_prefix = ''.join(sys.argv[1:])
rela_path = 'dataset/jp/' + data_prefix
text_path, dic_path = rela_path + '.txt', rela_path + '.dic'

# Load the dictionary (url 2 indices)
print("Load dictionary for url to indices...")
t1 = time.time()
with open(dic_path, 'rb') as f:
    url_to_i =  pickle.load(f)

t2 = time.time()
print('Finished loading dictionary, took {:.3f} secs\n'.format(t2 - t1))

def read_corpus(fname, token_only=False):
    with smart_open.open(fname, encoding='utf-8') as f:
        for line in f:
            url, *words = line.split()
            words = ' '.join(words)
            if token_only:
                yield gensim.utils.simple_preprocess(words)
            else:
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(words), [url_to_i[url]])

print("Start loading the corpus...")
t1 = time.time()
train_corpus = list(read_corpus(text_path))
t2 = time.time()
print("Finished loading the corpus, took {:.3f} secs".format(t2 - t1))
total_word_cnt = sum([len(doc.words) for doc in train_corpus])
print("The corpus has {} instances in total, {} words\n".format(len(train_corpus), total_word_cnt))



# Binding callback functions for the training model, to get some information about training progress.
class EpochSaver(CallbackAny2Vec):
    """Callback to save model after each epoch"""

    def __init__(self, path_prefix):
        self.path_prefix = path_prefix
        self.epoch = 1
        print('{}.model'.format(self.path_prefix))
    
    def on_epoch_end(self, model):
        model.save('{}.model'.format(self.path_prefix))
        self.epoch += 1

class EpochLogger(CallbackAny2Vec):
    """Callback to print training process"""

    def __init__(self):
        self.epoch = 1
        self.time = 0

    def on_epoch_begin(self, model):
        print("Epoch #{} starts".format(self.epoch))
        self.time = time.time()
    
    def on_epoch_end(self, model):
        print("Epoch #{} ends, took {:.3f} secs".format(self.epoch, time.time() - self.time))
        self.epoch += 1
        self.time = time.time()


# Build a Doc2Vec model with Japanese text data crwaled on 2019/02/1X
epoch_logger = EpochLogger()
epoch_saver = EpochSaver('model/{}_doc2vec_jp'.format(data_prefix))

print("Start to train the model...")
model = gensim.models.doc2vec.Doc2Vec(vector_size=100, min_count=5, epochs=20, callbacks=[epoch_logger, epoch_saver])
model.build_vocab(train_corpus)

t1 = time.time()
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
t2 = time.time()
print("Finished training, took {:.3f} secs\n".format(t2 - t1))

# model.save('doc2vec_jp_20190209_epoch20.model')
# Dump the corpus, save it as a list.
t1 = time.time()
print("Start to pickle the training corpus.")

with open('dataset/jp/{}_train_corpus.lst'.format(data_prefix), 'wb') as f:
    pickle.dump(train_corpus, f)

t2 = time.time()
print("Finished pickling the training, corpus, took {:.3f} secs\n".format(t2 - t1))

