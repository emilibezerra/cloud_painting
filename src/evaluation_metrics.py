from sklearn.model_selection import train_test_split

from skimage.metrics import structural_similarity as ssim
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import argparse
import cv2
import seaborn as sns
import numpy as np
from math import log10, sqrt
from tqdm import tqdm
from glob import glob
import xml.etree.ElementTree as ET
from pathlib import Path
import matplotlib.pyplot as plt



parser = ArgumentParser(description="Split dataset for train, test, validation", formatter_class=ArgumentDefaultsHelpFormatter)


parser.add_argument('--dataset_test_path', type=str, default='data/LST/test',
                    help=('Path to Dataset test images'))
parser.add_argument('--dataset_predicted_path', type=str, default='data/LST/test',
                    help=('Path to Dataset predicted by model'))


def psnr(original, predicted):
    mse = np.mean((original - predicted) ** 2)
    if(mse == 0):  # MSE is zero means no noise is present in the signal .
                  # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr
    

def mse(original, predicted):
    res = np.mean((original - predicted) ** 2)
    return res

def pearson(original, predicted):
    return (np.corrcoef(original.flatten(), predicted.flatten()))

def calculate_metrics(dataset_test_path, dataset_predicted_path):
    #Read all images from folder original - source
    img_test=[img_filename for img_filename in glob(dataset_test_path+"/*.TIF")]
    #Read all images from folder test
    img_predicted=[img_filename for img_filename in glob(dataset_predicted_path+"/*.TIF")]
    #save in vectors mestrics
    mse_res = [] 
    #pearson_res = []
    ssim_res = []
    psnr_res = []
    for i, [test, pred] in tqdm(enumerate(zip(img_test, img_predicted))):

        img_original = cv2.imread(test, cv2.IMREAD_UNCHANGED)
        
        img_reconstructed= cv2.imread(pred, cv2.IMREAD_UNCHANGED)
        img_reconstructed = cv2.blur(img_reconstructed,(5,5))

        (score, diff) = ssim(img_original, img_reconstructed, full=True, data_range=img_original.max() - img_original.min())
        ssim_res.append(score)
        #pearson_res.append(pearson(img_original, compressed))
        mse_res.append(mse(img_original, img_reconstructed))
        psnr_res.append(psnr(img_original, img_reconstructed))
        
    #print metrics
    print("=======================================================")
    print("Evaluation metrics results: \n Mean MSE: {0} \n Mean PSNR: {1} \n Mean SSIM: {2}".format(np.mean(mse_res),np.mean(psnr_res) ,np.mean(ssim_res)))
    print("\n STD MSE: {0} \n STD PSNR: {1} \n STD SSIM: {2}".format(np.std(mse_res),np.std(psnr_res) ,np.std(ssim_res)))
    print("=======================================================")
    fig, axs = plt.subplots(3)
    fig.suptitle('BoxPlot Metrics')
    sns.boxplot([mse_res],  orient='v' , ax=axs[0])
    axs[0].set_title("MSE")
    sns.boxplot([psnr_res],  orient='v' , ax=axs[1])
    axs[1].set_title("PSNR")
    sns.boxplot([ssim_res],  orient='v' , ax=axs[2])
    axs[2].set_title("SSIM")
    plt.show()


if __name__== "__main__":
  args = parser.parse_args()
  calculate_metrics(args.dataset_test_path, args.dataset_predicted_path)

else:
  print("This script can't be imported as module!")
