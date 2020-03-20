import numpy as np  
import sys,os  
import cv2
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import json
import xml.etree.ElementTree as ET


ROOT_DIR = '/home/charlie/disk2/dataset/number/data_dataset_voc'
#ROOT_DIR = '/home/charlie/disk2/dataset/number/test_data_dataset_voc'

detect_result_dir = os.path.join(ROOT_DIR, "det_result/all_xml/")
#detect_result_dir = os.path.join(ROOT_DIR, "result/02ssd_test_all/")

#test_files = os.path.join(ROOT_DIR, "ImageSets/Main/trainval.txt")
test_files = os.path.join(ROOT_DIR, "ImageSets/Main/test.txt")
#test_files = os.path.join(ROOT_DIR, "ImageSets/Main/all.txt")

lable_dir = os.path.join(ROOT_DIR, "Annotations/")
image_dir = os.path.join(ROOT_DIR, "JPEGImages/")
bad_case_image_dir = os.path.join(ROOT_DIR, "det_result/all_xml/all_badcase/")

global detect_obj_count
global lable_obj_count
detect_obj_count = 0
lable_obj_count = 0


global TP
global FP
global FN
TP = 0
FP = 0
FN = 0

global MIN_IOU
MIN_IOU = 0.5
global NEED_CHECK_TYPE
NEED_CHECK_TYPE = True

SHOW_ERROR_DETECTION = True

class DetObject:
    def __init__(self, type, conf,x1,y1,x2,y2):
        self.type = type
        self.conf = conf
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


def get_detect_result(file_name):
    detect_result_file = detect_result_dir + file_name + '.xml'
    print(detect_result_file)
    object_array = []

    tree = ET.parse(detect_result_file)
    root = tree.getroot()

    for child in root:
        #print('child-tag:', child.tag, ',child.attrib', child.attrib, ',child.text:', child.text)
        x1 = 0
        y1 = 0
        x2 = 1
        y2 = 1
        lable_str = ''
        conf = 0.0
        for sub in child:
            #print('sub-tag:', sub.tag, ',sub.attrib:', sub.attrib, ',sub.text:', sub.text)
            if sub.tag == 'name':
                lable_str = sub.text
            if sub.tag == 'conf':
                conf = float(sub.text)
            for subsub in sub:
                #print('subsub-tag:', subsub.tag, ',subsub.attrib:', subsub.attrib, ',subsub.text:', subsub.text)
                if subsub.tag == 'xmin':
                    x1 = int(subsub.text)
                if subsub.tag == 'ymin':
                    y1 = int(subsub.text)
                if subsub.tag == 'xmax':
                    x2 = int(subsub.text)
                if subsub.tag == 'ymax':
                    y2 = int(subsub.text)

        if conf > 0.01:
            #print(lable_str)
            #print(conf)
            #print(x1)
            #print(y1)
            #print(x2)
            #print(y2)
            obj = DetObject(lable_str,conf,x1,y1,x2,y2)
            object_array.append(obj)
        #else:
            #print('no detect result')

    return object_array

def get_lable_objects(file_name):
    detect_result_file = lable_dir + file_name + '.xml'
    print(detect_result_file)
    object_array = []

    tree = ET.parse(detect_result_file)
    root = tree.getroot()

    for child in root:
        #print('child-tag:', child.tag, ',child.attrib', child.attrib, ',child.text:', child.text)
        x1 = 0
        y1 = 0
        x2 = 1
        y2 = 1
        lable_str = ''
        for sub in child:
            #print('sub-tag:', sub.tag, ',sub.attrib:', sub.attrib, ',sub.text:', sub.text)
            have_obj = False
            if sub.tag == 'name':
                lable_str = sub.text
            for subsub in sub:
                #print('subsub-tag:', subsub.tag, ',subsub.attrib:', subsub.attrib, ',subsub.text:', subsub.text)
                if subsub.tag == 'xmin':
                    x1 = int(subsub.text)
                if subsub.tag == 'ymin':
                    y1 = int(subsub.text)
                if subsub.tag == 'xmax':
                    x2 = int(subsub.text)
                if subsub.tag == 'ymax':
                    y2 = int(subsub.text)
                    have_obj = True

            if have_obj == True:
                #print(lable_str)
                #print(x1)
                #print(y1)
                #print(x2)
                #print(y2)
                obj = DetObject(lable_str,1,x1,y1,x2,y2)
                object_array.append(obj)

    return object_array

