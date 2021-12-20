import os
import argparse
from shutil import copyfile
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Rename all images')
parser.add_argument("--img_dir", default="", help="img directory")
parser.add_argument("--save_dir", default="", help="path to save renamed img")
parser.add_argument("--skip_num", type=int, default="3", help="len of imgs name string")
parser.add_argument("--len_name", type=int, default="5", help="len of imgs name string")
args = parser.parse_args()

idx = 0
img_idx = 1
for img in tqdm(sorted(os.listdir(args.img_dir))):
    if idx % (args.skip_num + 1) == 0:
        img_path = os.path.join(args.img_dir, img)
        if not os.path.exists(args.save_dir):
            os.mkdir(args.save_dir)
        save_path = os.path.join(args.save_dir, img)
        copyfile(img_path, save_path)
        rename = str(img_idx).zfill(args.len_name) + '.png'
        os.rename(save_path, os.path.join(args.save_dir, rename))
        img_idx = img_idx + 1
    idx = idx + 1
