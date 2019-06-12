import gensim
import os
import collections
import smart_open
import random
from pprint import pprint
import numpy as np
import sys
import struct
import timeit


# Define a function to read corpus

def read_corpus(fname, tokens_only=False):
    with smart_open.smart_open(fname) as f:
        for i, line in enumerate(f):
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [i])

data_file = 'dataset/amz_data_shuffled.dat'

def get_line_numbers(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        line_cnt = 0
        for line in f:
            line_cnt += 1
    return line_cnt

# Process 10k lines of data
# Split the data into train corpus and test corpus

print("Start loading data...")
corpus = list(read_corpus(data_file))
corpus_len = len(corpus)
train_ratio = 0.9
train_corpus_len = int(corpus_len * train_ratio)
train_corpus, test_corpus = corpus[:train_corpus_len], corpus[train_corpus_len:]
print("Loading data finished.")

# Train doc2vec model
print("Start build the Doc2Vec model...")
t1 = timeit.default_timer()
model = gensim.models.doc2vec.Doc2Vec(vector_size=100, min_count=5, epochs=20)
model.build_vocab(train_corpus)
print("Start training...")
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
t2 = timeit.default_timer()
print("Training took {:.4f} secs".format(t2 - t1))

# Pickle the model file
print("Start saving the model and vectors...")
model.save('doc2vec_amz_epochs_40.model')
matrix = [model.docvecs[i] for i in range(len(model.docvecs))]
np.save('doc2vec_amz_epochs_40_vec', np.array(matrix))
t3 = timeit.default_timer()
print("Saving took {:.4f} secs".format(t3 - t2))

#infer = model.infer_vector(test_corpus[499].words)
#similarity = model.docvecs.most_similar([infer], topn=10)

similarity = model.docvecs.most_similar([model.docvecs[100]], topn=10)

print("Query: {}".format(' '.join(train_corpus[100].words)))

for i, sim in enumerate(similarity):
    print("Similarity:{}".format(sim[1]))
    print(" ".join(train_corpus[similarity[i][0]].words))
