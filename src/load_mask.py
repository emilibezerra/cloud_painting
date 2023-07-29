from glob import glob
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import argparse
import shutil
import random
import numpy as np
import cv2

parser = ArgumentParser(description="Preprocess a satelital image dataset", formatter_class=ArgumentDefaultsHelpFormatter)


parser.add_argument('--image_dataset', type=str, default='./',
                    help=('Path to Dataset images'))

parser.add_argument('--mask_dataset', type=str, default='./',
                    help=('Image extension'))

parser.add_argument('--output_maskDataset', type=str, default='./',
                    help=('Path to save images generated'))

def load_masks(image_dataset=None, mask_dataset=None, out_mask_dataset=None):
  """
        This function receive a path to images dataset and select a random mask to them
        and save in the output folder
        Args:
            image_dataset: path to image dataset
            mask_dataset:  path to masks dataset
            out_mask_dataset: path to output dataset maks
  """
  image_filenames=[img_filename for img_filename in glob(image_dataset+"/*")]
  mask_filenames=[img_filename for img_filename in glob(mask_dataset+"/*")]
  shape = cv2.imread(image_filenames[0]).shape
  print("INFO: selecting masks to dataset \n Shape will be: {} \n ================================".format(shape))

  for idx, img in enumerate(image_filenames):
    mask_filename = mask_filenames[random.randint(0, len(mask_filenames))]
    mask = cv2.imread(mask_filename)
    mask = cv2.resize(mask, (shape[0], shape[1]), interpolation=cv2.INTER_NEAREST)
    mask_filename = img.split('/')[-1]
    #print(out_mask_dataset+'/'+mask_filename)
    cv2.imwrite(out_mask_dataset+'/'+mask_filename, mask)
    #shutil.copyfile(mask, out_mask_dataset+'/'+mask_filename)

def main():
  args = parser.parse_args()
  load_masks(args.image_dataset, args.mask_dataset, args.output_maskDataset)

if __name__== "__main__":
  main()
else:
  print("This script can't be imported as module!")