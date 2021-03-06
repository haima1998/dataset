#!/usr/bin/env python3

import datetime
import json
import os
import re
import fnmatch
from PIL import Image
import numpy as np
import json
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import cv2
import xml.etree.ElementTree as ET

ROOT_DIR = '/home/charlie/disk2/dataset/number2/data_dataset_voc'
# ROOT_DIR = '/home/charlie/disk2/dataset/witch/data_dataset_voc'
#ROOT_DIR = '/home/charlie/disk2/dataset/voc_test'

IMAGE_DIR = os.path.join(ROOT_DIR, "JPEGImages_aug")
ANNOTATION_DIR = os.path.join(ROOT_DIR, "Annotations_aug")


def filter_for_jpeg(root, files):
    file_types = ['*.jpeg', '*.jpg']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    
    return files


def filter_for_annotations(root, files, image_filename):
    file_types = ['*.xml']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    basename_no_extension = os.path.splitext(os.path.basename(image_filename))[0]
    file_name_prefix = basename_no_extension + '.*'
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    files = [f for f in files if re.match(file_name_prefix, os.path.splitext(os.path.basename(f))[0])]
    #print files

    return files

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


def main():

    # filter for jpeg images
    print(IMAGE_DIR)
    for root, _, files in os.walk(IMAGE_DIR):
        files.sort()
        print(files)
        image_files = filter_for_jpeg(root, files)
        print image_files

        # go through each image
        for image_filename in image_files:
            image = Image.open(image_filename)

            # filter for associated png annotations
            for root, _, files in os.walk(ANNOTATION_DIR):
                annotation_files = filter_for_annotations(root, files, image_filename)

                # go through each associated annotation
                for annotation_filename in annotation_files:

                    print(annotation_filename)
                    print(image_filename)
                    (filepath, tempfilename) = os.path.split(image_filename)
                    (filename, extension) = os.path.splitext(tempfilename)
                    #print(filepath)
                    #print(tempfilename)
 
                    img = cv2.imread(image_filename)
                    height, width, depth = img.shape

                    tree = ET.parse(annotation_filename)
                    root = tree.getroot()
                    lable_str = ''
                    for child in root:
                        #print('child-tag:', child.tag, ',child.attrib', child.attrib, ',child.text:', child.text)
                        x1 = 0
                        y1 = 0
                        x2 = 1
                        y2 = 1

                        for sub in child:
                            #print('sub-tag:', sub.tag, ',sub.attrib:', sub.attrib, ',sub.text:', sub.text)
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

                        #print(x1)
                        #print(y1)
                        #print(x2)
                        #print(y2)
                        print(lable_str)

                        #print('width:%d height:%d lable:%s' % (x2 - x1, y2 - y1 , lable_str))
                        if x1 > 0:
                            cv2.rectangle(img,(x1,y1),(x2,y2),(255,255,0),2)
                            #cv2.putText(img,get_short_name(lable_str),(x1 + 3,y1 - 10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1,cv2.LINE_AA)
                            cv2.putText(img,lable_str,(x1 + 3,y1 - 10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1,cv2.LINE_AA)

                    # if lable_str != 'nine':
                    #     continue

                    cv2.namedWindow(annotation_filename, 0);
                    cv2.resizeWindow(annotation_filename, 1200, 1000);
                    cv2.imshow(annotation_filename,img)
                    k = cv2.waitKey(0)
                    if k == 27:
                        #sys.ext()
                        os._exit(0)
                        break;
                    elif k == -1:
                        cv2.destroyAllWindows()
                        continue
                    else:
                        cv2.destroyAllWindows()
                        print k

if __name__ == "__main__":
    main()



