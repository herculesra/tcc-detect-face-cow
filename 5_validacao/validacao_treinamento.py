import cv2 
from matplotlib import pyplot as plt

file_test = "info.txt"
# path_cascade_xml = "./haarcascade/testado/haarcascade_frontcow_30_24_36.xml" # 66% com neightbors em 3
path_cascade_xml = "./haarcascade/haarcascade_frontface_cownelore_30_24x36.xml" #  73.65% de acuracia e 95.27% de precisao total sem nenhuma movimentacao

def extract_lines_and_faces():
  classes_faces = {}
  path_images = []
  with open(file_test, 'r') as f:
    for linha in f.readlines():
      line_splited = linha.split()
      path = str(line_splited[0])
      path_images.append(path)
      qtd_faces = line_splited[1]
      if qtd_faces in classes_faces:
        classes_faces[qtd_faces][0] += 1
        classes_faces[qtd_faces][1].append(path)
      else:
        classes_faces[qtd_faces] = [1, [path]]

  return (path_images, classes_faces)

def show_image(faces, img):
  print("quantidade de faces encontrada(s): {}".format(len(faces)))
  for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

  p,l,m=cv2.split(img)
  img=cv2.merge([m,l,p])

  # Visualizando imagem
  plt.imshow(img)
  plt.show()


# obtendo o classificador
face_cascade = cv2.CascadeClassifier(path_cascade_xml)

path_images, classes_faces = extract_lines_and_faces()
classes_faces_detected = {}

for path in path_images:
  # Lendo a imagem e armazenando em um array.
  img = cv2.imread(path)

  # pode influenciar na detecção
  # img = cv2.resize(img, (300, 300))

  # Convertendo para escala cinza usada na predição.
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  # gray = cv2.equalizeHist(gray) # pode influenciar na detecção
 
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)

  qtd_faces = str(len(faces))

  if qtd_faces in classes_faces_detected:
    classes_faces_detected[qtd_faces][0] += 1
    classes_faces_detected[qtd_faces][1].append(path)
  else:
    classes_faces_detected[qtd_faces] = [1, [path]]

  # Mostrar a detecção em tempo de execução
  show_image(faces, img)

BREAK_LINES = "\n========================================//========================================\n"

print(BREAK_LINES)

for key in classes_faces:
  total_faces_classe = classes_faces[key][0]
  print("Total para a classe {} é de {}".format(key, total_faces_classe))

for key in classes_faces_detected:
  total_faces_classe = classes_faces_detected[key][0]
  print("Total detectado para a classe {} é de {}".format(key, total_faces_classe))

print(BREAK_LINES)


qtt_total_imgs = precisao_total_final =  len(path_images)
total_real = 0

for key in classes_faces_detected.keys():
  if key not in classes_faces.keys(): # se nao tiver a classe, então desconta seus valores da precisao
    print("A classe {} não pertence à classe de teste".format(key))
    precisao_total_final -= classes_faces_detected[key][0]
  else:
    qtd_face_total = classes_faces[key][0] # quantidade total para esta classe
    lista_nomes_imagens = classes_faces[key][1] # imagens da classe de teste
    qtd_face_dtt = classes_faces_detected[key][0] # quantidade de faces detectadas para a classe
    lista_nomes_imagens_dtt = classes_faces_detected[key][1] # imagens da classe detectada
    qtd_face_real = 0
    for nome_img in lista_nomes_imagens:
      if(nome_img not in lista_nomes_imagens_dtt):
        qtd_face_dtt -= 1
      if(nome_img in lista_nomes_imagens_dtt):
        qtd_face_real += 1
    precisao_parcial = qtd_face_dtt / qtd_face_total
    precisao_parcial_real = qtd_face_real / qtd_face_total
    total_real += qtd_face_real

print(BREAK_LINES)

print("Classificador utilizado: {}".format(path_cascade_xml.split("/")[-1]))

print("Quantidade total de imagens analizadas: {}".format(qtt_total_imgs))  
print("Quantidade total de imagens com faces detectadas: {}".format(precisao_total_final))
print("Acerto total de faces em imagens: {}".format(total_real))

print("Precisão Total = {:2.2%} (Certeza de detecção para ao menos uma face)".format(precisao_total_final / qtt_total_imgs))
print("Acurácia = {:2.2%} (Certeza da quantidade de faces encontradas seja a esperada)".format(total_real / qtt_total_imgs))
