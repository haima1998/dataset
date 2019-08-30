import os
import random


def _main():
    trainval_percent = 0.1
    train_percent = 0.9
    xmlfilepath = '/home/charlie/disk2/dataset/number/data_dataset_voc/Annotations'

    total_xml = os.listdir(xmlfilepath)

    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    trainval = random.sample(list, tv)

    print(num)
    print(tv)

    ftest = open('/home/charlie/disk2/dataset/number/data_dataset_voc/ImageSets/Main/test.txt', 'w')
    ftrain = open('/home/charlie/disk2/dataset/number/data_dataset_voc/ImageSets/Main/trainval.txt', 'w')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            ftest.write(name)
        else:
            ftrain.write(name)

    ftrain.close()
    ftest.close()


if __name__ == '__main__':
    _main()
