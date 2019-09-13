import numpy as np  
import sys,os  
import cv2
caffe_root = '/home/charlie/disk1/code/opensouce/caffe/caffe/'
sys.path.insert(0, caffe_root + 'python')  
import caffe  
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString

net_file= 'no_bn.prototxt'  
caffe_model='no_bn.caffemodel'  
#test_dir = "/home/charlie/disk2/dataset/number/data_dataset_voc/JPEGImages_ori"
#test_dir = "/home/charlie/disk2/dataset/number/data_dataset_voc/JPEGImages"
test_dir = "/home/charlie/disk2/dataset/number/test_data_dataset_voc/JPEGImages"

DEST_DIR = '/home/charlie/disk2/dataset/number/test_data_dataset_voc/det_result/all'
DEST_XML_DIR = '/home/charlie/disk2/dataset/number/test_data_dataset_voc/det_result/all_xml'

#RESIZE = 3
RESIZE = 1
CROP_SIZE = 160

NEED_WRITE_IMAGE = False

if not os.path.exists(caffe_model):
    print(caffe_model + " does not exist")
    exit()
if not os.path.exists(net_file):
    print(net_file + " does not exist")
    exit()
caffe.set_mode_cpu()
net = caffe.Net(net_file,caffe_model,caffe.TEST)  

CLASSES = ('background',
           'zero','one', 'two', 'three', 'four',
           'five', 'six', 'seven', 'eight', 'nine'
           )


def preprocess(src):
    img = cv2.resize(src, (300,300))
    img = img - 127.5
    img = img * 0.007843
    return img

def postprocess(img, out):   
    h = img.shape[0]
    w = img.shape[1]
    box = out['detection_out'][0,0,:,3:7] * np.array([w, h, w, h])

    cls = out['detection_out'][0,0,:,1]
    conf = out['detection_out'][0,0,:,2]
    return (box.astype(np.int32), conf, cls)

def detect(imgfile):
    origimg_ori = cv2.imread(imgfile)

    #origimg = cv2.resize(origimg_ori,(800,800))

    size = origimg_ori.shape
    origimg = cv2.resize(origimg_ori, (size[1] / RESIZE, size[0] / RESIZE))

    # C. crop top image
    size_resize = origimg.shape
    cv2.rectangle(origimg, (0, 0), (size_resize[0], CROP_SIZE), (0, 0, 0), -1)

    img = preprocess(origimg)
    
    img = img.astype(np.float32)
    img = img.transpose((2, 0, 1))

    net.blobs['data'].data[...] = img
    out = net.forward()  
    box, conf, cls = postprocess(origimg, out)

    (filepath, tempfilename) = os.path.split(imgfile)

    # begin fill detect result xml file info
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'image'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = tempfilename

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = '%s' % size_resize[1]

    node_height = SubElement(node_size, 'height')
    node_height.text = '%s' % size_resize[0]

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '%s' % size_resize[2]
    # end fill detect result xml file info

    for i in range(len(box)):
       p1 = (box[i][0], box[i][1])
       p2 = (box[i][2], box[i][3])
       cv2.rectangle(origimg, p1, p2, (0,255,0))
       p3 = (max(p1[0], 15), max(p1[1], 15))
       title = "%s:%.2f" % (CLASSES[int(cls[i])], conf[i])
       cv2.putText(origimg, title, p3, cv2.FONT_ITALIC, 0.6, (0, 0, 0), 2)

       #begin add detect result object
       node_object = SubElement(node_root, 'object')
       node_name = SubElement(node_object, 'name')
       node_name.text = CLASSES[int(cls[i])]
       node_difficult = SubElement(node_object, 'difficult')
       node_difficult.text = '0'
       node_difficult = SubElement(node_object, 'conf')
       node_difficult.text = '%s' % conf[i]
       node_bndbox = SubElement(node_object, 'bndbox')
       node_xmin = SubElement(node_bndbox, 'xmin')
       node_xmin.text = '%s' % box[i][0]
       node_ymin = SubElement(node_bndbox, 'ymin')
       node_ymin.text = '%s' % box[i][1]
       node_xmax = SubElement(node_bndbox, 'xmax')
       node_xmax.text = '%s' % box[i][2]
       node_ymax = SubElement(node_bndbox, 'ymax')
       node_ymax.text = '%s' % box[i][3]
       #end add detect result object

    if NEED_WRITE_IMAGE == True:
        save_det_image_file = os.path.join(DEST_DIR, tempfilename)
        cv2.imwrite(save_det_image_file, origimg)

    xml = tostring(node_root, pretty_print=True)
    dom = parseString(xml)
    save_xml = os.path.join(DEST_XML_DIR, tempfilename.replace('jpg', 'xml'))
    print(save_xml)
    with open(save_xml, 'wb') as f:
        f.write(xml)

    #cv2.imshow("SSD", origimg)
    #k = cv2.waitKey(0) & 0xff
    #    #Exit if ESC pressed
    #if k == 27 : return False

    return True

for f in os.listdir(test_dir):
    if detect(test_dir + "/" + f) == False:
       break
