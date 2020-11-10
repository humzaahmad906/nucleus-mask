import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET

root_dir = "/home/humza/Downloads/dataset3/"
image_dir = 'TissueImages/TissueImages/'
annotation_dir = 'Annotations/Annotations/'
image_files = []
mask_files = []
for file in os.listdir(root_dir+image_dir):
    if file.endswith(".tif") or file.endswith(".tiff"):
        # print(os.path.join("/mydir", file))
        image_files.append(root_dir+image_dir+file)
        name = file.split('.')
        mask_files.append(root_dir + annotation_dir + name[0]+'.xml')
# print(image_files, mask_files)
for i in range(len(mask_files)):
    root = ET.parse(mask_files[i]).getroot()
    annotation_points = []
    for annotation in root:
        for regions in annotation:
            if regions.tag=='Regions':
                for region in regions:
                    if region.tag=='Region':
                        region_list = []
                        for vertices in region:
                            if vertices.tag=='Vertices':
                                verices_list = []
                                for vertix in vertices:
                                    # print(vertix.tag)
                                    if vertix.tag=='Vertex':
                                        try:
                                            # verices_list.append({'X': vertix.attrib['X'], 'Y': vertix.attrib['Y']})
                                            verices_list.append([float(vertix.attrib['X']),float(vertix.attrib['Y'])])
                                        except:
                                            a=0
                                        # verices_list.append({'X': vertix.attrib.X, 'Y': vertix.attrib.Y})
                                region_list.append(verices_list)
                        annotation_points.append(region_list)

    img = cv2.imread(image_files[i])
    zero_img = np.zeros(img.shape[0:2], np.uint8)
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,200,255,0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)
    ann_con = []
    for annotation_point in annotation_points:
        if annotation_point[0]:
            cv2.fillPoly(zero_img, pts=np.int32(annotation_point), color=1)

    fileName = mask_files[i]
    cv2.imwrite(fileName.split('.')[0]+'.png', zero_img)
