import os
from pyvi import ViTokenizer
import gensim
import threading
import time
from ftfy import fix_encoding
import re

def tokenizer_word(data_dir, category, save_dir, sw_dir):
    list_fn = os.listdir(os.path.join(data_dir, category))
    file_train = os.path.join(save_dir, "Train", "{}.txt".format(category))
    file_test = os.path.join(save_dir, "Test", "{}.txt".format(category))

    # lay stopwords tu file
    with open(sw_dir, "r") as f:
        stopwords = f.readlines()
    for i in range(len(stopwords)):
        stopwords[i] = stopwords[i].strip()

    # tao train file, test file theo chu de
    with open(file_train, "w", encoding="utf8"): pass
    with open(file_test, "w", encoding="utf8"): pass

    # chia train, test (60/40)
    mid = int(len(list_fn) * 0.6 + 0.5)

    for i, fn in enumerate(list_fn):
        fl = os.path.join(data_dir, category, fn)
        with open(fl, "r") as f:
            content = f.readlines()
        content = " ".join(content)
        content = content.replace("\n", " ")
        content = fix_encoding(content)
        content = ViTokenizer.tokenize(content)
        content = gensim.utils.simple_preprocess(content)
        content = [w for w in content if not w in stopwords]
        content = " ".join(content)
        if len(content) < 100:
            continue
        if i < mid:
            with open(file_train, "a", encoding="utf8") as f:
                f.write(content)
                f.write("\n")
        elif i == mid:
            with open(file_train, "a", encoding="utf8") as f:
                f.write(content)
        else:
            if i == (len(list_fn) - 1):
                with open(file_test, "a", encoding="utf8") as f:
                    f.write(content)
            else:
                with open(file_test, "a", encoding="utf8") as f:
                    f.write(content)
                    f.write("\n")

def main():
    project_dir = os.getcwd()
    data_dir = os.path.join(project_dir, "news_data")
    save_dir = os.path.join(project_dir, "predata")
    sw_dir = os.path.join(project_dir, "stopwords")

    list_category = os.listdir(data_dir)
    for cate in list_category:
        path = os.path.join(data_dir, cate)
        thead = threading.Thread(target=tokenizer_word, args=(data_dir, cate, save_dir, sw_dir))
        thead.start()
        time.sleep(5)

if __name__ == "__main__":
    main()
