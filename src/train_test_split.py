from sklearn.model_selection import train_test_split


from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import argparse
import shutil
import numpy as np
import math
from tqdm import tqdm
from glob import glob
import xml.etree.ElementTree as ET
from pathlib import Path



parser = ArgumentParser(description="Split dataset for train, test, validation", formatter_class=ArgumentDefaultsHelpFormatter)


parser.add_argument('--dataset_clipped_path', type=str, default='./data/clipped_dataset',
                    help=('Path to Dataset images'))
parser.add_argument('--dataset_ndvi_path', type=str, default='./data/NDVI',
                    help=('Path to Dataset images'))
parser.add_argument('--dataset_lst_path', type=str, default='./data/LST',
                    help=('Path to Dataset images'))


def create_dir(path):
    """
    Create output folders

    Args: path: path to dataset
          folder_name: folder name
    """
    Path(path, 'train').mkdir(parents=True, exist_ok=True)
    Path(path, 'test').mkdir(parents=True, exist_ok=True)
    Path(path, 'val').mkdir(parents=True, exist_ok=True)




#Calcule NDVI and LST -> save data
def split_data(dataset_clipped_path, dataset_ndvi_path, dataset_lst_path):
    #creating output folders...
    create_dir(dataset_clipped_path)
    create_dir(dataset_ndvi_path)
    create_dir(dataset_lst_path)

    image_filenames=[img_filename for img_filename in glob(dataset_clipped_path+"/*.TIF")]
    

    X_train, test_val = train_test_split(image_filenames, test_size=0.2, random_state=42)
    print("INFO: Spliting dataset: Train {}, Test and Val {} images".format(len(X_train), len(test_val)))


    for image in tqdm(X_train):
       shutil.move(image, image.replace('clipped_dataset/', 'clipped_dataset/train/'))
       shutil.move(image.replace('clipped_dataset/', 'NDVI/'), image.replace('clipped_dataset/', 'NDVI/train/'))
       shutil.move(image.replace('clipped_dataset/', 'LST/'), image.replace('clipped_dataset/', 'LST/train/'))

    test, val = train_test_split(test_val, test_size=0.5, random_state=42)
    for image in tqdm(test):
       shutil.move(image, image.replace('clipped_dataset/', 'clipped_dataset/test/'))
       shutil.move(image.replace('clipped_dataset/', 'NDVI/'), image.replace('clipped_dataset/', 'NDVI/test/'))
       shutil.move(image.replace('clipped_dataset/', 'LST/'), image.replace('clipped_dataset/', 'LST/test/'))
    
    for image in tqdm(val):
       shutil.move(image, image.replace('clipped_dataset/', 'clipped_dataset/val/'))
       shutil.move(image.replace('clipped_dataset/', 'NDVI/'), image.replace('clipped_dataset/', 'NDVI/val/'))
       shutil.move(image.replace('clipped_dataset/', 'LST/'), image.replace('clipped_dataset/', 'LST/val/'))

if __name__== "__main__":
  args = parser.parse_args()
  split_data(args.dataset_clipped_path, args.dataset_ndvi_path, args.dataset_lst_path)

else:
  print("This script can't be imported as module!")