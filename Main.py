import streamlit as st
import cv2
from mtcnn import MTCNN
import numpy as np


def detect_faces(image):
    detector = MTCNN()
    result = detector.detect_faces(image)
    for face in result:
        x, y, width, height = face['box']
        cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)
    return image


def detect_faces_video(video_file):
    detector = MTCNN()
    cap = cv2.VideoCapture(video_file)
    while cap.isOpened():
        # Lê um frame do vídeo
        ret, frame = cap.read()
        if not ret:
            break

            # Detecta as faces no frame
        result = detector.detect_faces(frame)

        # Desenha um retângulo em volta de cada face detectada
        for face in result:
            x, y, width, height = face['box']
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # Exibe o frame processado
        cv2.imshow('Frame', frame)

        # Espera por um evento de teclado
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    uploaded_file = st.sidebar.file_uploader("Carregue uma imagem", type=["jpg", "jpeg", "png"])
    video_file = st.file_uploader('Selecione um vídeo', type=['mp4', 'avi'])
    if uploaded_file is not None:
        # decodificar uma imagem codificada em um formato específico em uma imagem OpenCV
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        image = detect_faces(image)
        st.image(image, channels="BGR")
    elif video_file is not None:
        detect_faces_video(video_file)


if __name__ == "__main__":
    main()
