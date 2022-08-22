import cv2

path_to_save = "rawdata_cropped/"

info_file_to_crop = "info_merged.txt"

with open(info_file_to_crop, "r") as f:
  for line in f.readlines():
    array = line.split()
    qtd_face = int(array[1])
    for i in range(0, qtd_face):
      file = array[0]
      current = i * 4 + 2
      y0 = int(array[current])
      x0 = int(array[current + 1])
      width = int(array[current + 2])
      height = int(array[current + 3])
      xf = x0 + height
      yf = y0 + width
      print("file= {} | x0={} | y0={} | width={} | height={}".format(file, x0, y0, width, height))
      print("xf={} ; yf={}".format(xf, yf))

      try:
        img = cv2.imread(file)
      except Exception as e:
        print("A imagem {} não está na pasta".format(file))
        continue

      cropped_image = img[x0:xf, y0:yf] 
      if(i != 0):
        file = file.split(".")[0] + "_{}.bmp".format(i)
        print(file)
      file_save = path_to_save + file.split("/")[-1]
      print(file_save)
      
      cv2.imwrite(file_save, cropped_image)
