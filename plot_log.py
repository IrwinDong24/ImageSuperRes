import re
import argparse

import numpy as np
from matplotlib import pyplot as plt

train_log_pattern = r'(\d{2}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s*-\s*INFO: <epoch:\s*(\d+),\s*iter:\s*([\d,]+)>\s*l_pix:\s*([\d\.e-]+)'
val_log_pattern = r'(\d{2}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s*-\s*INFO: <epoch:\s*(\d+),\s*iter:\s*([\d,]+)>\s*psnr:\s*([\d\.e\+]+)'


class TrainLog:
    def __init__(self, timestamp, epoch, iteration, lpix):
        self.timestamp = timestamp
        self.epoch = epoch
        self.iteration = iteration
        self.lpix = lpix


class ValLog:
    def __init__(self, timestamp, epoch, iteration, psnr):
        self.timestamp = timestamp
        self.epoch = epoch
        self.iteration = iteration
        self.psnr = psnr


def plot_log(log_file, title):
    train_logs = []
    val_logs = []
    with open(log_file, 'r') as logs:
        for line in logs:
            train_log_match = re.match(train_log_pattern, line)
            if train_log_match:
                timestamp = train_log_match.group(1)
                epoch = int(train_log_match.group(2))
                iter_num = int(train_log_match.group(3).replace(',', '').replace(' ', ''))
                l_pix = float(train_log_match.group(4))
                train_logs.append(TrainLog(timestamp, epoch, iter_num, l_pix))
            else:
                val_log_match = re.match(val_log_pattern, line)
                if val_log_match:
                    timestamp = val_log_match.group(1)
                    epoch = int(val_log_match.group(2))
                    iter_num = int(val_log_match.group(3).replace(',', '').replace(' ', ''))
                    psnr = float(val_log_match.group(4))
                    val_logs.append(ValLog(timestamp, epoch, iter_num, psnr))

    train_loss_dict = {}
    iterations_dict = {}
    for log in train_logs:
        if log.epoch in train_loss_dict:
            train_loss_dict[log.epoch] += log.lpix
            iterations_dict[log.epoch] += 1
        else:
            train_loss_dict[log.epoch] = log.lpix
            iterations_dict[log.epoch] = 1

    for epoch in train_loss_dict:
        train_loss_dict[epoch] /= iterations_dict[epoch]

    epoch_nums = list(train_loss_dict.keys())
    train_loss = list(train_loss_dict.values())

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    axs[0].plot(epoch_nums, train_loss)
    axs[0].set_title('Training Loss')
    axs[0].set_xlabel("Epochs")
    axs[0].set_ylabel("Loss Per Pixel")
    axs[0].grid()

    iter_nums = []
    val_loss = []
    for log in val_logs:
        iter_nums.append(log.iteration)
        val_loss.append(log.psnr)

    axs[1].plot(iter_nums, val_loss)
    axs[1].set_title('Validation')
    axs[1].set_xlabel("Iterations")
    axs[1].set_ylabel("PSNR")

    fig.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.savefig(title+".png")
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-log_file', type=str)
    parser.add_argument('-log_name', type=str)
    args = parser.parse_args()

    plot_log(args.log_file, args.log_name)
