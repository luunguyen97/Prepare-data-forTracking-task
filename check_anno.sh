echo "GENERATE ANNOTATION FROM IMAGE DIR"
FOLDER=$1
python check_anno.py \
       --img_dir /home/luunp/HDD/Dataset/Tracker_datasets/HOA-LAC-final/val/${FOLDER} \
       --anno_file /home/luunp/HDD/Dataset/Tracker_datasets/HOA-LAC-final/val/${FOLDER}/groundtruth.txt \
       --save False \
       --save_dir /home/luunp/HDD/Dataset/Tracker_datasets/HOA-LAC-CHECK-ANNO/val/${FOLDER} 