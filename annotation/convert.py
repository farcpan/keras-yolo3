import cv2
import glob
import json

# tag definition on VoTT
tags = ["green", "red", "unknown", "car-green", "car-red", "car-yellow", "car-unknown"]

# path for VoTT export json file
path_jsons = "../annotation/*.json"

# json files
json_list = glob.glob(path_jsons)

# input images directory
image_in_dir = "../traffic-lights_20200806"

# output images directory
image_out_dir = "./images"


for i, json_file in enumerate(json_list):
    with open(json_file) as f:
        value = json.load(f)

        asset = value["asset"]
        regions = value["regions"]

        name = asset["name"]
        image = cv2.imread("{}/{}".format(image_in_dir, name))
        image = cv2.resize(image, (image.shape[1]//2, image.shape[0]//2))
        cv2.imwrite("{}/{}".format(image_out_dir, name), image)

        boundingBoxStr = "training/{} ".format(name)
        for region in regions:
            tag = region["tags"][0]
            tag_index = tags.index(tag)
            left = region["boundingBox"]["left"]
            top = region["boundingBox"]["top"]
            right = left + region["boundingBox"]["width"]
            bottom = top + region["boundingBox"]["height"]
            boundingBoxStr += "{},{},{},{},{} ".format(int(left * 0.5), int(top * 0.5), int(right * 0.5), int(bottom * 0.5), tag_index)

        print(boundingBoxStr)
