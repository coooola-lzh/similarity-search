# Build callback functions for the training model, to get some information about training progress.
from gensim.models.callbacks import CallbackAny2Vec
class EpochSaver(CallbackAny2Vec):
    """Callback to save model after each epoch"""

    def __init__(self, path_prefix):
        self.path_prefix = path_prefix
        self.epoch = 1
        print('{}.model'.format(self.path_prefix))
    
    def on_epoch_end(self, model):
        model.save('{}.model'.format(self.path_prefix))
        self.epoch += 1

class EpochLogger(CallbackAny2Vec):
    """Callback to print training process"""

    def __init__(self):
        self.epoch = 1
        self.time = 0

    def on_epoch_begin(self, model):
        print("Epoch #{} starts".format(self.epoch))
        self.time = time.time()
    
    def on_epoch_end(self, model):
        print("Epoch #{} ends, took {:.3f} secs".format(self.epoch, time.time() - self.time))
        self.epoch += 1
        self.time = time.time()