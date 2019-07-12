#%%
# This script is to load the pre-trained doc2vec model, and url-to-index dicionary and corpus (document) datas.
# After loading the data, doing the search with given query url and specified retrieval numbers, conduct the search, 
# and output the similar document id, similarity, content and urls.


from callback import EpochLogger, EpochSaver
import gensim
import pickle
import os
import time

    
#    prefix = input('Please input the date in which data are collected:\n')
prefix = '20190209'

model_path = 'model/' + prefix + '_doc2vec_jp.model'
model = gensim.models.doc2vec.Doc2Vec.load(model_path)

dic_path = 'dataset/jp/' + prefix + '.dic'
with open(dic_path, 'rb') as f:
    url_to_i = pickle.load(f)

corpus_path = 'dataset/jp/' + prefix + '_train_corpus.lst'
with open(corpus_path, 'rb') as f:
    corpus = pickle.load(f)


#%%
url_to_i['1sei.co.jp']
#%%
sims = model.docvecs.most_similar([model.docvecs[3]], topn=10)
sims
#%%
    while True:
        query_url = input("Please input the url query you want to search with:\n")
        if query_url not in url_to_i:
            print("The url doesn't exist!\n")
            continue
        
        topN = int(input("Please input the number of most similar results you want to get:\n"))
        query_i = url_to_i[query_url]
        sims = model.docvecs.most_similar([model.docvecs[query_i]], topn=topN)
        for doc_id, sim in sims:
            print(doc_id, sim)
            print('\n')
            print("The similar document url is: {}, similarity is: {}, and the contents:\n".format(corpus[int(doc_id)].tags[0], sim))
            print(' '.join(corpus[doc_id].words) + '\n\n')
            print(doc_id, sim)
    return

