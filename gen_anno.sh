echo "GENERATE ANNOTATION FROM IMAGE DIR"
DIR=$1
python gen_anno.py \
       --config config/siamfcpp_googlenet.yaml \
       --device cuda \
       --img_dir /home/luunp/HDD/Dataset/Tracker_datasets/HOA-LAC-final_v2/${DIR} \
       --anno_file /home/luunp/HDD/Dataset/Tracker_datasets/HOA-LAC-final2/${DIR}/groundtruth.txt \
       --auto False
