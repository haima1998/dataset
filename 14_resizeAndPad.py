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
import sys
import cv2 as cv
import numpy as np

ROOT_DIR = '/home/charlie/Pictures'
IMAGE_DIR = os.path.join(ROOT_DIR, "03fruit")
OUTPUT_DIR = os.path.join(IMAGE_DIR, "output")

def resizeAndPad(img, padColor=0):

    in_h, in_w = img.shape[:2]
    print('in image width:%d height:%d ' % (in_w,in_h))

    need_h = in_w * 4 / 3
    pad_height = 0
    if need_h > in_h:
        pad_height =  need_h - in_h
        pad_top = pad_height / 2
        pad_bot = pad_height / 2
        scaled_img = cv2.copyMakeBorder(img, pad_top, pad_bot, 0, 0, borderType=cv2.BORDER_CONSTANT, value=[255,255,255])
        return scaled_img
    else:
        return img


def filter_for_jpeg(root, files):
    file_types = ['*.jpeg', '*.jpg']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]

    return files

def main():
    print(IMAGE_DIR)
    # print(OUTPUT_DIR)

    for root, _, files in os.walk(IMAGE_DIR):
        files.sort()
        image_files = filter_for_jpeg(root, files)

        # go through each image
        for image_filename in image_files:
            print(image_filename)
            (filepath, tempfilename) = os.path.split(image_filename)
            output_file_name = os.path.join(OUTPUT_DIR, tempfilename)

            #A. open one image file
            v_img = cv2.imread(image_filename)

            #B. resize and pad image
            scaled_v_img = resizeAndPad(v_img, 255)
            out_h, out_w = scaled_v_img.shape[:2]
            print('out image width:%d height:%d ' % (out_w,out_h))

            #C. write resize and pad image to output file
            cv2.imwrite(output_file_name, scaled_v_img)
            print(output_file_name)


if __name__ == "__main__":
    main()



