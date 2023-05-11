import streamlit as st
import cv2
import numpy as np
from mtcnn import MTCNN
import io


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
    uploaded_file = st.file_uploader("Escolha um vídeo", type=["mp4"])
    if uploaded_file is not None:
        video = cv2.VideoCapture('https://vod-progressive.akamaized.net/exp=1683822149~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F4428%2F15%2F397143934%2F1690405210.mp4~hmac=7e9d3739a29c9333e7d4184231f7c06e45094b985cf0589cb62b08d82a51078b/vimeo-prod-skyfire-std-us/01/4428/15/397143934/1690405210.mp4', cv2.CAP_ANY)
        video_generator = detect_faces_video(video)

        # Exibe o vídeo com as faces detectadas em tempo real
        stframe = st.empty()
        while True:
            try:
                frame = next(video_generator)
                stframe.image(frame, channels="RGB")
            except StopIteration:
                break


if __name__=="__main__":
    main()