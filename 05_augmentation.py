import xml.etree.ElementTree as ET
import pickle
import os
from os import getcwd
import numpy as np
from PIL import Image
import shutil
import matplotlib.pyplot as plt

import imgaug as ia
from imgaug import augmenters as iaa


ia.seed(1)


def read_xml_annotation(root, image_id):
    in_file = open(os.path.join(root, image_id))
    tree = ET.parse(in_file)
    root = tree.getroot()
    bndboxlist = []

    for object in root.findall('object'):
        bndbox = object.find('bndbox')

        xmin = int(bndbox.find('xmin').text)
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)
        # print(xmin,ymin,xmax,ymax)
        bndboxlist.append([xmin, ymin, xmax, ymax])
        # print(bndboxlist)

    bndbox = root.find('object').find('bndbox')
    return bndboxlist


# (506.0000, 330.0000, 528.0000, 348.0000) -> (520.4747, 381.5080, 540.5596, 398.6603)
def change_xml_annotation(root, image_id, new_target):
    new_xmin = new_target[0]
    new_ymin = new_target[1]
    new_xmax = new_target[2]
    new_ymax = new_target[3]

    in_file = open(os.path.join(root, str(image_id) + '.xml'))
    tree = ET.parse(in_file)
    xmlroot = tree.getroot()
    object = xmlroot.find('object')
    bndbox = object.find('bndbox')
    xmin = bndbox.find('xmin')
    xmin.text = str(new_xmin)
    ymin = bndbox.find('ymin')
    ymin.text = str(new_ymin)
    xmax = bndbox.find('xmax')
    xmax.text = str(new_xmax)
    ymax = bndbox.find('ymax')
    ymax.text = str(new_ymax)
    tree.write(os.path.join(root, str("%06d" % (str(id) + '.xml'))))


def change_xml_list_annotation(root, image_id, new_target, saveroot, id):
    in_file = open(os.path.join(root, str(image_id) + '.xml'))
    tree = ET.parse(in_file)
    elem = tree.find('filename')
    elem.text = (id + '.jpg')
    xmlroot = tree.getroot()
    index = 0

    for object in xmlroot.findall('object'):
        bndbox = object.find('bndbox')

        # xmin = int(bndbox.find('xmin').text)
        # xmax = int(bndbox.find('xmax').text)
        # ymin = int(bndbox.find('ymin').text)
        # ymax = int(bndbox.find('ymax').text)

        new_xmin = new_target[index][0]
        new_ymin = new_target[index][1]
        new_xmax = new_target[index][2]
        new_ymax = new_target[index][3]

        xmin = bndbox.find('xmin')
        xmin.text = str(new_xmin)
        ymin = bndbox.find('ymin')
        ymin.text = str(new_ymin)
        xmax = bndbox.find('xmax')
        xmax.text = str(new_xmax)
        ymax = bndbox.find('ymax')
        ymax.text = str(new_ymax)

        index = index + 1

    aug_xml_file_name = os.path.join(saveroot, id + '.xml')
    print(aug_xml_file_name)
    tree.write(aug_xml_file_name)


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' create done')
        return True
    else:
        print(path + ' dir exist')
        return False


if __name__ == "__main__":

    #ROOT_DIR = '/home/charlie/disk2/dataset/number/data_dataset_voc_test'
    ROOT_DIR = '/home/charlie/disk2/dataset/number/data_dataset_voc'

    IMG_DIR = os.path.join(ROOT_DIR, "JPEGImages")
    XML_DIR = os.path.join(ROOT_DIR, "Annotations")
    AUG_XML_DIR = os.path.join(ROOT_DIR, "Annotations_aug")
    AUG_IMG_DIR = os.path.join(ROOT_DIR, "JPEGImages_aug")

    try:
        shutil.rmtree(AUG_XML_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_XML_DIR)

    try:
        shutil.rmtree(AUG_IMG_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_IMG_DIR)

    AUGLOOP = 5

    boxes_img_aug_list = []
    new_bndbox = []
    new_bndbox_list = []

    seq = iaa.Sequential([
        #iaa.Flipud(0.5),  # vertically flip 20% of all images
        #iaa.Fliplr(0.5),
        iaa.Multiply((0.8, 1.1)),  # change brightness, doesn't affect BBs
        #iaa.GaussianBlur(sigma=(0, 3.0)),  # iaa.GaussianBlur(0.5),
        #iaa.Affine(
        #    translate_px={"x": 15, "y": 15},
        #    scale=(0.5, 0.95),
        #    rotate=(-90, 90)
        #)  # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
    ])

    for root, sub_folders, files in os.walk(XML_DIR):

        for name in files:

            bndbox = read_xml_annotation(XML_DIR, name)
            ori_file_name = name[:-4] +  str("_%02d" %  AUGLOOP )
            #shutil.copy(os.path.join(XML_DIR, ori_file_name + '.xml'), AUG_XML_DIR)
            shutil.copy(os.path.join(XML_DIR, name), os.path.join(AUG_XML_DIR, ori_file_name + '.xml'))
            #shutil.copy(os.path.join(IMG_DIR, ori_file_name + '.jpg'), AUG_IMG_DIR)
            shutil.copy(os.path.join(IMG_DIR, name[:-4] + '.jpg'), os.path.join(AUG_IMG_DIR, ori_file_name + '.jpg'))
            #print(name)

            for epoch in range(AUGLOOP):
                seq_det = seq.to_deterministic()
                img = Image.open(os.path.join(IMG_DIR, name[:-4] + '.jpg'))
                # sp = img.size
                img = np.asarray(img)
                for i in range(len(bndbox)):
                    bbs = ia.BoundingBoxesOnImage([
                        ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                    ], shape=img.shape)

                    bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                    boxes_img_aug_list.append(bbs_aug)

                    # new_bndbox_list:[[x1,y1,x2,y2],...[],[]]
                    n_x1 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x1)))
                    n_y1 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y1)))
                    n_x2 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x2)))
                    n_y2 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y2)))
                    if n_x1 == 1 and n_x1 == n_x2:
                        n_x2 += 1
                    if n_y1 == 1 and n_y2 == n_y1:
                        n_y2 += 1
                    if n_x1 >= n_x2 or n_y1 >= n_y2:
                        print('error', name)
                    new_bndbox_list.append([n_x1, n_y1, n_x2, n_y2])
                image_aug = seq_det.augment_images([img])[0]
                #print(' file: %s , name:%s' % (files,name[:-4]))

                #tempfilename.replace('jpg', 'xml')
                #(filepath, tempfilename) = os.path.split(image_filename)
                (filename, extension) = os.path.splitext(name)
                aug_file_name = filename + str("_%02d" %  epoch )

                path = os.path.join(AUG_IMG_DIR, aug_file_name + '.jpg')
                print(path)
                print(aug_file_name)
                image_auged = bbs.draw_on_image(image_aug, thickness=0)
                Image.fromarray(image_auged).save(path)

                change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR,
                                                                               aug_file_name)
                #print(str("%06d" % (len(files) + int(name[:-4]) + epoch * 250)) + '.jpg')
                new_bndbox_list = []
