from glob import glob
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import argparse
import shutil
import matplotlib.pyplot as plt
import numpy as np
import cv2


#clipped_dataset/LC08_L1TP_002066_20230711_20230718_02_T1_clipped_019_005.TIF

NDVI = cv2.imread('clipped_dataset/LC08_L1TP_002066_20230711_20230718_02_T1_clipped_019_005.TIF', cv2.IMREAD_UNCHANGED)
fig, ax = plt.subplots()
im = ax.imshow(NDVI, cmap='winter')
cbar = fig.colorbar(im)
cbar.ax.set_ylabel('NDVI', fontsize=14)
ax.axis('off')
plt.show()

###########################
NDVI_ORIGINAL = cv2.imread('data/test2/NDVI/LC08_L1TP_001067_20210714_20210721_02_T1_clipped_000_003_mirror_crop000.TIF', cv2.IMREAD_UNCHANGED)
fig, ax = plt.subplots()
im = ax.imshow(NDVI, cmap='winter')
cbar = fig.colorbar(im)
cbar.ax.set_ylabel('NDVI', fontsize=14)
ax.axis('off')
plt.show()


LST_ORIGINAL = cv2.imread('data/test2/LST/LC08_L1TP_001067_20210714_20210721_02_T1_clipped_000_003_mirror_crop000.TIF', cv2.IMREAD_UNCHANGED)
fig, ax = plt.subplots()
im = ax.imshow(LST, cmap='hot_r')
cbar = fig.colorbar(im)
cbar.ax.set_ylabel('Surface Temperature (°C)', fontsize=14)
ax.axis('off')
plt.show()



LST = cv2.imread('data/peru_dataset/dataset_14745/train/LC08_L1TP_001067_20210714_20210721_02_T1_clipped_0_0_mirror.png', cv2.IMREAD_UNCHANGED)
fig, ax = plt.subplots()
im_3 = ax.imshow(PERU, cmap='hot_r')
cbar = fig.colorbar(im_3)
cbar.ax.set_ylabel('Surface Temperature (°C)', fontsize=14)
ax.axis('off')
plt.show()

NDVI = cv2.imread('data/LST/val/LC08_L1TP_001067_20210714_20210721_02_T1_clipped_000_003.TIF', cv2.IMREAD_UNCHANGED)
fig, ax = plt.subplots()
im = ax.imshow(NDVI, cmap='winter')
cbar = fig.colorbar(im)
cbar.ax.set_ylabel('NDVI', fontsize=14)
ax.axis('off')
plt.show()

