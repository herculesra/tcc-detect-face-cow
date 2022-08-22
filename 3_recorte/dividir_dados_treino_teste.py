import os
import numpy as np

file_name = "info.txt"
file_train_name = "info_train.txt"
file_test_name = "info_test.txt"

array_lines = []

with open(file_name, 'r') as f:
    for line in f.readlines():
      array_lines.append(str(line))


total_linhas = len(array_lines)
# obtendo 80% do valor total
treino_80 = round((total_linhas * 80) / 100)
# obtendo 20% para teste
teste_20 = total_linhas - treino_80

# Obtendo aleatoriamente 80% das linhas do arquivo, com valores nao repetidos
treino = np.random.choice(array_lines, size=treino_80, replace=False)
# Filtrando o restando para o teste
teste = [x for x in array_lines if x not in treino]

print("linhas totais: ", total_linhas)
print("Quantidade de linhas para treino: ", len(treino))
print("Quantidade de linhas para teste: ", len(teste))

with open(file_train_name, 'w') as f:
  for linha in treino:
    f.write(linha)

with open(file_test_name, 'w') as f:
  for linha in teste:
    f.write(linha)


