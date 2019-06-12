#%%
import pickle
with open('dataset/jp/tfidf1.pickle', 'rb') as f:
    tfidf = pickle.load(f)

#%%
tfidf["11298.co.jp"]