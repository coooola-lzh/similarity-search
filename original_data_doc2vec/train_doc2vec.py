# This script take url-text input data, train a doc2vec model for further usage of searching similar documents.
# The output includes trained model, url-to-index and index-to-url dictionaries, to support queries with urls.

import gensim
import os
import smart_open
import pickle
import time 
import sys
import urllib3

# Expand path for imported python modules
sys.path.append('..')

from callback import EpochLogger, EpochSaver
from split_words import split_words




url_to_i, i_to_url  = {}, {}
data = 'url_text.dat'

def read_corpus(fname):
    with smart_open.open(fname, encoding='utf-8') as f:
        i = 0
        for line in f:
            if i and i % 10 == 0:
                print('Finished loading {} docs.\n'.format(i), flush=True)
            url, *text = line.split()
            url = urllib3.util.parse_url(url).hostname
            text = ''.join(text)
            url_to_i[url], i_to_url[i]= i, url
            yield gensim.models.doc2vec.TaggedDocument(split_words(text), [i])
            i += 1
            if i > 10: break

def main():
    # Load corpus and build url-to-index, index-to-url dictionaries.
    print('Start to load the corpus, building url-to-index and index-to-url dictionaries simultaneously.\n', flush=True)
    t1 = time.time()
    train_corpus = list(read_corpus(data))
    t2 = time.time()
    print('Loading corpus finished, took {:.3f} secs.\n'.format(t2 - t1), flush=True)
    
    # Save the u-to-i and i-to-u dictionaries with pickling.
    with open('model/url_to_i', 'wb') as f:
        pickle.dump(url_to_i, f)
    with open('model/i_to_url', 'wb') as f:
        pickle.dump(i_to_url, f)
    
    # Show first 10 training corpus
    print('First 10 training corpus look like this:\n')
    for i in range(10):
        print(train_corpus[i], '\n')
    
    # A statistic of training corpus
    total_word_cnt = sum([len(doc.words) for doc in train_corpus])
    print("The corpus has {} instances in total, {} words\n".format(len(train_corpus), total_word_cnt), flush=True)

    # Instantiate callback functions for tracing the training process.
    # We instantiate an epoch logger and an epoch saver
    epoch_logger = EpochLogger()
    model_save_path = 'model/doc2vec.model'
    epoch_saver = EpochSaver(model_save_path)

    # Start training
    print("Start to train the model\n", flush=True)
    model = gensim.models.doc2vec.Doc2Vec(vector_size=100, min_count=5, epochs=20, callbacks=[epoch_logger, epoch_saver])
    model.build_vocab(train_corpus)

    t1 = time.time()
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    t2 = time.time()
    print('Training finished, took {:.3f} secs\n'.format(t2 - t1), flush=True)
    
    # Save the corpus as a python list
    print('Start to save the corpus\n')
    t1 = time.time()
    with open('model/train_corpus.lst', 'wb') as f:
        pickle.dump(train_corpus, f)
    t2 = time.time()
    print('Corpus saved, took {:.3f} secs\n'.format(t2 - t1))

if __name__ == '__main__':
    main()
    
