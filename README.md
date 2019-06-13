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

## glimpse.py
This script is to have a glimpse at the processed data file, say, url-to-index dictionary or url-words pairs document data.<br/>
The needed arguments are __1.type of the file__, `txt` or `dic`, __2.date of data collected__, for example, `20190209`, which means all the data collected on Feb.9th of 2019. It's also a representation of the data path. __3.number of instances to check__, which means how many instances you want to look at.<br/>
As a example usage, you type `python3 glimpse.py`, then follow the input prompts.
