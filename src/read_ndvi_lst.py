from glob import glob
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import argparse
import shutil
import matplotlib.pyplot as plt
import numpy as np
import cv2

NDVI = cv2.imread('data/NDVI/LC08_L1TP_001067_20210714_20210721_02_T10_2.TIF', cv2.IMREAD_UNCHANGED)
fig, ax = plt.subplots()
im = ax.imshow(NDVI, cmap='winter')
cbar = fig.colorbar(im)
cbar.ax.set_ylabel('NDVI', fontsize=14)
ax.axis('off')
plt.show()

LST = cv2.imread('data/LST/LC08_L1TP_001067_20210714_20210721_02_T10_2.TIF', cv2.IMREAD_UNCHANGED)
fig, ax = plt.subplots()
im = ax.imshow(LST, cmap='hot_r')
cbar = fig.colorbar(im)
cbar.ax.set_ylabel('Surface Temperature (°C)', fontsize=14)
ax.axis('off')
plt.show()