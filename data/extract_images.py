import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from pathlib import Path
import glob

cmap_viridis = plt.get_cmap('viridis')

def to_rgb_image(img):
    # Normalize the values to the range [0, 1]
    array_normalized = (img - img.min()) / (img.max() - img.min())
    rgba_image = cmap_viridis(array_normalized)
    rgb = np.delete(rgba_image, 3, axis=-1)  # Remove the alpha channel
    return rgb


for file in (bar := tqdm(glob.glob('../wind/*.nc'))):
    bar.set_description(f'extracting {file}')
    path = Path(file)
    if path.suffix == '.nc':
        stem = path.stem
        os.makedirs(f"../wind/{stem}", exist_ok=True)
        data = xr.open_dataset(f'../wind/{file}')
        data_key = next(iter(data.dtypes.mapping.keys()))
        ws_data = data[data_key].values
        print(ws_data.shape)

        for i in (sub_bar := tqdm(range(ws_data.shape[0]))):
            sub_bar.set_description(f'extracting image ')
            time_index = i + 1
            rgb_img = to_rgb_image(ws_data[i, 250:1700, 100:2600])
            plt.imsave(f'../wind/{stem}/raw_{time_index}.png', rgb_img)
