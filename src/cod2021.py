
import json
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import rasterio as rio
from glob import glob
#LANDSAT 8
fname = 'LC08_L1TP_002067_20210923_20211003_02_T1_MTL.json'

with open(fname) as f:
    data = json.load(f)

#S_sentinel_bands = glob("LC08_L1TP_002067_20210923_20211003_02_T1_B5.TIF")
# B5 = rio.open("LC08_L1TP_002067_20210923_20211003_02_T1_B5.TIF")

# #plt.imshow(satdat.read(1), cmap='pink')
# # The dataset reports a band count.
# print(B5.count)

# # And provides a sequence of band indexes.  These are one indexing, not zero indexing like Numpy arrays.
# print(B5.indexes)

# B5 = B5.read(1)
# print(B5)
# B5 = B5[5247:5247+(6481 - 5247), 2303:2303+3598 - 2303]



BIV = cv2.imread('LC08_L1TP_002067_20210923_20211003_02_T1_B5.TIF', cv2.IMREAD_UNCHANGED)
BIV = BIV[2303:2303+3598 - 2303, 5247:5247+(6481 - 5247)]
print(BIV[0:10])
plt.imshow(BIV, cmap='pink')


BV = cv2.imread('LC08_L1TP_002067_20210923_20211003_02_T1_B4.TIF', cv2.IMREAD_UNCHANGED)
BV = BV[2303:2303+3598 - 2303, 5247:5247+(6481 - 5247)]

B_INF = cv2.imread('LC08_L1TP_002067_20210923_20211003_02_T1_B10.TIF', cv2.IMREAD_UNCHANGED)
B_INF = B_INF[2303:2303+3598 - 2303, 5247:5247+(6481 - 5247)]


BIV = cv2.resize(BIV, (1388, 1411))
BV = cv2.resize(BV, (1388, 1411))
B_INF = cv2.resize(B_INF, (1388, 1411))


print(BIV.shape)
cv2.imshow("BIV", BIV)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
cv2.imshow("BV", BV)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("B_INF", B_INF)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

q_cal10 = B_INF# / 1
q_cal4 = BV# / 1
q_cal5 = BIV# / 1

RADIANCE_MULT_BAND_10 = float(data['LANDSAT_METADATA_FILE']['LEVEL1_RADIOMETRIC_RESCALING']['RADIANCE_MULT_BAND_10'])
RADIANCE_ADD_BAND_10 = float(data['LANDSAT_METADATA_FILE']['LEVEL1_RADIOMETRIC_RESCALING']['RADIANCE_ADD_BAND_10'])

L_TOA10 = (RADIANCE_MULT_BAND_10 * q_cal10) + RADIANCE_ADD_BAND_10

REFLECTANCE_MULT_BAND_4 = float(data['LANDSAT_METADATA_FILE']['LEVEL1_RADIOMETRIC_RESCALING']['REFLECTANCE_MULT_BAND_4'])
REFLECTANCE_MULT_BAND_5 = float(data['LANDSAT_METADATA_FILE']['LEVEL1_RADIOMETRIC_RESCALING']['REFLECTANCE_MULT_BAND_5'])
REFLECTANCE_ADD_BAND_4 = float(data['LANDSAT_METADATA_FILE']['LEVEL1_RADIOMETRIC_RESCALING']['REFLECTANCE_ADD_BAND_4'])
REFLECTANCE_ADD_BAND_5 = float(data['LANDSAT_METADATA_FILE']['LEVEL1_RADIOMETRIC_RESCALING']['REFLECTANCE_ADD_BAND_5'])

SUN_ELEVATION = float(data['LANDSAT_METADATA_FILE']['IMAGE_ATTRIBUTES']['SUN_ELEVATION'])
EARTH_SUN_DISTANCE = float(data['LANDSAT_METADATA_FILE']['IMAGE_ATTRIBUTES']['EARTH_SUN_DISTANCE'])
Z = (math.pi / 2) - (SUN_ELEVATION / 2) * math.pi



R_B4 = ((REFLECTANCE_MULT_BAND_4 * q_cal4) + REFLECTANCE_ADD_BAND_4) / (math.cos(Z) * (1 / EARTH_SUN_DISTANCE ** 2))
R_B5 = ((REFLECTANCE_MULT_BAND_5 * q_cal5) + REFLECTANCE_ADD_BAND_5) / (math.cos(Z) * (1 / EARTH_SUN_DISTANCE ** 2))




NDVI = (R_B5 - R_B4) / (R_B5 + R_B4)
print(NDVI.min(), NDVI.max())
#NDVI[np.where(NDVI == 0)] = np.nan

fig, ax = plt.subplots()
im = ax.imshow(NDVI, vmin=0, vmax=1, cmap='hsv')
cbar = fig.colorbar(im)
cbar.ax.set_ylabel('NDVI', fontsize=14)
ax.axis('off')
plt.show()

L = 0.5
SAVI = (1 + L) * (R_B5 - R_B4) / (L + R_B5 + R_B4)

IAF = -np.emath.log10((0.69 - SAVI) / 0.59) / 0.91
IAF = np.real(IAF)

EmissividadeNB = 0.97 - 0.0033 * IAF

K1_CONSTANT_BAND_10 = float(data['LANDSAT_METADATA_FILE']['LEVEL1_THERMAL_CONSTANTS']['K1_CONSTANT_BAND_10'])
K2_CONSTANT_BAND_10 = float(data['LANDSAT_METADATA_FILE']['LEVEL1_THERMAL_CONSTANTS']['K2_CONSTANT_BAND_10'])
TempSuperf = (K2_CONSTANT_BAND_10 / np.log((EmissividadeNB * K1_CONSTANT_BAND_10 / L_TOA10) + 1)) - 273.15
#TempSuperf[np.where(TempSuperf < -20)] = np.nan

fig, ax = plt.subplots()
im = ax.imshow(TempSuperf, cmap='hot')
cbar = fig.colorbar(im)
cbar.ax.set_ylabel('Surface Temperature (°C)', fontsize=14)
ax.axis('off')
plt.show()

x1 = 1
y1 = 1411
x2 = 1388
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