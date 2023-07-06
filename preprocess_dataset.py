import numpy as np
import cv2
import math
from scipy import ndimage
from os import listdir
from os.path import isfile, join
from glob import glob
import os.path

def deskew_images(path='./', ext='.TIF'):

    """
        This function receive a path from the dataset and deskew the images
        Args:
            path: './data/dataset' path to dataset
            ext: '.png' Extensions from images
        Return:

    """
    all_tif_file_paths = glob(os.path.join(path, "**", "*"+ext), recursive=True)
    for i, filename in enumerate(all_tif_file_paths):
       print(filename)
deskew_images('/data/landsat9')











def ok():

    imgFullPath = imgPath + image
    img_before = cv2.imread(imgFullPath)
    img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    val, bin_mask = cv2.threshold(img_gray,1,255,cv2.THRESH_BINARY)#cv2.bitwise_not(im)
    img_edges = cv2.Canny(bin_mask, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

    angles = []

    if (lines is not None):
      for x1, y1, x2, y2 in lines[0]:
        # cv2.line(img_before, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

      print(angles)
      median_angle = np.median(angles)

      if (median_angle != 0):
        img_rotated = ndimage.rotate(img_before, median_angle)
      else:
        img_rotated = img_before


      print("Angle is {}".format(median_angle))

      print(imgPath+'deskewed/'+image + '_rotated.jpg')
      cv2.imwrite(imgPath+image + '_rotated.jpg', img_rotated)

