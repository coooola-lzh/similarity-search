# This script is to load the pre-trained doc2vec model, and url-to-index dicionary and corpus (document) datas.
# After loading the data, doing the search with given query url and specified retrieval numbers, conduct the search, 
# and output the similar document id, similarity, content and urls.


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
    
    model_path = 'model/' + prefix + '_doc2vec_jp.model'
    model = load_model(model_path)

    dic_path = 'dataset/jp/' + prefix + '.dic'
    url_to_i = load_dic(dic_path)

    corpus_path = 'dataset/jp/' + prefix + '_train_corpus.lst'
    corpus = load_corpus(corpus_path)

    while True:
        query_url = input("Please input the url query you want to search with:\n")
        if query_url not in url_to_i:
            print("The url doesn't exist!\n")
            continue
        
        topN = int(input("Please input the number of most similar results you want to get:\n"))
        query_i = url_to_i[query_url]
        sims = model.docvecs.most_similar([model.docvecs[query_i]], topn=topN)
        for doc_id, sim in sims:
            #print(doc_id, sim)
            #print('\n')
            #print("The similar document url is: {}, similarity is: {}, and the contents:\n".format(corpus[int(doc_id)].tags[0], sim))
            #print(' '.join(corpus[doc_id].words) + '\n\n')
            print(doc_id, sim)
    return

if __name__ == '__main__':
    main()

