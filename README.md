# similarity-search
This is the repository for document (Japanese) similarity search, using doc2vec model.

## process.py
The file to process the compressed Japanese document data, group them by urls.
<br/>For the usage, type `python process.py *prefix*` to process all the data inside the directories with a prefix name `*prefix*`.
<br/>For example, `python process.py 20190209` process all the data inside folders with name __20190209xxxx__

## doc2vec_jp.py
This script take the data processed by __process.py__, training a Doc2Vec model for it.<br/>
For the usage, type `python doc2vec_jp.py *prefix*` to process the data with name `*prefix*`.<br/>

## callback.py
The script with 2 callback functions to trace the training process, which are __EpochSaver__ and __EpochLogger__.<br/>
Namely, __EpochSaver__ is the callback function to save model for each epoch.<br/>
With same idea, __EpochLogger__ is the callback function to trace the process of training, and print the elapsed time for each epoch.
