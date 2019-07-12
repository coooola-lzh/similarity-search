import chardet

def decode(text):
    decoded_text = ''
    try:
        decoded_text = text.decode()
    except UnicodeDecodeError:
        encoding = chardet.detect(text)['encoding']
        if encoding:
            try:
                decoded_text = text.decode(encoding)
            except UnicodeDecodeError:
                pass
    return decoded_text