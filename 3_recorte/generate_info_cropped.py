import cv2
import os

path_to_analize = "rawdata_cropped/"

info_file_to_crop = "info_croppeds.txt"

for file in os.listdir(path_to_analize):
  img = cv2.imread(path_to_analize + file)
  h, w = img.shape[0:2]
  line = "{}{} 1 0 0 {} {}\n".format(path_to_analize, file, w, h)
  with open(info_file_to_crop, "a") as f:
    f.write(line)