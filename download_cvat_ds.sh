#!/bin/bash

rm -r bdd100k
rm -r dataset-cvat

function download_task {
  echo "##################################"
  echo Download task $1

  mkdir -p dataset-cvat/task-$1
  cd dataset-cvat/task-$1

  # Download images
  cvat-cli --auth sperez:NuevaEra.2023 --server-host 20.197.227.116 --server-port 8080 --debug export $1 task-$1.zip
  unzip -q task-$1.zip

  # Download annotations
  cvat-cli --auth sperez:NuevaEra.2023 --server-host 20.197.227.116 --server-port 8080 --debug dump --format "PASCAL VOC 1.1" $1 task-$1-dump.zip
  unzip -q task-$1-dump.zip

  cd ../../
}

function move_task_img {
  echo "##################################"
  echo move task img $1

  DIR_TASK="dataset-cvat/task-$1"

  echo `ls $DIR_TASK/data | wc -l`
  echo `ls $DIR_TASK/Annotations | wc -l`

  cp $DIR_TASK/data/* dataset-cvat/images
  cp $DIR_TASK/Annotations/* dataset-cvat/labels
}

download_task 18
download_task 19
download_task 20
download_task 23

mkdir -p dataset-cvat/images
mkdir -p dataset-cvat/labels

move_task_img 18
move_task_img 19
move_task_img 20
move_task_img 23

echo "##################################"
echo CONVERT PNG TO JPG
mogrify -format jpg dataset-cvat/images/*.png
rm dataset-cvat/images/*.png

echo "##################################"
echo TOTAL IMAGES/LABELS IN CVAT DATASET
ls dataset-cvat/images/*.jpg | wc -l
ls dataset-cvat/labels/*.xml | wc -l

echo "##################################"
echo CREATE BDD100K DIR STRUCTURE
mkdir -p bdd100k/bdd100k/images/100k/train
mkdir -p bdd100k/bdd100k/images/100k/val
mkdir -p bdd100k/bdd100k/xml/train
mkdir -p bdd100k/bdd100k/xml/val

echo "##################################"
echo POPULATE BDD100K DIR STRUCTURE
python preprocess_cvat_ds.py

echo "##################################"
echo REMOVE NOLABELED DATA
python remove_nolabel_data.py --img_path bdd100k/bdd100k/images/100k/train --xml_path bdd100k/bdd100k/xml/train
python remove_nolabel_data.py --img_path bdd100k/bdd100k/images/100k/val --xml_path bdd100k/bdd100k/xml/val

cp -r bdd_files bdd100k/
cp -r models bdd100k/

ls -1 bdd100k/bdd100k/images/100k/train  | sed -e 's/\.jpg$//' > bdd100k/bdd_files/trainval.txt
ls -1 bdd100k/bdd100k/images/100k/val  | sed -e 's/\.jpg$//' >> bdd100k/bdd_files/trainval.txt

echo FINISHED
echo "##################################"
