from janome.tokenizer import Tokenizer
t = Tokenizer(mmap=True)

def split_words(text):
    ans = [tokens for tokens in t.tokenize(text)]
    return ans