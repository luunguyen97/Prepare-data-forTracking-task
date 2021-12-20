# -*- coding: utf-8 -*
import argparse
import os
import cv2
from loguru import logger
import numpy as np
import torch
from videoanalyst.config.config import cfg, specify_task
from videoanalyst.model import builder as model_builder
from videoanalyst.pipeline import builder as pipeline_builder
from videoanalyst.pipeline.utils.bbox import xywh2xyxy

parser = argparse.ArgumentParser(description='Generate annotation from images directory')
parser.add_argument('--config', type=str, help='experiment configuration')
parser.add_argument('--device', type=str, default='cuda', help='torch.device, cuda or cpu')
parser.add_argument('--img_dir', type=str, help='image directory')
parser.add_argument('--anno_file', type=str, help='annotation file')
parser.add_argument('--auto', choices=('True', 'False'), help='auto generate bounding box')
args = parser.parse_args()

font_size = 0.5
font_width = 1


def main():
    root_cfg = cfg
    root_cfg.merge_from_file(args.config)
    # logger.info("Load experiment configuration at: %s" % args.config)

    # resolve config
    root_cfg = root_cfg.test
    task, task_cfg = specify_task(root_cfg)
    task_cfg.freeze()
    window_name = 'Generate Bounding Box'
    # build model
    model = model_builder.build(task, task_cfg.model)
    # build pipeline
    pipeline = pipeline_builder.build(task, task_cfg.pipeline, model)
    dev = torch.device(args.device)
    pipeline.set_device(dev)
    init_box = None
    # init_box = (355, 198, 63, 138)
    template = None

    frame_idx = 0
    gt_bbox = []
    initialized = False
    all_img = sorted(os.listdir(args.img_dir))
    all_img = [image for image in all_img if image.endswith(".png")]
    logger.debug("\n===========================\n"
                 "Press s to start annotating\n"
                 "Press f to fix bounding box\n"
                 # "Press b to go back to the previous image"
                 "Press q to quit anytime\n"
                 "==========================\n")

    for img in all_img:
        frame_path = os.path.join(args.img_dir, img)
        frame = cv2.imread(frame_path)
        if initialized:
            rect_pred = pipeline.update(frame)
            logger.debug(f"Created bounding box #{frame_idx}: {rect_pred}")
            show_frame = frame.copy()
            bbox_pred = xywh2xyxy(rect_pred)
            bbox_pred = tuple(map(int, bbox_pred))
            cv2.rectangle(show_frame, bbox_pred[:2], bbox_pred[2:],
                          (0, 255, 0))
            cv2.imshow(window_name, show_frame)

            if args.auto == 'True':
                cv2.waitKey()
                gt_bbox.append(rect_pred)
            else:
                # Manually fix bbox if tracker generates wrong bbox
                key = cv2.waitKey()
                if key == ord("f"):
                    logger.debug("FIX BOUNDING BOX OF THE OBJECT")
                    box = cv2.selectROI(window_name,
                                        frame,
                                        fromCenter=False,
                                        showCrosshair=False)
                    if box[2] > 0 and box[3] > 0:
                        init_box = box
                    gt_bbox.append(init_box)
                    pipeline.init(frame, init_box)
                    logger.debug(" FIXED BOUNDING BOX : {}".format(init_box))
                else:
                    gt_bbox.append(rect_pred)
                if key == ord("q"):
                    break
        if not initialized:
            cv2.imshow(window_name, frame)
            key = cv2.waitKey()
            if key == ord("s"):
                # select the bounding box of the object we want to track
                # make sure you press ENTER or SPACE after selecting the ROI
                logger.debug("Select object to track")
                box = cv2.selectROI(window_name,
                                    frame,
                                    fromCenter=False,
                                    showCrosshair=False)
                if box[2] > 0 and box[3] > 0:
                    init_box = box
                template = cv2.resize(frame[int(init_box[1]):int(init_box[1] + init_box[3]),
                                      int(init_box[0]):int(init_box[0] + init_box[2])], (128, 128))
                pipeline.init(frame, init_box)
                gt_bbox.append(init_box)
                logger.debug("pipeline initialized with bbox : {}".format(init_box))
                initialized = True
            else:
                break
        frame_idx += 1
    # Saving annotation
    np.savetxt(args.anno_file, gt_bbox, fmt='%d', delimiter=',')
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
