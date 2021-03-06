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
from PIL import Image
import time

ROOT_DIR = '/home/charlie/disk2/dataset/magic/01orin_pic'
DEST_DIR = '/home/charlie/disk2/dataset/magic/lableme/20200406_train/JPEG'
IMAGE_DIR = os.path.join(ROOT_DIR, "20200406_train")

RESIZE = 1.3
#CROP_SIZE = 130
CROP_SIZE = 0

def filter_for_jpeg(root, files):
    file_types = ['*.jpeg', '*.jpg','*.JPG']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]

    return files



def main():

    # filter for jpeg images
    print(IMAGE_DIR)
    for root, _, files in os.walk(IMAGE_DIR):
        print(files)
        image_files = filter_for_jpeg(root, files)
        print image_files

        # go through each image
        for image_filename in image_files:

            (filepath, tempfilename) = os.path.split(image_filename)
            (filename, extension) = os.path.splitext(tempfilename)

            current_time = time.strftime("%Y_%m_%d_%H_%M_", time.localtime())
            # print(current_time)
            # new_file_name = filename + '.jpg'
            new_file_name = current_time + filename + '.jpg'
            save_file_name = os.path.join(DEST_DIR, new_file_name)
            print(new_file_name)

            #A .read source image file
            image = cv2.imread(image_filename)

            #B. resize
            size = image.shape
            resize_width = size[1] / RESIZE
            resize_height = size[0] / RESIZE
            img_dst = cv2.resize(image, (int(resize_width), int(resize_height)))

            #C. crop top image
            size_resize = img_dst.shape
            cv2.rectangle(img_dst, (0, 0), (size_resize[0], CROP_SIZE), (0, 0, 0), -1)

            #D. save result image to file
            cv2.imwrite(save_file_name, img_dst)

if __name__ == "__main__":
    main()



