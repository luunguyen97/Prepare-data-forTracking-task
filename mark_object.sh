echo "SKIP AND RENAME IMAGE SEQUENCE"
DIR=$1
python mark_object.py \
       --img_dir /home/luunp/HDD/Dataset/Tracker_datasets/HOA-LAC-final_v2/${DIR} \
       --save_dir /home/luunp/HDD/Dataset/Tracker_datasets/HOA-LAC-final_v2/Mark_objects
echo "DONE"