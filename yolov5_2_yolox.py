import xml.etree.ElementTree as ET
import json
import cv2
import os
import io
from cv2 import VideoWriter_fourcc
import glob


def get_name(id):
    if id == "0":
        label = 'human'
        return label
    elif id == "1":
        label = 'car'
        return label
    elif id =="2":
        label = 'animal'
        return label



# This is the parent (root) tag
# onto which other tags would be
# created
for filename in glob.glob('labels/*.txt'):
    basename_without_ext = os.path.splitext(os.path.basename(filename))[0]
    ext = os.path.splitext(os.path.basename(filename))[1]
    img2 = cv2.imread('images/'+basename_without_ext + '.jpg')
    file_name = basename_without_ext + ".jpg"
    height, width, layers = img2.shape
    # inside our root tag
    data = ET.Element('annotation')
    element1 = ET.SubElement(data, 'filename')
    element1.text = file_name
    element2 = ET.SubElement(data, 'path')
    element2.text = file_name
    element3 = ET.SubElement(data, 'size')
    s_elem1 = ET.SubElement(element3, 'width')
    s_elem1.text = str(width)
    s_elem2 = ET.SubElement(element3, 'height')
    s_elem2.text = str(height)
    s_elem3 = ET.SubElement(element3, 'depth')
    s_elem3.text = "3"
    element5 = ET.SubElement(data, 'segmented')
    element5.text = "0"
    try:
        try:
            with open('labels/'+basename_without_ext + '.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    s = line.strip().split('\t')
                    centerx = 0
                    centery = 0
                    w = 0
                    h = 0
                    id = 0
                    id = s(0)
                    elementobject = ET.SubElement(data, 'object')
                    s_elem_bndbox = ET.SubElement(elementobject, 'bndbox')
                    s_elem_name = ET.SubElement(elementobject, 'name')
                    name = get_name(id)
                    s_elem_name.text = name
                    # print('width',width)
                    # print('s', s)
                    # print('(s[1])',s[1])
                    centerx = float(s[1]) * width
                    centery = float(s[2]) * height
                    w = float(s[3]) * width
                    h = float(s[4]) * height
                    x1 = float(centerx - w / 2)
                    y1 = float(centery - h / 2)
                    x2 = float(centerx + w / 2)
                    y2 = float(centery + h / 2)

                    s_elem1 = ET.SubElement(s_elem_bndbox, 'xmin')
                    s_elem1.text = str(round(x1,2))
                    s_elem2 = ET.SubElement(s_elem_bndbox, 'ymin')
                    s_elem2.text = str(round(y1,2))
                    s_elem3 = ET.SubElement(s_elem_bndbox, 'xmax')
                    s_elem3.text = str(round(x2,2))
                    s_elem3 = ET.SubElement(s_elem_bndbox, 'ymax')
                    s_elem3.text = str(round(y2,2))

        except Exception:
            with open('labels/'+basename_without_ext + '.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    s = line.strip().split(' ')
                    centerx = 0
                    centery = 0
                    w = 0
                    h = 0
                    id = 0
                    id = s[0]
                    elementobject = ET.SubElement(data, 'object')
                    s_elem_bndbox = ET.SubElement(elementobject, 'bndbox')
                    s_elem_name = ET.SubElement(elementobject, 'name')
                    name = get_name(id)
                    s_elem_name.text = name
                    if s[1] != '':
                        centerx = float(s[1]) * width
                        centery = float(s[2]) * height
                        w = float(s[3]) * width
                        h = float(s[4]) * height
                    else:
                        centerx = float(s[2]) * width
                        centery = float(s[3]) * height
                        w = float(s[4]) * width
                        h = float(s[5]) * height
                    x1 = float(centerx - w / 2)
                    y1 = float(centery - h / 2)
                    x2 = float(centerx + w / 2)
                    y2 = float(centery + h / 2)
                    s_elem1 = ET.SubElement(s_elem_bndbox, 'xmin')
                    s_elem1.text = str(round(x1,2))
                    s_elem2 = ET.SubElement(s_elem_bndbox, 'ymin')
                    s_elem2.text = str(round(y1,2))
                    s_elem3 = ET.SubElement(s_elem_bndbox, 'xmax')
                    s_elem3.text = str(round(x2,2))
                    s_elem3 = ET.SubElement(s_elem_bndbox, 'ymax')
                    s_elem3.text = str(round(y2,2))


    except Exception:
        print("error")
        pass

    # Converting the xml data to byte object,
    # for allowing flushing data to file
    # stream
    b_xml = ET.tostring(data)

    # Opening a file under the name `items2.xml`,
    # with operation mode `wb` (write + binary)
    with open('labels/'+basename_without_ext + ".xml", "wb") as f:
        f.write(b_xml)
