# This script conducts document similarity search queries.
# Input is taken as url, and it gives urls as output whose website content (document) is similar to the query.

# Expand the python import search path.
import sys
sys.path.append('..')

from callback import EpochLogger, EpochSaver
import pickle
import gensim
import os
import time

model_path = 'model/doc2vec.model.model'
corpus_path = 'model/train_corpus.lst'

def load_model():
    t1 = time.time()
    print('Start to load the pre-trained doc2vec model.\n')
    model = gensim.models.doc2vec.Doc2Vec.load(model_path)
    t2 = time.time()
    print('Loading model finished, took {:.3f} secs.\n'.format(t2 - t1))
    return model

def load_dic(path):
    t1 = time.time()
    print('Start to load the dictionary.\n')
    with open(path, 'rb') as f:
        dic = pickle.load(f)
    t2 = time.time()
    print('Loading dictionary finished, took {:.3f} secs.\n'.format(t2 - t1))
    return dic

def load_corpus():
    t1 = time.time()
    print('Start to load the corpus.\n')
    with open(corpus_path, 'rb') as f:
        corpus = pickle.load(f)
    t2 = time.time()
    print('Loading corpus finished, took {:.3f} secs.\n'.format(t2 - t1))
    return corpus

def main():
    print('Initialize the data for similar document query.\n')
    
    model = load_model()
    url_to_i = load_dic('model/url_to_i')
    i_to_url = load_dic('model/i_to_url')
    corpus = load_corpus()

    # Start querying.
    while True:
        query_url = input('Please input the url you want to search with:\n')
        if query_url not in url_to_i: 
            print('The url doesn\'t exist!\n')
            continue
        
        topN = int(input('Please input the number of most similar answers you want:\n'))
        query_i = url_to_i[query_url]
        sims = model.docvecs.most_similar([model.docvecs[query_i]], topn=topN)
        for doc_id, sim in sims:
            print('The similar document url is: {}, similarity: {}, and the contents: {}\n'.format(i_to_url[doc_id], sim, ' '.join(corpus[doc_id].words)) + '\n\n')
    
    return 

if __name__ == '__main__':
    main()