def get_short_name(obj_type):
    short_name = "UNK"
    if obj_type == "zero":
        short_name = "0"
    if obj_type == "one":
        short_name = "1"
    if obj_type == "two":
        short_name = "2"
    if obj_type == "three":
        short_name = "3"
    if obj_type == "four":
        short_name = "4"
    if obj_type == "five":
        short_name = "5"
    if obj_type == "six":
        short_name = "6"
    if obj_type == "seven":
        short_name = "7"
    if obj_type == "eight":
        short_name = "8"
    if obj_type == "nine":
        short_name = "9"
    return short_name


def show_result(file_name,det_obj_list,lable_obj_list):
    image_file = image_dir + file_name + '.jpg'
    print(image_file)
    img = cv2.imread(image_file)
    #height, width, depth = img.shape
    img_lable = cv2.imread(image_file)

    for obj in det_obj_list:
        cv2.rectangle(img, (obj.x1, obj.y1), (obj.x2, obj.y2), (255, 255, 0), 1)
        cv2.putText(img, get_short_name(obj.type), (obj.x1 + 3, obj.y1 - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
        #cv2.putText(img, str(obj.conf), (obj.x1 + 3, obj.y1 - 23), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

    lable_width = 0
    lable_height = 0
    for obj in lable_obj_list:
        cv2.rectangle(img_lable, (obj.x1, obj.y1), (obj.x2, obj.y2), (0, 255, 0), 1)
        cv2.putText(img_lable, get_short_name(obj.type), (obj.x1 + 3, obj.y1 - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 125, 255), 1, cv2.LINE_AA)
        lable_width = obj.x2 - obj.x1
        lable_height = obj.y2 - obj.y1

    gt_win_str = "GT(" + str(lable_width) + "," + str(lable_height) + ")"
    cv2.imshow("Detect(" + file_name + ")", img)
    cv2.imshow(gt_win_str, img_lable)
    cv2.moveWindow(gt_win_str, 580, 0)
    k = cv2.waitKey(0)
    if k == 27:
        # sys.ext()
        cv2.destroyAllWindows()
        os._exit(0)
    else:
        print k

def write_badcase(file_name,det_obj_list,lable_obj_list):
    image_file = image_dir + file_name + '.jpg'
    print(image_file)
    img = cv2.imread(image_file)
    #height, width, depth = img.shape
    img_lable = cv2.imread(image_file)

    for obj in det_obj_list:
        cv2.rectangle(img, (obj.x1, obj.y1), (obj.x2, obj.y2), (255, 255, 0), 1)
        cv2.putText(img, get_short_name(obj.type), (obj.x1 + 3, obj.y1 - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

    lable_width = 0
    lable_height = 0
    for obj in lable_obj_list:
        cv2.rectangle(img_lable, (obj.x1, obj.y1), (obj.x2, obj.y2), (0, 255, 0), 1)
        cv2.putText(img_lable, get_short_name(obj.type), (obj.x1 + 3, obj.y1 - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 125, 255), 1, cv2.LINE_AA)
        lable_width = obj.x2 - obj.x1
        lable_height = obj.y2 - obj.y1

    gt_image_file = bad_case_image_dir + file_name + "_gt_" + str(lable_width) + "_" +str(lable_height) + ".jpg"
    det_image_file = bad_case_image_dir + file_name + "_det_" + str(len(det_obj_list))  + ".jpg"

    print(gt_image_file)
    print(det_image_file)

    cv2.imwrite(gt_image_file,img_lable)
    cv2.imwrite(det_image_file,img)

def compute_iou(rec1, rec2):
    """
     computing IoU
     :param rec1: (y0, x0, y1, x1), which reflects
             (top, left, bottom, right)
     :param rec2: (y0, x0, y1, x1)
     :return: scala value of IoU
     """
    # computing area of each rectangles
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

    # computing the sum_area
    sum_area = S_rec1 + S_rec2

    # find the each edge of intersect rectangle
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])

    # judge if there is an intersect
    if left_line >= right_line or top_line >= bottom_line:
        #print('no intersect ret (%d,%d,%d,%d)' % (left_line,right_line,top_line,bottom_line))
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        print('have intersect ret (%d,%d,%d,%d,%d)' % (left_line,right_line,top_line,bottom_line,intersect))
        print('iou ret (%d,%d,%d)' % (sum_area,intersect,sum_area - intersect))
        return float(intersect) / float(sum_area - intersect)

def check_detect_result(det_obj_list,lable_obj_list):
    #print('enter check_detect_result')
    global TP
    global FP
    global FN
    global MIN_IOU
    global NEED_CHECK_TYPE
    ret = True

    for lable_obj in lable_obj_list:
        have_match = False
        for det_obj in det_obj_list:
            det_obj_ret = (det_obj.x1,det_obj.y1,det_obj.x2,det_obj.y2)
            lable_obj_ret = (lable_obj.x1,lable_obj.y1,lable_obj.x2,lable_obj.y2)
            #print('det rect(%d,%d,%d,%d)' % (det_obj.x1,det_obj.y1,det_obj.x2,det_obj.y2))
            #print('lable rect(%d,%d,%d,%d)' % (lable_obj.x1,lable_obj.y1,lable_obj.x2,lable_obj.y2))
            iou = compute_iou(det_obj_ret,lable_obj_ret)
            print(' det type:%s ' % det_obj.type)
            print(' lable type:%s' % lable_obj.type)
            print('iou = %f' % iou)
            if iou > MIN_IOU and (det_obj.type == lable_obj.type or NEED_CHECK_TYPE == False):
                have_match = True
        if have_match == False:
            ret = False
            FN = FN + 1
            #print('lable w:%d h:%d ' % (lable_obj.x2 - lable_obj.x1,lable_obj.y2 - lable_obj.y1))

    for det_obj in det_obj_list:
        have_match = False
        for lable_obj in lable_obj_list:
            det_obj_ret = (det_obj.x1,det_obj.y1,det_obj.x2,det_obj.y2)
            lable_obj_ret = (lable_obj.x1,lable_obj.y1,lable_obj.x2,lable_obj.y2)
            #print('det rect(%d,%d,%d,%d)' % (det_obj.x1,det_obj.y1,det_obj.x2,det_obj.y2))
            #print('lable rect(%d,%d,%d,%d)' % (lable_obj.x1,lable_obj.y1,lable_obj.x2,lable_obj.y2))
            iou = compute_iou(det_obj_ret,lable_obj_ret)
            #print('iou = %f' % iou)
            if iou > MIN_IOU and (det_obj.type == lable_obj.type or NEED_CHECK_TYPE == False):
            #if iou > MIN_IOU and (det_obj.type == lable_obj.type or (det_obj.type == 'red_only' and lable_obj.type == 'yellow_only')  or NEED_CHECK_TYPE == False):
                have_match = True

        if have_match == False:
            ret = False
            FP = FP + 1
        else:
            TP = TP + 1


    return ret



def eval_one_frame(file_name):
    global detect_obj_count
    global  lable_obj_count
    #print('eval_one_frame')
    det_obj_list = get_detect_result(file_name)
    detect_obj_count = detect_obj_count + len(det_obj_list)
    #print('detect one frame result')
    print(len(det_obj_list))

    lable_obj_list = get_lable_objects(file_name)
    lable_obj_count =  lable_obj_count + len(lable_obj_list)
    #print('one frame lable count')
    #print(len(lable_obj_list))

    ret = check_detect_result(det_obj_list,lable_obj_list)

    if((len(det_obj_list) != len(lable_obj_list)) or ret != True):
        print(' det_num:%d lable_num:%d ret:%d' % (len(det_obj_list),len(lable_obj_list),ret))
        if SHOW_ERROR_DETECTION == True:
            show_result(file_name,det_obj_list,lable_obj_list)
        else:
            write_badcase(file_name,det_obj_list,lable_obj_list)

def main():
    global detect_obj_count
    global lable_obj_count
    global TP
    global FP
    global FN

    print("eval main enter")
    with open(test_files, "r") as lf:
        for line in lf.readlines():
            line = line.strip('\n')
            #print(line)
            eval_one_frame(line)

    print(' TP: %d, FP: %d, FN: %d , lable_cout %d, detect count:%d' % (TP,FP,FN,lable_obj_count,detect_obj_count))
    recall = float(TP)/float(lable_obj_count)
    precision = float(TP) / float(TP + FP)
    print(' recall:%f  precision:%f' % (recall,precision))


if __name__ == "__main__":
    main()