import os
import random

#ROOT_DIR = '/home/charlie/disk2/dataset/number/data_dataset_voc'
ROOT_DIR = '/home/charlie/disk2/dataset/number/data_dataset_voc'

LABLE_DIR = os.path.join(ROOT_DIR, "Annotations")
TEST_SET_FILE = os.path.join(ROOT_DIR, "ImageSets/Main/test.txt")
TRAIN_SET_FILE = os.path.join(ROOT_DIR, "ImageSets/Main/trainval.txt")
ALL_SET_FILE = os.path.join(ROOT_DIR, "ImageSets/Main/all.txt")

def _main():
    trainval_percent = 0.3
    train_percent = 0.7

    total_xml = os.listdir(LABLE_DIR)

    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    trainval = random.sample(list, tv)

    print(num)
    print(tv)

    ftest = open(TEST_SET_FILE, 'w')
    ftrain = open(TRAIN_SET_FILE, 'w')
    fall = open(ALL_SET_FILE, 'w')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        fall.write(name)
        if i in trainval:
            ftest.write(name)
        else:
            ftrain.write(name)

    ftrain.close()
    ftest.close()


if __name__ == '__main__':
    _main()
