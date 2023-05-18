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




