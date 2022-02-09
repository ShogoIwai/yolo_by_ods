#!/usr/bin/env bash
python ./convert_kaggleimages.py --dwn
python ./convert_kaggleimages.py --zip kagglecatsanddogs_3367a.zip
python ../common/cdd/convert_darknettxt_dataset.py ./ ./custom_classes.txt

git clone https://github.com/nekobean/pytorch_yolov3
wget https://pjreddie.com/media/files/darknet53.conv.74
python train.py --dataset_dir ./ --weights ./darknet53.conv.74 --config ./yolov3_custom.yaml
for image in ./images/Cat0001000*.jpg ./images/Dog0001000*.jpg; do
python inference.py --input $image --output ./output --weights ./train_output/yolov3_final.pth --config ./yolov3_custom.yaml
done
