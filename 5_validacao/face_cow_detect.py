import cv2 
from matplotlib import pyplot as plt

path_img = "para_teste_nelore_frontal/2001.bmp"
path_cascade_xml = "./haarcascade/haarcascade_frontface_cownelore_30_24x36.xml" # MELHOR CLASSIFICADOR ATÉ O MOMENTO!

face_cascade = cv2.CascadeClassifier(path_cascade_xml)

img = cv2.imread(path_img)

# Convertendo para escala cinza usada na predição.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in faces:
  cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

p,l,m=cv2.split(img)
img=cv2.merge([m,l,p])

plt.imshow(img)
plt.show()

print("Quantidade de animais detectados na imagem: {}".format(len(faces)))
