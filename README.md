# Prepare-data-for-Tracking-task
## 0. Download pretrained models for trackers
Create a folder name ``model``, download all the pretrained model in this [link](https://drive.google.com/drive/folders/1uy7mG95tIRT6eXj9csyywAyI9wO6XdjR?usp=sharing) and put it in ``model`` folder

## 1. Select data sequences manually 
Data sequences requirement:
- Data sequence need to be continuous, uninterupted
- The sequence focus on 3 challenges: fast scale, shaking and motion blur
- Choose apprpriate name for the sequence base on the target object, moving direction or challenges

Manually select all the sequences in the dataset and then move to next step

## 2. Skip frame
Skip middle frames to increase scale and shaking speed by runing the script [skip_frame.sh](./skip_frame.sh) (eg: ``source skip_frame.sh Car_in1``).

Script parameter:
```bash
--img_dir: image directory 
--save_dir: directory to save image after skipping middle frames
--skip_num: number of middle frame to skip
--len_name: length of image name in zero filled format (eg: 00001.png with len_name = 5)
```
#### Note:
- The number of image after skipping: 50 < image number < 400
- Need to choose appropriate skip_num to increase scale and shaking speed (choose skip_num = 0 for no skipping option). You may need need to run this script several time and look at the result to choose the appropriate skip num for the sequence

## 3. Mark the object 
In sequences which have multiple objects, we need to choose which object to be tracked. If the sequence only contain one object, you can skip this step

Run the scrip [mark_object.sh](./mark_object.sh) (eg: ``source mark_object.sh Car_in1``) to mark object in Car_in1 directory

After running this scrip, mark the tracked object by selecting a ROI for it and press SPACE to quit and save the frame with marked object in ``Mark_objects`` folder

Repeate step 2 and 3 through all the sequences in the dataset

## 4. Genenrate annotation
Check the marked object in ``Mark_object`` folder.
Generate annotation for the object by running script [gen_anno.sh](./gen_anno.sh) (eg: source gen_anno.sh Car_in1 to generate annotation for this directory). The bounding boxes are in xywh format

Script parameter:
```bash
--config: loaded config file for the tracker (do not change this parameter)
--device: cuda (use for host with GPU)
--img_dir: image directory
--anno_file: path to save annotation file
--auto: if True, running in auto mode , if False, running in semi-auto mode (you can fix the bounding box manually if the tracker generate wrong bounding box)
```
Running in semi-auto mode:
- Press 's' to select the ROI for the tracked object
- Press 'SPACE' to generate bounding box for next frame
- Press 'f' to fix the bounding box
- Press 'q' to quit

Running in auto mode:
- Press 's' to selcect ROI for the object
- Press 'SPACE' to automatically generate bounding box

## 5. Check annotation
Check and fix annotation by running [check_anno.sh](check_anno.sh) (eg: source check_anno.sh Car_in1)

Script parameters:
```bash
- img_dir: image directory
- anno_file: annotation file to check
- save: save image with bounding box in anno_file (True, False)
- save_dir: save image directory if save is set to True
```
Guide:
- Press 'SPACE' to continue
- Press 'f' to fix bounding box
- Press 'b' to go back to the previous image
- Press 'q' to quit

## 6. Create validate dataset
Take 20% of the dataset to make validate dataset.
Generate val json file by running [gen_json.sh](gen_sjon.sh)
This json file is used when evaluate Tracker model on AR benchmark
