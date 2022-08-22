import cv2 
import os
import logging as log

log.basicConfig(handlers=[log.FileHandler(filename="./log_best_classifier.log", 
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=log.INFO)

path_classifiers = "haarcascade/testado/"
file_test = "info.txt"

best_classifier_accuracy = {}
best_classifier_real_accuracy = {}

acuracia_total, best_acc, best_acc_real = ["", 0], ["", 0], ["", 0]
BREAK_LINES = "\n========================================//========================================\n"

def zero_div(x, y):
  try:
    return x / y
  except ZeroDivisionError:
    return 0

def log_init():
  log.info("====================== INICIO ======================\n")

def log_final():
  log.info("\n====================== FIM ======================")

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

log_init()

path_images, classes_faces = extract_lines_and_faces()

for classifier_name in os.listdir(path_classifiers):
  
  string_to_log = "\n============== CLASSIFICADOR: {} ===================\n".format(classifier_name)
  print(classifier_name)

  # obtendo o classificador
  face_cascade = cv2.CascadeClassifier(path_classifiers + classifier_name)

  classes_faces_detected = {}

  for path in path_images:
    # Lendo a imagem e armazenando em um array.
    img = cv2.imread(path)

    # img = cv2.resize(img, (300, 300))

    # Convertendo para escala cinza usada na predição.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    qtd_faces = str(len(faces))

    if qtd_faces in classes_faces_detected:
      classes_faces_detected[qtd_faces][0] += 1
      classes_faces_detected[qtd_faces][1].append(path)
    else:
      classes_faces_detected[qtd_faces] = [1, [path]]


  for key in classes_faces:
    total_faces_classe = classes_faces[key][0]
    string_to_log += "\nTotal para a classe {} é de {}".format(key, total_faces_classe)

  for key in classes_faces_detected:
    total_faces_classe = classes_faces_detected[key][0]
    string_to_log += "\nTotal detectado para a classe {} é de {}".format(key, total_faces_classe)

  string_to_log += BREAK_LINES
  """
    A precisão total se dá pelo num_acerto_total / num_total_imagens
  """
  qtt_total_imgs = precisao_total_final =  len(path_images)
  total_real = 0

  for key in classes_faces_detected.keys():
    if key not in classes_faces.keys(): # se nao tiver a classe, então desconta seus valores da precisao
      string_to_log += "\nA classe {} não existe nas classes de teste".format(key)
  
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

  string_to_log += BREAK_LINES

  string_to_log += "\nQuantidade total de imagens analizadas: {}".format(qtt_total_imgs)
  string_to_log += "\nQuantidade total de imagens com faces detectadas: {}".format(precisao_total_final)
  string_to_log += "\nAcerto total de faces em imagens: {}".format(total_real)

  precisao_total = zero_div(precisao_total_final, qtt_total_imgs)
  acuracia = zero_div(total_real, qtt_total_imgs)

  string_to_log += "\nPrecisão Total = {:2.2%} (Certeza de detecção para ao menos uma face)".format(precisao_total)
  string_to_log += "\nAcurácia = {:2.2%} (Certeza da quantidade de faces encontradas seja a esperada)".format(acuracia)
  
  acc_total = (precisao_total + acuracia) / 2
  if(acuracia_total[1] < acc_total):
    acuracia_total[0], acuracia_total[1] = classifier_name, acc_total
  
  if(best_acc[1] < precisao_total):
    best_acc[0], best_acc[1] = classifier_name, precisao_total
  
  if(best_acc_real[1] < acuracia):
    best_acc_real[0], best_acc_real[1] = classifier_name, acuracia

  print(string_to_log)
  log.info(string_to_log)

best_faces = "A melhor precisao total de faces foi do classificador: [{}] com um total de {:2.2%}".format(best_acc[0], best_acc[1])
best_real = "A melhor acurácia real foi do classificador: [{}] com um total de {:2.2%}".format(best_acc_real[0], best_acc_real[1])

line =  "{} {} \n {} {}".format(BREAK_LINES, best_faces, best_real, BREAK_LINES)
print(line)
log.info(line)
log_final()
