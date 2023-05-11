import streamlit as st
import cv2
from mtcnn import MTCNN


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
    video_choice = {'video1': 'https://bit.ly/3pB4mmU',
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


if __name__=="__main__":
    main()
