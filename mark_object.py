import os
import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser(description='Rename all images')
parser.add_argument("--img_dir", default="", help="img directory")
parser.add_argument("--save_dir", default="", help="path to save renamed img")
args = parser.parse_args()


def xywh2xyxy(rect):
    rect = np.array(rect, dtype=np.float32)
    return np.concatenate([
        rect[..., [0]], rect[..., [1]], rect[..., [2]] + rect[..., [0]] - 1,
                                        rect[..., [3]] + rect[..., [1]] - 1
    ],
        axis=-1)


if not os.path.exists(args.save_dir):
    os.makedirs(args.save_dir)

window_name = 'Mark Object'
list_img = [f for f in os.listdir(args.img_dir) if (str(f))[-3:] == "png"]
list_img = sorted(list_img)

first_frame = cv2.imread(os.path.join(args.img_dir, list_img[0]))
bbox = cv2.selectROI(window_name, first_frame, fromCenter=False, showCrosshair=False)
bbox = xywh2xyxy(bbox)
bbox = tuple(map(int, bbox))
cv2.rectangle(first_frame, bbox[:2], bbox[2:], (0, 255, 0))
frame_name = os.path.basename(os.path.normpath(args.img_dir)) + '.png'
cv2.imwrite(os.path.join(args.save_dir, frame_name), first_frame)
cv2.destroyAllWindows()