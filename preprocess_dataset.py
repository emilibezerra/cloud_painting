import numpy as np
import cv2
import math
from scipy import ndimage
from os import listdir
from os.path import isfile, join
from glob import glob
import os.path
from pathlib import Path
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import argparse
 

parser = ArgumentParser(description="Preprocess a satelital image dataset", formatter_class=ArgumentDefaultsHelpFormatter)


parser.add_argument('--current_dataset', type=str, default='./',
                    help=('Current dataset path'))

parser.add_argument('--extension', type=str, default='.TIF',
                    help=('Image extension'))
parser.add_argument('--output_desired', type=int, default=256,
                    help=('Dimensionality of output images'))

parser.add_argument('--output_dataset', type=str, default='./',
                    help=('Path to save images generated'))


IMAGE_EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'pgm', 'png', 'ppm',
                    'tif', 'tiff', 'webp'}

def adjust_size(img, output_size):
  """
        This function receive an image and an output_size (to compute the final size image),
        and transform image shape to square
        Args:
            img: uint8
            output_size: '256' Extensions from images
        Return:
              image croped
  """
  shape = img.shape
  x, y = shape[1], shape[0]
  if y < x:
    if y % output_size != 0:
      y = y- (y % output_size)
    return img[:y,:x-(x-y)]
  else:
    if x % output_size != 0:
      x = shape[1] - (x % output_size)
    return img[:y-(y-x),:x]

def crop_image(img=None, output_size=256):
  """
        This function receive an image and an output_size (to compute the final size image),
        and crop the image erasing the background 
        Args:
            img: uint8
            output_size: '256' Extensions from images
        Return:
              image croped
  """
  print("INFO: croping and adjusting image...")
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img_gray = cv2.GaussianBlur(img_gray, (11, 11), 0)
  val, bin_mask = cv2.threshold(img_gray,1,255,cv2.THRESH_BINARY)#cv2.bitwise_not(im)
  edged = cv2.Canny(bin_mask, 10, 250, apertureSize=3)
  (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  idx = 0
  for c in cnts:
      x,y,w,h = cv2.boundingRect(c)
      if w>200 and h>200:
          idx+=1
          pad_x, pad_y = 100, 100
          new_img=img[y+pad_y:y+h-pad_y,x+pad_x:x+w-pad_x]
  new_img = adjust_size(new_img, output_size=output_size)
  return new_img



def split_image(img=None, patch_size=256, img_path = '', dataset_path=''):
  """
        This function receive an image, patch_size (output_size), img_path (path to image)
        an dataset_path (Output dataset path), and split an big image (e.g. 1000x1000) into many images (100x100)
        and save into a folder
        Args:
            img: uint8
            patch_size: '256' size of path, or size output image
            img_path : path to current image
            dataset_path: path to output dataset to save all croped images
        Return:
              NULL
  """
  # Setup hyperparameters and make sure img_size and patch_size are compatible
  print("INFO: spliting image: ", img_path)
  img_size = img.shape[0]
  num_patches = img_size/patch_size
  assert img_size % patch_size == 0, "Image size must be divisible by patch size"
  print(f"Number of patches per row: {num_patches}\
          \nNumber of patches per column: {num_patches}\
          \nTotal patches: {num_patches*num_patches}\
          \nPatch size: {patch_size} pixels x {patch_size} pixels")
  # Loop through height and width of image
  for i, patch_height in enumerate(range(0, img_size, patch_size)): # iterate through height
      for j, patch_width in enumerate(range(0, img_size, patch_size)): # iterate through width
          img_filename = img_path.split('/')[-1].split('.')[0]
          cv2.imwrite(dataset_path + img_filename + str(i)+'_'+str(j)+'.tif', img[patch_height:patch_height+patch_size, # iterate through height
                                          patch_width:patch_width+patch_size, # iterate through width
                                          :])
          
def deskew_images(path='./', ext='.TIF', output_size=256, dataset_output=''):

    """
        This function receive a path from the dataset and deskew the images
        Args:
            path: './data/dataset' path to dataset
            ext: '.png' Extensions from images
        Return:
              null
    """
    all_tif_file_paths = glob(os.path.join(path, "**", "*"+ext), recursive=True)
    all_tif_file_paths = ["data/LC08_L1TP_001067_20210714_20210721_02_T1_B10.TIF"]
    #print(all_tif_file_paths)
    for i, imgFullPath in enumerate(all_tif_file_paths):
      print("INFO: reading image"+ imgFullPath)
      img_before = cv2.imread(imgFullPath, cv2.IMREAD_UNCHANGED)
      img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
      val, bin_mask = cv2.threshold(img_gray,1,255,cv2.THRESH_BINARY)#cv2.bitwise_not(im)
      img_edges = cv2.Canny(bin_mask, 100, 100, apertureSize=3)
      lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
      angles = []
      cv2.imshow('graycsale image',img_edges)
 
      # waitKey() waits for a key press to close the window and 0 specifies indefinite loop
      cv2.waitKey(0)
      
      # cv2.destroyAllWindows() simply destroys all the windows we created.
      cv2.destroyAllWindows()
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

        new_img = crop_image(img_rotated, output_size)
        split_image(new_img, 256, imgFullPath, dataset_output)
        print("INFO: image "+ imgFullPath + " splited with sucessfully! ")


def main():
  args = parser.parse_args()
  print(args.current_dataset, args.extension, args.output_desired, args.output_dataset)
  deskew_images(args.current_dataset, args.extension, args.output_desired, args.output_dataset)

if __name__== "__main__":
  main()
else:
   deskew_images(current_dataset='./data/landsat9/', ext='.TIF', output_size=256, dataset_output='./data/landsat9/')