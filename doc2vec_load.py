#%%
from callback import EpochLogger, EpochSaver
import gensim
import pickle
import os
import time

def load_model(path):
    if not os.path.exists(path):
        print("The path of model doesn't exist!\n")
        raise FileExistsError
    t1 = time.time()
    print("Start loading the pre-trained doc2vec model...")
    model = gensim.models.doc2vec.Doc2Vec.load(path)
    t2 = time.time()
    print("Finished loading the model, took {:.3f} secs\n".format(t2 - t1))
    return model

def load_dic(path):
    if not os.path.exists(path):
        print("the path of dictionary doesn't exist!\n")
        raise FileExistsError
    t1 = time.time()
    print("Start loading the url-to-index dictionary...")
    with open(path, 'rb') as f:
        dic = pickle.load(f)
    t2 = time.time()
    print("Finished loading the dictionary, took {:.3f} secs".format(t2 - t1))
    return dic

def load_corpus(path):
    if not os.path.exists(path):
        print("the path of the corpus doesn't exist!\n")
        raise FileExistsError
    t1 = time.time()
    print("Start loading the corpus...")
    with open(path, 'rb') as f:
        corpus = pickle.load(f)
    t2 = time.time()
    print("Finished loading the corpus, took {:.3f} secs".format(t2 - t1))
    return corpus

def main():
    
    prefix = input('Please input the date in which data are collected:\n')
    
    model_path = prefix + '_doc2vec_jp.model'
    model = load_model(model_path)

    dic_path = 'dataset/jp/' + prefix + '.dic'
    url_to_i = load_dic(dic_path)

    corpus_path = 'dataset/jp/' + prefix + '_train_corpus.lst'
    corpus = load_corpus(corpus_path)

    return

if __name__ == '__main__':
    main()

