#%%
import gensim

model = gensim.models.doc2vec.Doc2Vec.load('doc2vec_amz_epochs_40.model')
#%%
dir(model)
#%%
model.vocabulary