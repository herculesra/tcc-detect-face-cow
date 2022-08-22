import cv2
import os

path_images = "./data/"
path_to_save = "./data_reconfigurada/"
count_image = 2128

IMG_MT_GRANDE = 700 * 700
IMG_GRANDE = 500 * 500
IMG_MEDIA = 400 * 400

for img_file in os.listdir(path_images):
  full_path = path_images + img_file
  img = cv2.imread(full_path)
  shape = img.shape
  height, width, channel = shape

  tamanho_imagem = height * width

  if(tamanho_imagem >= IMG_MT_GRANDE):
    resized_image = cv2.resize(img, (700, 700))
  elif(tamanho_imagem >= IMG_GRANDE):
    resized_image = cv2.resize(img, (500, 500))
  elif(tamanho_imagem >= IMG_MEDIA):
    resized_image = cv2.resize(img, (400, 400))
  else:
    resized_image = img

  cv2.imwrite("{}{}.bmp".format(path_to_save, count_image), resized_image)
  count_image += 1