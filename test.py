import sys
import pickle

def cut_url(url):
    """ An function to cut url, into regular version.
        We cut the prefix 'http://' and the suffix after 'co.jp' """
    start = url.find('http://') + len('http://')
    end = url.find('co.jp') + len('co.jp')
    return url[start:end]


def main():
    dic_path = 'dataset/jp/20190209.txt'
    output_num = input("Please input the number of urls you want to see:\n")
    output_num = int(output_num)
    with open(dic_path, 'r', ) as f:
        cnt = 0
        for line in f:
            if cnt >= output_num: break
            print(line)
            cnt += 1

    return
main()
