from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter
from janome.tokenfilter import ExtractAttributeFilter, POSStopFilter


t = Tokenizer(mmap=True)

# An analyzer need 3 parameters, which are: char_filters, tokenizer, token_filters
a = Analyzer([UnicodeNormalizeCharFilter()], t, [POSStopFilter(['記号']), ExtractAttributeFilter('surface')])


# Split text into words, only remove punctuation.
def split_words(text):
    return list(a.analyze(text))
