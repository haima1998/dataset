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

#ROOT_DIR = '/home/charlie/disk2/dataset/number/lableme/02_resize'
ROOT_DIR = '/home/charlie/disk2/dataset/number/lableme/04_pad_resize'

IMAGE_DIR = os.path.join(ROOT_DIR, "JPEG")


def filter_for_jpeg(root, files):
    file_types = ['*.jpeg', '*.jpg']
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

            image = cv2.imread(image_filename)
            #crop_size = (800, 800)
            #crop_size = (2592, 1944)

            #img_resize = cv2.resize(image, crop_size)
            #cv2.imwrite(image_filename, img_resize)
            cv2.imwrite(image_filename, image)

if __name__ == "__main__":
    main()



