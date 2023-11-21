from glob import glob
from random import shuffle, seed
import shutil
import os

def move_img_dataset(input_path, dest_path, sub_ds, split, seed_sample, max_img=0):
  annot = glob(input_path+'/labels/*.xml')

  seed(seed_sample)
  shuffle(annot)

  if max_img!=0:
    annot = annot[:max_img]

  print(sub_ds,"-> len annot:", len(annot))

  data_size = int((split)*len(annot))
  print(sub_ds, "-> len data: ", data_size)
  for src_txt in annot[:data_size]:
      src_img = src_txt.replace('/labels/','/images/')
      src_img = src_img.replace('.xml','.jpg')
      src_img = glob(src_img)[0]
      if not os.path.isfile(src_img):
        print("WARNING: No existe el archivo", src_img, ". No se mueve el txt.")
        continue
      shutil.copy(src_img, dest_path+'/images/100k/'+sub_ds+'/')
      shutil.copy(src_txt, dest_path+'/xml/'+sub_ds+'/')


split = 1
seed_sample = 123456

input_path = 'dataset-cvat'
dest_path = "bdd100k/bdd100k"

max_img = 1481
sub_ds = 'train'
move_img_dataset(input_path, dest_path, sub_ds, split, seed_sample, max_img)

max_img = 370
sub_ds = 'val'
move_img_dataset(input_path, dest_path, sub_ds, split, seed_sample, max_img)