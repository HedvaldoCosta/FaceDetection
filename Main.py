# Bibliotecas necessárias para a execução do código
import streamlit as st
import cv2
from mtcnn import MTCNN
import numpy as np


class FaceDetection:
    def __init__(self, file_image='', file_video=''):
        self.detector = MTCNN()
        self.image = file_image
        self.video = file_video

    def detecting_faces_image(self):
        result = self.detector.detect_faces(self.image)
        for faces in result:
            x, y, width, height = faces['box']
            cv2.rectangle(self.image, (x, y), (x+width, y+height), (0, 0, 255), 2)
        return self.image

    def detecting_faces_video(self):
        while self.video.isOpened():
            ret, frame = self.video.read()
            if not ret:
                break
            result = self.detector.detect_faces(frame)
            for face in result:
                x, y, w, h = face['box']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            yield frame

    def detecting_faces_webcam(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Detecção de rosto usando MTCNN
            results = self.detector.detect_faces(frame)

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


if __name__ == '__main__':
    video_choice = {'Vídeo 1': 'https://bit.ly/436YGiF',
                    'Vídeo 2': 'https://bit.ly/45bh5wJ',
                    'Vídeo 3': 'https://bit.ly/3Oneg5H',
                    'Vídeo 4': 'https://bit.ly/42POU4R'}
    st.sidebar.title("ESCOLHA UM VÍDEO")
    select_video = st.sidebar.selectbox('', video_choice.keys())
    start_video_button = st.sidebar.button("INICIAR")
    if start_video_button:
        video = cv2.VideoCapture(video_choice[select_video])
        face_detection_video = FaceDetection(file_video=video)
        video_generator = face_detection_video.detecting_faces_video()
        # Exibe o vídeo com as faces detectadas em tempo real
        stframe = st.empty()
        while True:
            try:
                frame = next(video_generator)
                stframe.image(frame, channels="RGB")
            except StopIteration:
                break





