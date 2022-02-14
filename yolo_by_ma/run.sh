#!/usr/bin/env bash
mkdir -p ./txt; cp -f ./images/*.txt ./txt
python ./prepare_maimages.py --dwn
pushd images; bash ./down.sh; popd
python ./prepare_maimages.py --conv

python ../common/cdd/convert_darknettxt_dataset.py ./ ./custom_classes.txt
git clone https://github.com/nekobean/pytorch_yolov3
wget https://pjreddie.com/media/files/darknet53.conv.74
python train.py --dataset_dir ./ --weights ./darknet53.conv.74 --config ./yolov3_custom.yaml
