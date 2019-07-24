from janome.tokenizer import Tokenizer
t = Tokenizer(mmap=True)

def split_words(text):
    return t.tokenize(text)
    