#!/usr/bin/env bash
python ./convert_kaggleimages.py --dwn
python ./convert_kaggleimages.py --zip kagglecatsanddogs_3367a.zip
rm -rf PetImages
python ../common/cdd/convert_darknettxt_dataset.py ./ ./custom_classes.txt

git clone https://github.com/nekobean/pytorch_yolov3
wget https://pjreddie.com/media/files/darknet53.conv.74
python train.py --dataset_dir ./ --weights ./darknet53.conv.74 --config ./yolov3_custom.yaml
python inference.py --input ./images/Cat00010000.jpg --output ./output --weights ./train_output/yolov3_final.pth --config ./yolov3_custom.yaml
