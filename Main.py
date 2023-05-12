import streamlit as st
import cv2
from mtcnn import MTCNN
import numpy as np


class FaceDetection:
    def __init__(self, file_image=None, file_video=None):
        self.image = file_image
        self.video = file_video
        self.detector = MTCNN()

    def detecting_faces_images(self):
        result_img = self.detector.detect_faces(self.image)
        for faces in result_img:
            x, y, width, height = faces["box"]
            cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 0, 255), 2)
        return self.image

    def detecting_faces_videos(self):
        while self.video.isOpened():
            ret, frame = self.video.read()
            if not ret:
                break
            result_video = self.detector.detect_faces(frame)
            for faces in result_video:
                x, y, width, height = faces["box"]
                cv2.Rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Usado para iterar sobre uma sequência de valores.
            yield frame


if __name__=="__main__":
    st.title("Detector de faces com MTCNN")
    video_choice = {
        '': '',
        'video1': 'https://bit.ly/3pB4mmU',
        'video2': 'https://bit.ly/3LZSIZY',
        'video3': 'https://bit.ly/453LTzA',
        'video4': 'https://bit.ly/42MTkch'
    }
    select_video = st.sidebar.selectbox('Selecione um vídeo', video_choice.keys())
    video = cv2.VideoCapture(video_choice[select_video])
    face_detection_video = FaceDetection(file_video=video)
    video_generator = face_detection_video.detecting_faces_videos()

    stframe = st.empty()
    while True:
        try:
            frame = next(video_generator)
            stframe.image(frame, channels="RGB")
        except StopIteration:
            break

    uploaded_file_img = st.sidebar.file_uploader("Carregue uma imagem", type=["jpg", "jpeg", "png"])
    if uploaded_file_img is not None:
        image = cv2.imdecode(np.fromstring(uploaded_file_img.read(), np.uint8), 1)
        face_detection_img = FaceDetection(file_image=image)
        image = face_detection_img.detecting_faces_images()
        st.image(image, channels="BGR")
