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


def main():
    uploaded_file = st.sidebar.file_uploader("Carregue uma imagem", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # decodificar uma imagem codificada em um formato específico em uma imagem OpenCV
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        image = detect_faces(image)
        st.image(image, channels="BGR")


if __name__ == "__main__":
    main()