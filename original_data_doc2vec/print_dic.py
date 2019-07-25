import pickle

def load_dic(data):
    with open(data, 'rb') as f:
        dic = pickle.load(f)
    return dic

def main():
    dic_name = input("Please input the dictionary you want to check, (url_to_i) or (i_to_url):\n")
    data = 'model/' + dic_name
    dic = load_dic(data)
    print(dic)
    return

if __name__ == '__main__':
    main()
    