import os
import shutil


data_path = '../dataset/wind_hrrr_16_128'
validation_path = '../dataset/wind_hrrr_v_16_128'

os.makedirs(os.path.join(validation_path, 'hr_128'), exist_ok=True)
os.makedirs(os.path.join(validation_path, 'lr_16'), exist_ok=True)
os.makedirs(os.path.join(validation_path, 'sr_16_128'), exist_ok=True)

hr_path = os.path.join(data_path, 'hr_128')
lr_path = os.path.join(data_path, 'lr_16')
sr_path = os.path.join(data_path, 'sr_16_128')
files = os.listdir(hr_path)
split_index = int(len(files) * 0.9)

for i in range(split_index, len(files)):
    os.rename(os.path.join(hr_path, files[i]), os.path.join(validation_path, 'hr_128', files[i]))
    os.rename(os.path.join(lr_path, files[i]), os.path.join(validation_path, 'lr_16', files[i]))
    os.rename(os.path.join(sr_path, files[i]), os.path.join(validation_path, 'sr_16_128', files[i]))


