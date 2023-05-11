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


def detect_faces_video(video):
    detector = MTCNN()
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        result = detector.detect_faces(frame)
        for face in result:
            x, y, w, h = face['box']
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        yield frame


def main():
    st.title("Detector de faces em vídeo com MTCNN")
    # Carrega o vídeo
    video_choice = {'': '',
                    'video1': 'https://bit.ly/3pB4mmU',
                    'video2': 'https://bit.ly/3LZSIZY',
                    'video3': 'https://bit.ly/453LTzA',
                    'video4': 'https://bit.ly/42MTkch'}
    select_video = st.sidebar.selectbox('Selecione um vídeo', video_choice.keys())
    video = cv2.VideoCapture(video_choice[select_video])
    video_generator = detect_faces_video(video)

    # Exibe o vídeo com as faces detectadas em tempo real
    stframe = st.empty()
    while True:
        try:
            frame = next(video_generator)
            stframe.image(frame, channels="RGB")
        except StopIteration:
            break

    uploaded_file = st.sidebar.file_uploader("Carregue uma imagem", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # decodificar uma imagem codificada em um formato específico em uma imagem OpenCV
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        image = detect_faces(image)
        st.image(image, channels="BGR")


if __name__=="__main__":
    main()
