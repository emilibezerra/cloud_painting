from glob import glob
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import argparse
import shutil
from tqdm import tqdm
import numpy as np
import cv2

parser = ArgumentParser(description="Preprocess a satelital image dataset", formatter_class=ArgumentDefaultsHelpFormatter)


parser.add_argument('--dataset', type=str, default='./data/',
                    help=('Path to image folder bands (B4, B5, B10)'))

parser.add_argument('--output_dataset', type=str, default='./data/combined_dataset/',
                    help=('Path to combined dataset'))

def load_masks(dataset, output_dataset):
  """
        This function receive a path to image folder bandas dataset and concat all bands into an image
        and save in the output folder combined dataset
        Args:
            dataset: Path to image folder bands
            output_dataset:path to output combined dataset 
  """
  image_filenames_b4=[img_filename for img_filename in glob(dataset+"/B4/*")]

  print("INFO: concatenating bands...")

  for  b4_filename in tqdm(image_filenames_b4):
    #mask_filename = mask_filenames[random.randint(0, len(mask_filenames))]
    b5_filename = b4_filename.replace(b4_filename.split('_')[-1], 'B5.TIF').replace('B4','B5')
    b10_filename = b4_filename.replace(b4_filename.split('_')[-1], 'B10.TIF').replace('B4','B10')
    #print(b5_filename)
    b4 = cv2.imread(b4_filename, cv2.IMREAD_UNCHANGED)
    b5 = cv2.imread(b5_filename, cv2.IMREAD_UNCHANGED)
    b10 = cv2.imread(b10_filename, cv2.IMREAD_UNCHANGED)
    img_res = np.dstack([b4, b5, b10])
    img_res_filename = output_dataset + '/' + b4_filename.split('\\')[-1].replace('_' + b4_filename.split('_')[-1], '.TIF')
    cv2.imwrite(img_res_filename, img_res)
    #print("INFO: image "+ img_res_filename + " splited with sucessfully! ")
    
    #shutil.copyfile(mask, out_mask_dataset+'/'+mask_filename)


if __name__== "__main__":
    args = parser.parse_args()
    load_masks(args.dataset, args.output_dataset)
else:
  print("This script can't be imported as module!")