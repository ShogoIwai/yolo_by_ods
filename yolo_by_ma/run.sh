#!/usr/bin/env bash
mkdir -p ./txt ; cp -f ./images/*.txt ./txt
python ./convert_maimages.py --dwn
pushd images
bash ./down.sh
popd
python ./convert_maimages.py --conv
