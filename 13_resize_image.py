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

# DEST_DIR = '/home/charlie/Pictures/output'
# INPUT_IMAGE_FILE = '/home/charlie/Pictures/appicon_1024.png'



def main():
            output_x = int(sys.argv[1])
            output_y = int(sys.argv[2])
            input_file_name = sys.argv[3]
            output_dir = sys.argv[4]

            print(input_file_name)

            image_filename = input_file_name

            (filepath, tempfilename) = os.path.split(image_filename)
            (filename, extension) = os.path.splitext(tempfilename)

            new_file_name = filename + '_' + str(output_x) + '_' + str(output_y) + '.png'
            save_file_name = os.path.join(output_dir, new_file_name)
            print(new_file_name)

            #A .read source image file
            image = cv2.imread(image_filename,cv2.IMREAD_UNCHANGED)

            #B. resize
            img_dst = cv2.resize(image, (output_x, output_y))
            print(img_dst.shape)

            #D. save result image to file
            cv2.imwrite(save_file_name, img_dst)

if __name__ == "__main__":
    main()



