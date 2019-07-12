
import os
import warc
import pickle
from get_text_of_html import get_text_of_html
from is_valid_text import is_valid_text
import decode

data = 'part-r-00001.seg-00000.attempt-00000.warc.gz'


# Process warc files, extract payload (text contents) and their URL

collected_text_nums = 0
invalid_text_nums = 0
text_url_pairs = []
with warc.open(data) as f:
    for record in f:
        text, url = record.payload.read(), record['WARC-Target-URI']
        decoded_text = decode.decode(text)
        if not decoded_text: 
            invalid_text_nums += 1
            continue
        
        processed_text = get_text_of_html(decoded_text)
        if not is_valid_text(processed_text): 
            invalid_text_nums += 1
            continue
        if collected_text_nums % 500 == 0 and collected_text_nums:
            print("Collected {} text-url pairs".format(collected_text_nums))
        text_url_pairs.append((processed_text, url))
        collected_text_nums += 1

print('Totally {} files, {} invalid, {} collected\n'.format(collected_text_nums + invalid_text_nums, invalid_text_nums, collected_text_nums))

output_text = 'url_text.dat'

with open(output_text, 'w') as f:
    written_num = 0
    for t, url in text_url_pairs:
        if not is_valid_text(t): continue

        if written_num % 500 == 0 and written_num:
            print('{} text files dumped.'.format(written_num))

        text = get_text_of_html(t).split()
        text = ' '.join([t for t in text if t])
        f.write(url + ' ' + text + '\n')
        written_num += 1

print("URL-text data dump finished, totally {} instances\n".format(written_num))