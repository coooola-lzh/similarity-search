#%%
from callback import EpochLogger, EpochSaver
fname = 'model/20190209_doc2vec_jp.model'
model = gensim.models.doc2vec.Doc2Vec.load(fname)

#%%
model.docvecs[0]