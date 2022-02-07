#!/usr/bin/env bash
python ./convert_maimages.py --dwn
pushd images
bash ./down.sh
popd
python ./convert_maimages.py --conv
