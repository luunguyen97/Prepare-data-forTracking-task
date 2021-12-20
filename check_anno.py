import argparse
import os
import cv2
import numpy as np
from loguru import logger
from videoanalyst.pipeline.utils.bbox import xywh2xyxy, xyxy2xywh

parser = argparse.ArgumentParser(description='Check annotation')
parser.add_argument('--img_dir', type=str, help='image directory')
parser.add_argument('--anno_file', type=str, help='annotation file')
parser.add_argument('--save', choices=('True', 'False'), help='save img or not')
parser.add_argument('--save_dir', type=str, help='save path')
args = parser.parse_args()


def main():
    logger.debug("\n===========================\n"
                 "Press f to fix bounding box\n"
                 "Press b to go back to the previous image\n"
                 "Press q to quit anytime\n"
                 "==========================\n")
    window_check = 'Check Annotation'
    cv2.namedWindow(window_check)
    cv2.moveWindow(window_check, 0, 0)
    window_fix = 'Fix BBox'

    gt_bbox = np.loadtxt(args.anno_file, delimiter=",")
    list_img = [f for f in os.listdir(args.img_dir) if (str(f))[-3:] == "png"]
    list_img = sorted(list_img)
    idx = 0

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    while idx < len(list_img):
        bbox = gt_bbox[idx]
        bbox = xywh2xyxy(bbox)
        bbox = tuple(map(int, bbox))
        img_path = os.path.join(args.img_dir, list_img[idx])
        frame = cv2.imread(img_path)
        frame_bbox = frame.copy()
        cv2.rectangle(frame_bbox, bbox[:2], bbox[2:], (0, 255, 0))

        cv2.imwrite(os.path.join(args.save_dir, list_img[idx]), frame_bbox)
        cv2.imshow(window_check, frame_bbox)
        key = cv2.waitKey()
        if key == ord("f"):
            cv2.namedWindow(window_fix)
            cv2.moveWindow(window_fix, 700, 0)
            # box = cv2.selectROI(window_name, frame, False, False)
            box = cv2.selectROI(window_fix, frame, False, False)
            gt_bbox[idx] = box
            cv2.destroyWindow(window_fix)
        if key == ord("q"):
            break
        if key == ord("b"):
            idx = idx - 1
            if idx < 0:
                idx = 0
            continue
        idx = idx + 1
    np.savetxt(args.anno_file, gt_bbox, fmt='%d', delimiter=',')
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
