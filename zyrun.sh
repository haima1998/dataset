# convert trainning set
#python 02_labelme2voc.py  /home/charlie/disk2/dataset/magic/lableme/20200309_train/lable  /home/charlie/disk2/dataset/magic/data_dataset_voc --labels /home/charlie/disk2/dataset/magic/labels.txt
python 02_labelme2voc.py  /home/charlie/disk2/dataset/number2/lableme/20200319_test/lable  /home/charlie/disk2/dataset/number2/data_dataset_voc_test --labels /home/charlie/disk2/dataset/number2/labels.txt

#python 02_labelme2voc.py  /home/charlie/disk2/dataset/number/lableme/07_pad_0912/lable  /home/charlie/disk2/dataset/number/data_dataset_voc --labels /home/charlie/disk2/dataset/number/labels.txt

#convert test set
#python 02_labelme2voc.py  /home/charlie/disk2/dataset/number/lableme/00_pad_test_set/lable  /home/charlie/disk2/dataset/number/test_data_dataset_voc --labels /home/charlie/disk2/dataset/number/labels.txt

#show lableme result
#python 03_show_labelme_lable.py  /home/charlie/disk2/dataset/number/data_annotated/lable  /home/charlie/disk2/dataset/number/data_dataset_voc --labels /home/charlie/disk2/dataset/number/labels.txt
