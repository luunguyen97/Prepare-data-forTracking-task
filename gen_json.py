import json
import numpy as np
import os

import argparse

parser = argparse.ArgumentParser(description='Gen json annotation file')
parser.add_argument("--dataset_dir", default="", help="dataset directory")
parser.add_argument("--json_anno", default="", help="path to save json annotaion")
args = parser.parse_args()


json_anno = {}
for sub_dir in sorted(os.listdir(args.dataset_dir)):
    dict = {}
    gt_path = os.path.join(args.dataset_dir, sub_dir, 'groundtruth_rect.txt')
    gt_rect = np.loadtxt(gt_path, delimiter=',')
    gt_rect = gt_rect.astype('int').tolist()

    img_dir = os.path.join(args.dataset_dir, sub_dir, 'img')
    img_list = sorted(os.listdir(img_dir), key=lambda x: int(x.split('.')[0]))
    img_list = [os.path.join(sub_dir, "img", name) for name in img_list]
    assert len(img_list) == len(gt_rect), "number ground truth not fit to number frame"
    xxx = gt_rect[0]
    
    sub_dict = {"video_dir": sub_dir,
                "init_rect": gt_rect[0],
                "img_names": img_list,
                "gt_rect": gt_rect}
    dict[sub_dir] = sub_dict
    # json_anno += dict,
    # json_anno.append(dict)
    json_anno.update(dict)

with open(args.json_anno, 'w') as output:
    json.dump(json_anno, output)
