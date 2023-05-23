![face_detection_banner](https://github.com/HedvaldoCosta/ProfileSearch/assets/67663958/2b956da0-ee0e-40c5-980c-6249030bd558)

# RESUMO
Repositório direcionado para a utilização de bibliotecas específicas para a identificação de rostos em formatos de imagem, vídeo e até mesmo podendo ser testado em sua webcam.

# INTRODUÇÃO
A aplicação foi construída visando a liberdade do usuário para fazer seus testes com próprias fotos e vídeos. Pode até ser utilizado para reconhecimento facial de pessoas específicas e monitoramento de ruas por meio de câmeras de segurança (ainda não aplicado dentro deste repositório).

# SOLUÇÃO
Utilizando-se da biblioteca python, [MTCNN](https://pypi.org/project/mtcnn/), é possível aplicar a função de detecção de faces em imagens e vídeos, carregados pela biblioteca [opencv](https://docs.opencv.org/4.x/). A demonstração das imagens/vídeos foram feitos dentro de uma aplicação [streamlit](https://docs.streamlit.io). 

**Código:** https://bit.ly/42TpB1T

![image](https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/f10f1bda-93ee-431c-9700-d09d701bdca9)

Em determinados casos, a inteligência artificial (IA) não consegue identificar o rosto, podendo ser que algo esteja tapando uma parte do rosto ou até mesmo a pessoa esteja de lado.

![image](https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/ed7ca574-afb2-4701-9d0a-bde9010bfb8a)

Cortando o vídeo frame por frame, é necessário aplicar a função de detecção de faces a cada frame para que a função do MTCNN funcione dentro de um vídeo.

![2023-05-23-14-16-03](https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/1b4bef45-bf42-498d-8c77-b39d6fab34bc)

# FERRAMENTAS
pycharm community Edition 2023.1

python 3.9.13

click==8.1.3

mtcnn==0.1.1

numpy==1.23.5

opencv-python==4.7.0.72

streamlit==1.22.0

google colab

# SOBRE O CÓDIGO

````python
# Biblioteca utilizada para a construção da aplicação e colocar o projeto em produção
import streamlit as st
# Criação do retângulo e carregamento das imagens/vídeos/webcam
import cv2
# Detecção de rostos
from mtcnn import MTCNN
# Converter uma sequência de bytes em um array NumPy.
import numpy as np
# Criar um arquivo temporário no sistema de arquivos com um nome único.
import tempfile
````

````python
# Classe criada para a utilização da função de detecção de faces em vídeos e imagens
# carregados pelo opencv
class FaceDetection:
    def __init__(self, file_image='', file_video=''):
        # Instância de um objeto detector de faces 
        self.detector = MTCNN()
        # Instância do recebimento da imagem
        self.image = file_image
        # Instância do recebimento do vídeo
        self.video = file_video
````

````python
    # Função utilizada para aplicar a detecção de faces em imagens
    def detecting_faces_image(self):
        # realizar a detecção de faces na imagem
        result = self.detector.detect_faces(self.image)
        # loop sobre cada elemento (dicionário) presente na lista 'result'
        for faces in result:
            # Os valores das chaves 'box' são extraídos e atribuídos às variáveis x, y,
            # width e height. Essas informações representam as coordenadas e dimensões 
            # da caixa delimitadora (retângulo) ao redor da face detectada.
            x, y, width, height = faces['box']
            # Desenha um retângulo na imagem original 
            cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 0, 255), 2)
        # Retorna a imagem com um retângulo na face
        return self.image
````

````python
    # Função utilizada para aplicar a detecção de faces em vídeos
    def detecting_faces_video(self):
        # Loop a ser mantido enquanto o vídeo estiver aberto
        while self.video.isOpened():
            # Verificando se cada frame de self.video foi lido e armazenado
            # ret é um valor booleano que indica se o quadro foi lido
            ret, frame = self.video.read()
            #  Indica que não foi possível ler o próximo quadro do vídeo.
            if not ret:
                break
            # Detectar faces no quadro de imagem frame.
            result = self.detector.detect_faces(frame)
            # loop sobre cada elemento (dicionário) presente na lista 'result'
            for face in result:
                # Os valores das chaves 'box' são extraídos e atribuídos às variáveis 
                # x, y, width e height. Essas informações representam as coordenadas 
                # e dimensões da caixa delimitadora (retângulo) ao redor da 
                # face detectada.
                x, y, w, h = face['box']
                # Desenha um retângulo na imagem original 
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # converte o quadro de imagem de formato BGR para o formato RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #  função geradora, que pode ser iterada para obter cada quadro 
            #  processado individualmente. 
            yield frame
````

````python
    #Função para detecção de faces em sua webcam
    def detecting_faces_webcam(self):
        # Inicia sua webcam
        cap = cv2.VideoCapture(0)
        # Loop que para quando não for possível ler o próximo frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Detecção de rosto usando MTCNN
            results = self.detector.detect_faces(frame)

            # Desenhar retângulos em torno dos rostos detectados
            for result in results:
                x, y, w, h = result['box']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Mostrar o quadro com os retângulos dos rostos detectados
            cv2.imshow('Webcam', frame)

            # Condição de saída do loop (pressionando a tecla "q")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # Libere os recursos
            cap.release()
            cv2.destroyAllWindows()
````

````python

````
# SUMMARY

# INTRODUCTION

# SOLUTION

# TOOLS

# ABOUT THE CODE
