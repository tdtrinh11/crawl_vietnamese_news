import os
from pyvi import ViTokenizer
import gensim
import threading
import time

def tokenizer_word(path, save_dir):
    list_fn = os.listdir(path)
    file_train = os.path.join(save_dir, "Train", "{}.txt".format(category))
    file_test = os.path.join(save_dir, "Test", "{}.txt".format(category))

    # tao train file, test file theo chu de
    with open(file_train, "w"): pass
    with open(file_test, "w"): pass

    # chia train, test (60/40)
    mid = int(len(list_fn) * 0.6 + 0.5)

    for i, fn in enumerate(list_fn):
        fl = os.path.join(data_dir, category, fn)
        with open(fl, "r") as f:
            content = f.readlines()
        content = " ".join(content)
        content = ViTokenizer.tokenize(content)
        content = gensim.utils.simple_preprocess(content)
        content = " ".join(content)
        if i < mid:
            with open(file_train, "a") as f:
                f.write(content)
                f.write("/n")
        elif i == mid:
            with open(file_train, "a") as f:
                f.write(content)
        else:
            if i == (len(list_fn) - 1):
                with open(file_test, "a") as f:
                    f.write(content)
            else:
                with open(file_test, "a") as f:
                    f.write(content)
                    f.write("/n")

def main():
    project_dir = os.getcwd()
    data_dir = os.path.join(project_dir, "news_data")
    save_dir = os.path.join(project_dir, "predata")

    list_category = os.listdir(data_dir)
    for cate in list_category:
        path = os.path.join(data_dir, cate)
        thead = threading.Thead(target=tokenizer_word, args=(path,save_dir))
        thead.start()
        time.sleep(5)

if __name__ == "__main__":
    main()