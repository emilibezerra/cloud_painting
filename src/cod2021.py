
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import argparse
import cv2
import numpy as np
import math
from tqdm import tqdm
from glob import glob
import xml.etree.ElementTree as ET
from pathlib import Path



parser = ArgumentParser(description="Calcule NDVI and LST from satelital images", formatter_class=ArgumentDefaultsHelpFormatter)


parser.add_argument('--dataset_path', type=str, default='./data/clipped_dataset',
                    help=('Path to Dataset images'))

parser.add_argument('--xml_path', type=str, default='./data/metadata_xml/',
                    help=('Path to XML folder with metadata'))


def create_dir(path, folder_name):
    """
    Create output folders: NDVI, LST

    Args: path: path to dataset
          folder_name: folder name
    """
    Path(path, folder_name).mkdir(parents=True, exist_ok=True)




#Calcule NDVI and LST -> save data
def calcule_ndvi_lst(dataset_path, xml_path):
    #creating output folders...
    path = 'data/'
    create_dir(path, 'NDVI')
    create_dir(path, 'LST')

    image_filenames=[img_filename for img_filename in glob(dataset_path+"/*")]
    print("INFO: Calculating NDVI and LST to {} images".format(len(image_filenames)))
    for full_filename in tqdm(image_filenames):
        IMG_FILE = cv2.imread(full_filename, cv2.IMREAD_UNCHANGED)
        filename = full_filename.split('/')[-1]
        xml_name = xml_path + filename.split('clipped_')[0]+'MTL.xml'
        tree = ET.parse(xml_name)
        root = tree.getroot()


        BIV = IMG_FILE[:,:,0]
        BV = IMG_FILE[:,:,1]
        B_INF = IMG_FILE[:,:,2]

        q_cal10 = B_INF# / 1
        q_cal4 = BIV# / 1
        q_cal5 = BV# / 1

        RADIANCE_MULT_BAND_10 = float(root.find('./LEVEL1_RADIOMETRIC_RESCALING/RADIANCE_MULT_BAND_10').text)
        RADIANCE_ADD_BAND_10 = float(root.find('./LEVEL1_RADIOMETRIC_RESCALING/RADIANCE_ADD_BAND_10').text)

        L_TOA10 = (RADIANCE_MULT_BAND_10 * q_cal10) + RADIANCE_ADD_BAND_10

        REFLECTANCE_MULT_BAND_4 = float(root.find('./LEVEL1_RADIOMETRIC_RESCALING/REFLECTANCE_MULT_BAND_4').text)
        REFLECTANCE_MULT_BAND_5 = float(root.find('./LEVEL1_RADIOMETRIC_RESCALING/REFLECTANCE_MULT_BAND_5').text)
        REFLECTANCE_ADD_BAND_4 = float(root.find('./LEVEL1_RADIOMETRIC_RESCALING/REFLECTANCE_ADD_BAND_4').text)
        REFLECTANCE_ADD_BAND_5 = float(root.find('./LEVEL1_RADIOMETRIC_RESCALING/REFLECTANCE_ADD_BAND_5').text)

        SUN_ELEVATION = float(root.find('./IMAGE_ATTRIBUTES/SUN_ELEVATION').text)
        EARTH_SUN_DISTANCE = float(root.find('./IMAGE_ATTRIBUTES/EARTH_SUN_DISTANCE').text)
        Z = (math.pi / 2) - (SUN_ELEVATION / 2) * math.pi



        R_B4 = ((REFLECTANCE_MULT_BAND_4 * q_cal4) + REFLECTANCE_ADD_BAND_4) / (math.cos(Z) * (1 / EARTH_SUN_DISTANCE ** 2))
        R_B5 = ((REFLECTANCE_MULT_BAND_5 * q_cal5) + REFLECTANCE_ADD_BAND_5) / (math.cos(Z) * (1 / EARTH_SUN_DISTANCE ** 2))




        NDVI = (R_B5 - R_B4) / (R_B5 + R_B4)
        #NDVI[np.where(NDVI == 0)] = np.nan
        '''
        fig, ax = plt.subplots()
        im = ax.imshow(NDVI, cmap='winter')
        cbar = fig.colorbar(im)
        cbar.ax.set_ylabel('NDVI', fontsize=14)
        ax.axis('off')
        plt.show()
        '''
        L = 0.5
        SAVI = (1 + L) * (R_B5 - R_B4) / (L + R_B5 + R_B4)

        IAF = -np.emath.log10((0.69 - SAVI) / 0.59) / 0.91
        IAF = np.real(IAF)

        EmissividadeNB = 0.97 - 0.0033 * IAF

        K1_CONSTANT_BAND_10 = float(root.find('./LEVEL1_THERMAL_CONSTANTS/K1_CONSTANT_BAND_10').text)
        K2_CONSTANT_BAND_10 = float(root.find('./LEVEL1_THERMAL_CONSTANTS/K2_CONSTANT_BAND_10').text)
        TempSuperf = (K2_CONSTANT_BAND_10 / np.log((EmissividadeNB * K1_CONSTANT_BAND_10 / L_TOA10) + 1)) - 273.15
        #TempSuperf[np.where(TempSuperf < -20)] = np.nan
        '''
        fig, ax = plt.subplots()
        im = ax.imshow(TempSuperf, cmap='hot_r')
        cbar = fig.colorbar(im)
        cbar.ax.set_ylabel('Surface Temperature (°C)', fontsize=14)
        ax.axis('off')
        plt.show()
        '''
        
        cv2.imwrite(path + '/NDVI/' + filename, NDVI)
        cv2.imwrite(path + '/LST/' + filename, TempSuperf)





'''
x1 = 1
y1 = 254
x2 = 254
y2 = 1

a_temp = np.rot90(TempSuperf, 1)
d_a_temp = np.diag(a_temp)

b_temp = cv2.cvtColor(np.float32(NDVI), cv2.COLOR_GRAY2RGB)
b_temp = cv2.line(b_temp, (x1, y1), (x2, y2), (255, 0, 0), 3)

a_ndvi = np.rot90(NDVI, 1)
a_ndvi = a_ndvi
d_a_ndvi = np.diag(a_ndvi)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(d_a_temp, linewidth=2, label='Temperature (°C)')
ax2.plot(d_a_ndvi, linewidth=2, label='NDVI', color='r')
ax1.set_ylabel('Temperature (°C)', fontsize=14)
ax2.set_ylabel('NDVI', fontsize=14)
ax1.set_xlabel('Sampled Pixels', fontsize=14)
ax1.legend(loc='best')
ax2.legend(loc='best')
plt.title('Profile 2010')
plt.show()

rho, pval = np.corrcoef(d_a_temp, d_a_ndvi)
'''




if __name__== "__main__":
  args = parser.parse_args()
  calcule_ndvi_lst(args.dataset_path, args.xml_path)

else:
  print("This script can't be imported as module!")