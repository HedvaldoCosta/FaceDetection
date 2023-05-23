# Bibliotecas necessárias para a execução do código
import streamlit as st
import cv2
from mtcnn import MTCNN
import numpy as np
import tempfile


class FaceDetection:
    def __init__(self, file_image='', file_video=''):
        self.detector = MTCNN()
        self.image = file_image
        self.video = file_video

    def detecting_faces_image(self):
        result = self.detector.detect_faces(self.image)
        for faces in result:
            x, y, width, height = faces['box']
            cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 0, 255), 2)
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

            results = self.detector.detect_faces(frame)

            for result in results:
                x, y, w, h = result['box']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            cv2.imshow('Webcam', frame)

            # Condição de saída do loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # ________________________________PARTE PARA A EXECUÇÃO DE VÍDEOS________________________________
    st.sidebar.title("ESCOLHA UM VÍDEO")
    uploaded_file = st.sidebar.file_uploader("", type=["mp4", "avi"])
    if uploaded_file is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        video_path = temp_file.name
        temp_file.close()
        video = cv2.VideoCapture(video_path)
        face_detection_video = FaceDetection(file_video=video)
        video_generator = face_detection_video.detecting_faces_video()
        stframe = st.empty()
        while True:
            try:
                frame = next(video_generator)
                stframe.image(frame, channels="RGB")
            except StopIteration:
                break
    st.sidebar.info("Sem arquivos? escolha aqui")
    video_choice = {'PARAR': '',
                    'Vídeo 1': 'https://bit.ly/436YGiF',
                    'Vídeo 2': 'https://bit.ly/45bh5wJ',
                    'Vídeo 3': 'https://bit.ly/3Oneg5H',
                    'Vídeo 4': 'https://bit.ly/42POU4R'}
    select_video = st.sidebar.selectbox('', video_choice.keys())
    video = cv2.VideoCapture(video_choice[select_video])
    face_detection_video = FaceDetection(file_video=video)
    video_generator = face_detection_video.detecting_faces_video()
    stframe = st.empty()
    while True:
        try:
            frame = next(video_generator)
            stframe.image(frame, channels="RGB")
        except StopIteration:
            break

    # ________________________________PARTE PARA A EXECUÇÃO DE IMAGENS________________________________
    st.sidebar.title("ESCOLHA UMA IMAGEM")
    upload_image = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])
    if upload_image is not None:
        image = cv2.imdecode(np.fromstring(upload_image.read(), np.uint8), 1)
        face_detection_image = FaceDetection(file_image=image)
        image_generator = face_detection_image.detecting_faces_image()
        st.image(image_generator, channels="BGR")

    # ________________________________PARTE PARA A EXECUÇÃO DA WEBCAM________________________________
    st.sidebar.title("WEBCAM")
    start_webcam_button = st.sidebar.button("INICIAR WEBCAM")
    if start_webcam_button:
        face_detection_webcam = FaceDetection()
        face_detection_webcam.detecting_faces_webcam()
