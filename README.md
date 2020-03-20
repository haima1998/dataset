# 数据处理流程：
1. 获取需要标注的数据:
   1) 一种途经是自己拍特定的场景，比如小米pad4的图片，分辨率是:1944X2592
   2) 一种途经是用户使用过程中上传，这类图片需要先按比例resize 再上传，控制上传的大小，控制在最长边800以内。

2.按比例resize图片，控制最长边在800以内。
  python 01_resize_image.py
  修改源图片路经:/home/charlie/disk2/dataset/witch/01orin_pic/20190929_train
    目标图片路经:/home/charlie/disk2/dataset/witch/lableme/20190929_train/JPEG


3.采用lableme 标注数据。得到JPEG 和 lable 目录的数据.

4. 将lableme 格式的jason标准格式转换为voc的xml格式.
   输出目录/home/charlie/disk2/dataset/number/data_dataset_voc
   备注:如果需要修改输出类型修改:/home/charlie/disk2/dataset/number/labels.txt
   python 02_labelme2voc.py
   
5. 可视化voc数据,检查标注和转换是否有问题.
   python 04_show_voc_lable.py

6. 对voc数据进行数据增强.
   python 05_augmentation.py

7. 切分训练集和测试集.
   python 06_make_train_val_test_set.py

8. 创建caffe 格式的lmdb 格式
   备注:如果需要修改输出个数,需要修改以下文件:
   /home/charlie/disk1/code/mygithub/dataset/labelmap_num.prototxt
   /home/charlie/disk2/dataset/number/labels.txt

   cd /home/charlie/disk1/code/opensouce/caffe/caffe/data/number
   ./07_create_list.sh
   ./08_create_data.sh


9. 如果需要修改模型的输出个数
   cd /home/charlie/disk1/code/opensouce/caffe/caffe/examples/MobileNet-SSD
   ./gen_model.sh 实际输出类别数+1

   修改MobileNetSSD_train.prototxt和MobileNetSSD_test.prototxt文件中的
   source: "trainval_lmdb_num/"   数据文件地址
   
   修改MobileNetSSD_test.prototxt文件的batch_size: 1



train and test model
-------------------------------------------------------------------
cd /home/charlie/disk1/code/opensouce/caffe/caffe/examples/MobileNet-SSD
1. train model 
./train_num.sh

2. test model
./test_num.sh

3. merge model:
./zymerge.sh

4. evaluate model
python 10_record_det_result.py

cd /home/charlie/disk1/code/mygithub/dataset 
python 11_evaluate_det_lable.py
