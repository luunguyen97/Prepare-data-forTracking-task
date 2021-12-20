echo "SKIP AND RENAME IMAGE SEQUENCE"
DIR=$1
python skip_frame.py \
       --img_dir /home/luunp/HDD/Dataset/Tracker_datasets/HOA-LAC-DATASET/Bridge/${DIR} \
       --save_dir /home/luunp/HDD/Dataset/Tracker_datasets/HOA-LAC-final2/${DIR} \
       --skip_num 3 \
       --len_name 5
echo "DONE"