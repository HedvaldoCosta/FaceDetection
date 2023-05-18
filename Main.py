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
    # Carrega o vídeo
    video_choice = {'': '',
                    'video1': 'https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/fb1e4a18-cbbd-4bfd-8303-940714912c10',
                    'video2': 'https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/1b662c17-579d-4326-beb2-fb30d6d3034f',
                    'video3': 'https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/924cec28-e115-4c13-8d7e-c4d48dc47ac5',
                    'video4': 'https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/116ef041-a81a-4a5a-86d8-106c67e86dd6'
                    }
    st.sidebar.title("SELECIONE UM VÍDEO")
    select_video = st.sidebar.selectbox('', video_choice.keys())

    button_video = st.sidebar.button("PARAR O VÍDEO")
    if button_video:
        select_video = ''
    if select_video != '':
        st.title("BUSCANDO ROSTOS")
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
    st.sidebar.title("SELECIONE UMA IMAGEM")
    uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.title("ROSTO IDENTIFICADO")
        # decodificar uma imagem codificada em um formato específico em uma imagem OpenCV
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        image = detect_faces(image)
        st.image(image, channels="BGR")
    st.sidebar.title("WEBCAM")
    webcam = st.sidebar.button("Iniciar WEBCAM")
    if webcam:
        st.sidebar.text("Pressione a tecla q para parar a webcam.")
        detector = MTCNN()
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Detecção de rosto usando MTCNN
            results = detector.detect_faces(frame)

            # Desenhar retângulos em torno dos rostos detectados
            for result in results:
                x, y, w, h = result['box']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Mostrar o quadro com os retângulos dos rostos detectados
            cv2.imshow('Webcam', frame)

            # Condição de saída do loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Libere os recursos
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
