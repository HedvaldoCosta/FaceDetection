import cv2
import streamlit as st


def process_video(video_file):
    # Carrega o vídeo
    video_capture = cv2.VideoCapture(video_file.name)

    # Define o modelo de detecção de rostos
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Processa cada quadro do vídeo
    while True:
        # Lê um quadro do vídeo
        ret, frame = video_capture.read()

        # Verifica se a leitura do quadro foi bem sucedida
        if not ret:
            break

        # Converte o quadro para escala de cinza para facilitar a detecção de rostos
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detecta os rostos no quadro
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Desenha um retângulo em volta de cada rosto detectado
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Mostra o quadro processado na janela de saída
        cv2.imshow('Video', frame)

        # Verifica se o usuário pressionou a tecla 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera os recursos e fecha as janelas
    video_capture.release()
    cv2.destroyAllWindows()


# Define o título do aplicativo
st.title('Identificação de Rostos em Vídeo')

# Adiciona um seletor de arquivos para permitir que o usuário carregue um vídeo
video_file = st.file_uploader('Selecione um arquivo de vídeo', type=['mp4', 'avi'])

if video_file is not None:
    # Chama a função 'process_video' com o arquivo de vídeo selecionado
    process_video(video_file)

