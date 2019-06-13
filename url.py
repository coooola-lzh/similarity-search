# This script defines a url processing function.

def cut_url(url):
    if 'www.' in url:
        start = url.find('www.') + len('www.')
    else:
        start = url.find('//') + len('//')
    if 'co.jp' in url:
        end = url.find('co.jp') + len('co.jp')
    else:
        end = url.find('.jp') + len('.jp')
    return url[start:end]

def main():
    url = input()
    print(cut_url(url))

if __name__ == '__main__':
    main()