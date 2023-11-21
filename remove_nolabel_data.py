import glob
import os
import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser(
    description='Remove no-labeled data')

parser.add_argument("--img_path", default="bdd100k/bdd100k/images/100k/train", type=str,
                    help='Path to image to validate.')
parser.add_argument("--xml_path", default="bdd100k/bdd100k/xml/train", type=str,
                    help='Path ti XML to validate.')

args = parser.parse_args()

img_path = args.img_path
xml_path = args.xml_path

print(img_path)
print(xml_path)


img_src = glob.glob(img_path+"/*.jpg")
xml_src = glob.glob(xml_path+"/*.xml")

img_name = []

num_img = 0
for img in img_src:
    num_img += 1
    img_basename = os.path.basename(img)
    img_onlyname = os.path.splitext(img_basename)

    img_name.append(img_onlyname[0])
    
print("Amount of images:", num_img)

xml_name = []

num_xml = 0
for xml in xml_src:
    num_xml += 1
    xml_basename = os.path.basename(xml)
    xml_onlyname = os.path.splitext(xml_basename)  
    if ET.parse(xml).findall("object"):
        xml_name.append(xml_onlyname[0])
    
print("Amount of XMLs:", num_xml)

not_in_list = []

for img in img_name:
    if img not in xml_name: not_in_list.append(img)

print("Amount of images without labels:", len(not_in_list))
print("Images without labels:", not_in_list)

# path = "../bdd100k/bdd100k/images/100k/train/" + not_in_list[0] + ".jpg"
# print(path)

# Remove training samples which do not have anotation.
count_img = 0
count_xml = 0
for item in not_in_list:
    path_img = img_path + "/" + item + ".jpg"
    if os.path.exists(path_img):
        os.remove(path_img)
        count_img += 1
    else:
        print("The JPG file does not exist")

    path_xml = xml_path + "/" + item + ".xml"
    if os.path.exists(path_xml):
        os.remove(path_xml)
        count_xml += 1
    else:
        print("The XML file does not exist")

print("Images removed:", count_img)
print("XMLs removed", count_xml)