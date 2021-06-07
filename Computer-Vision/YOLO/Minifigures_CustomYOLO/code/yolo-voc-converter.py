# Script to convert yolo annotations to voc format
import os
import xml.etree.cElementTree as ET
from PIL import Image
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,
                help="Source path for .txt files to be converted to .xml")
ap.add_argument("-d", "--destination", required=True,
                help="Destination path for converted files.")

args = vars(ap.parse_args())


PATH = args["source"]

CLASS_MAPPING = {
    '0': 'Legogubbe'
    # Add your remaining classes here.
}


def create_root(file_prefix, width, height):
    root = ET.Element("annotations")
    ET.SubElement(root, "filename").text = "{}.JPEG".format(file_prefix)
    ET.SubElement(root, "folder").text = "images"
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)

    tree.write("{}/{}.xml".format(args["destination"], file_prefix))


def read_file(file_path):
    file_prefix = file_path.split(".txt")[0]
    image_file_name = "{}.JPEG".format(file_prefix)
    img = Image.open("{}/{}".format(PATH, image_file_name))

    print(img)

    w, h = img.size
    prueba = "{}/{}".format(PATH, file_path)
    print(prueba)
    with open(prueba) as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(CLASS_MAPPING.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(center_x - (bbox_width / 2))
            voc.append(center_y - (bbox_height / 2))
            voc.append(center_x + (bbox_width / 2))
            voc.append(center_y + (bbox_height / 2))
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels)
    print("Processing complete for file: {}".format(file_path))


def start():
    if not os.path.exists(args["destination"]):
        os.makedirs(args["destination"])
    for filename in os.listdir(args["source"]):
        if filename.endswith('txt'):
            try:
                PathFileName = "{}/{}".format(PATH, filename)
                if os.stat(PathFileName).st_size > 0:
                    print("Sí")
                    read_file(filename)
            except Exception as e:
                print("No:", e)

        else:
            print("Skipping file: {}".format(filename))


if __name__ == "__main__":
    start()

# Basecode from https://gist.github.com/goodhamgupta/7ca514458d24af980669b8b1c8bcdafd
