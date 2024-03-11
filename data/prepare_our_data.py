import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

def to_rgb_image(array):
    # Normalize the values to the range [0, 1]
    array_normalized = (img.values - img.values.min()) / (img.values.max() - img.values.min())
    rgba_image = cmap(array_normalized)
    rgb = np.delete(rgba_image, 3, axis=-1)  # Remove the alpha channel
    return rgb

# 载入NetCDF文件
file_path = './wind/ws_100m_2018_01_10days.nc'
data = xr.open_dataset(file_path)
cmap = plt.get_cmap('viridis')
for i in range(240):
    time_index = i
    imgsx512 = []
    for j in range(7):
        imgsx512.append(data['windspeed_100m'][time_index, 50:562, j*73:512+j*73])
        imgsx512.append(data['windspeed_100m'][time_index, 100:612, j * 73:512 + j * 73])

    for j, img in enumerate(imgsx512):
        rgb_image = to_rgb_image(img)
        plt.imsave(f'./wind/512/hour-{i}-slide-{j}.png', rgb_image)

    imgsx128 = []
    for j in range(7):
        for k in range(2):
            imgsx128.append(data['windspeed_100m'][time_index, 198+128*k:326+128*k, 256+50*j:384+50*j])

    for j, img in enumerate(imgsx128):
        rgb_image = to_rgb_image(img)
        plt.imsave(f'./wind/128/hour-{i}-slide-{j}.png', rgb_image)

