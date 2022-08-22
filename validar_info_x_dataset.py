import os

# 1 - ler o arquivo de info e criar uma string giante com todos os nomes separados por pipe

arquivo_info = "./4_treinamento/haar_training/training/positive/info.txt"

nomes_imagens = ""

with open(arquivo_info, 'r') as file:
  for line in file.readlines():
    array = line.split()
    nome_imagem = array[0]
    nomes_imagens += nome_imagem + " | "

# 2 - para cada imagem lida, verificar se o nome dela está no arquivo info, se não, mostrar qual imagem nao está

path_images = "./4_treinamento/haar_training/training/positive/rawdata/"
pasta_imagens = ""
for img_file in os.listdir(path_images):
  pasta_imagens += img_file + " | "
  if(img_file not in nomes_imagens):
    print("A imagem não está no arquivo info: ", img_file)

# INVERSO
# 1 - ler o arquivo Info e verificar se há imagens faltantes na pasta

## aproveitando o código acima

nomes_imagens = nomes_imagens.replace("rawdata/", "")

# passa a ser um array

nomes_imagens = nomes_imagens.split(" | ")

# verificando o último conteúdo

print("primeiro: ", nomes_imagens[0])
print("Último conteudo: ", nomes_imagens[-1])

for nome_img_arquivo in nomes_imagens:
  if(nome_img_arquivo not in pasta_imagens):
    print("A imagem não está na pasta: ", nome_img_arquivo)



