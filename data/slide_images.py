import argparse
import os
import cv2

def slide(raw_input_image_dir, raw_out_image_dir):
    hour = 1
    for file in os.listdir(raw_input_image_dir):
        img = cv2.imread(os.path.join(raw_input_image_dir, file))
        raw_shape = img.shape
        imgsx128 = []
        x=0
        y=0
        while x+128 <= raw_shape[0]:
            while y+128 <= raw_shape[1]:
                slide = img[x:x+128, y:y+128, :]
                imgsx128.append(slide)
                y += 128
            x += 128
            y = 0

        os.makedirs(raw_out_image_dir, exist_ok=True)
        for i, img in enumerate(imgsx128):
            cv2.imwrite(f'{raw_out_image_dir}/hour-{hour}-slide-{i+1}.png', img)

        hour += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', '-i', type=str)
    parser.add_argument('--output-dir', '-o', type=str)
    args = parser.parse_args()
    slide(args.input_dir, args.output_dir)
