import streamlit as st
import cv2
from mtcnn import MTCNN
import numpy as np


def detect_faces(image):
    detector = MTCNN()
    result = detector.detect_faces(image)
    for face in result:
        x, y, width, height = face['box']
        cv2.rectangle(image, (x, y), (x+width, y+height), (0, 0, 255), 2)
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
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        yield frame


def main():
    st.title("DETECTOR DE FACES")
    # Carrega o vídeo
    video_choice = {'': '',
                    'video1': 'https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/fb1e4a18-cbbd-4bfd-8303-940714912c10',
                    'video2': 'https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/1b662c17-579d-4326-beb2-fb30d6d3034f',
                    'video3': 'https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/924cec28-e115-4c13-8d7e-c4d48dc47ac5',
                    'video4': 'https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/116ef041-a81a-4a5a-86d8-106c67e86dd6'
                    }
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


if __name__ == "__main__":
    main()
