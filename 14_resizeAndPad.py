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

# DEST_DIR = '/home/charlie/Pictures/output'
# INPUT_IMAGE_FILE = '/home/charlie/Pictures/appicon_1024.png'

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

def main():
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    print(input_file_name)
    print(output_file_name)

    v_img = cv2.imread(input_file_name) # vertical image

    scaled_v_img = resizeAndPad(v_img, 255)

    out_h, out_w = scaled_v_img.shape[:2]
    print('out image width:%d height:%d ' % (out_w,out_h))

    cv2.imwrite(output_file_name, scaled_v_img)

if __name__ == "__main__":
    main()



