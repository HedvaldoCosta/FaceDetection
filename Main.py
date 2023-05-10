import cv2
from mtcnn import MTCNN
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import streamlit as st


uploaded_file_img = st.sidebar.file_uploader("Selecione uma imagem", type="jpg")
uploaded_file_video = st.sidebar.file_uploader("Selecione um vídeo", type=["mp4"])

if uploaded_file_img is not None:
    st.image(uploaded_file_img)

if uploaded_file_video is not None:
    # Usado para capturar vídeo de uma fonte de entrada, como uma câmera de vídeo ou um arquivo de vídeo.
    cap = cv2.VideoCapture(str(uploaded_file_video.name))
    # Cria um objeto de detecção de faces, que pode ser usado para detectar faces em imagens.
    detector = MTCNN()

    while True:
        # Ler cada quadro da câmera/vídeo
        ret, frame = cap.read()
        # Função para detectar as faces na imagem
        output = detector.detect_faces(frame)

        for single_output in output:
            # Extrai as informações de caixa delimitadora (box) do dicionário single_output e as atribui às variáveis x, y, width e height.
            x, y, width, height = single_output['box']
            # Desenha um retângulo ao redor da face detectada na imagem
            cv2.rectangle(frame, pt1=(x, y), pt2=(x + width, y + height), color=(255, 0, 0), thickness=3)
        st.video(frame)

