#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import json
import os
import os.path as osp
import sys
import cv2

try:
    import lxml.builder
    import lxml.etree
except ImportError:
    print('Please install lxml:\n\n    pip install lxml\n')
    sys.exit(1)
import numpy as np
import PIL.Image

import labelme


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_dir', help='input annotated directory')
    parser.add_argument('output_dir', help='output dataset directory')
    parser.add_argument('--labels', help='labels file', required=True)
    args = parser.parse_args()


    for label_file in glob.glob(osp.join(args.input_dir, '*.json')):
        print('Generating dataset from:', label_file)
        with open(label_file) as f:
            data = json.load(f)
        base = osp.splitext(osp.basename(label_file))[0]

        img_file = osp.join(osp.dirname(label_file), data['imagePath'])
        img = np.asarray(PIL.Image.open(img_file))

        maker = lxml.builder.ElementMaker()
        xml = maker.annotation(
            maker.folder(),
            maker.filename(base + '.jpg'),
            maker.database(),    # e.g., The VOC2007 Database
            maker.annotation(),  # e.g., Pascal VOC2007
            maker.image(),       # e.g., flickr
            maker.size(
                maker.height(str(img.shape[0])),
                maker.width(str(img.shape[1])),
                maker.depth(str(img.shape[2])),
            ),
            maker.segmented(),
        )

        bboxes = []
        labels = []

        img = cv2.imread(img_file)
        height,width,channels = img.shape

        for shape in data['shapes']:
            if shape['shape_type'] != 'rectangle':
                print('Skipping shape: label={label}, shape_type={shape_type}'
                      .format(**shape))
                continue

            (xmin_f, ymin_f), (xmax_f, ymax_f) = shape['points']
            xmin = int(xmin_f)
            ymin = int(ymin_f)
            xmax = int(xmax_f)
            ymax = int(ymax_f)

            bboxes.append([xmin, ymin, xmax, ymax])
            print('xmin:%d ymin:%d xmax:%d ymax:%d  height:%d width:%d ' % (xmin, ymin, xmax, ymax, height, width))
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 255, 0), 3)

        crop_size = (800, 800)
        img_resize = cv2.resize(img, crop_size)
        cv2.imshow(img_file, img_resize)
        k = cv2.waitKey(0)
        if k == 27:
            # sys.ext()
            os._exit(0)
            break;
        elif k == -1:
            continue
        else:
            print(k)

        #viz = labelme.utils.draw_instances(
        #    img, bboxes, labels, captions=captions
        #)


if __name__ == '__main__':
    main()
