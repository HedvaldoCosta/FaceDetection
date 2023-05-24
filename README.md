![face_detection_banner](https://github.com/HedvaldoCosta/ProfileSearch/assets/67663958/2b956da0-ee0e-40c5-980c-6249030bd558)

# RESUMO
Repositório direcionado para a utilização de bibliotecas específicas para a identificação de rostos em formatos de imagem, vídeo e até mesmo podendo ser testado em sua webcam.

# INTRODUÇÃO
A aplicação foi construída visando a liberdade do usuário para fazer seus testes com próprias fotos e vídeos. Pode até ser utilizado para reconhecimento facial de pessoas específicas e monitoramento de ruas por meio de câmeras de segurança (ainda não aplicado dentro deste repositório).

# SOLUÇÃO
Utilizando-se da biblioteca python, [MTCNN](https://pypi.org/project/mtcnn/), é possível aplicar a função de detecção de faces em imagens e vídeos, carregados pela biblioteca [opencv](https://docs.opencv.org/4.x/). A demonstração das imagens/vídeos foram feitos dentro de uma aplicação [streamlit](https://docs.streamlit.io). 

**Código:** https://bit.ly/42TpB1T

![image](https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/f10f1bda-93ee-431c-9700-d09d701bdca9)

Em determinados casos, a inteligência artificial (IA) não consegue identificar o rosto, podendo ser que algo esteja tapando uma parte do rosto ou até mesmo a pessoa esteja de lado.

![image](https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/ed7ca574-afb2-4701-9d0a-bde9010bfb8a)

Cortando o vídeo frame por frame, é necessário aplicar a função de detecção de faces a cada frame para que a função do MTCNN funcione dentro de um vídeo.

![2023-05-23-14-16-03](https://github.com/HedvaldoCosta/FaceDetection/assets/67663958/1b4bef45-bf42-498d-8c77-b39d6fab34bc)

# FERRAMENTAS
pycharm community Edition 2023.1

python 3.9.13

click==8.1.3

mtcnn==0.1.1

numpy==1.23.5

opencv-python==4.7.0.72

streamlit==1.22.0

google colab

# SOBRE O CÓDIGO

````python
# Biblioteca utilizada para a construção da aplicação e colocar o projeto em produção
import streamlit as st
# Criação do retângulo e carregamento das imagens/vídeos/webcam
import cv2
# Detecção de rostos
from mtcnn import MTCNN
# Converter uma sequência de bytes em um array NumPy.
import numpy as np
# Criar um arquivo temporário no sistema de arquivos com um nome único.
import tempfile
````

````python
# Classe criada para a utilização da função de detecção de faces em vídeos e imagens
# carregados pelo opencv
class FaceDetection:
    def __init__(self, file_image='', file_video=''):
        # Instância de um objeto detector de faces 
        self.detector = MTCNN()
        # Instância do recebimento da imagem
        self.image = file_image
        # Instância do recebimento do vídeo
        self.video = file_video
````

````python
    # Função utilizada para aplicar a detecção de faces em imagens
    def detecting_faces_image(self):
        # realizar a detecção de faces na imagem
        result = self.detector.detect_faces(self.image)
        # loop sobre cada elemento (dicionário) presente na lista 'result'
        for faces in result:
            # Os valores das chaves 'box' são extraídos e atribuídos às variáveis x, y,
            # width e height. Essas informações representam as coordenadas e dimensões 
            # da caixa delimitadora (retângulo) ao redor da face detectada.
            x, y, width, height = faces['box']
            # Desenha um retângulo na imagem original 
            cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 0, 255), 2)
        # Retorna a imagem com um retângulo na face
        return self.image
````

````python
    # Função utilizada para aplicar a detecção de faces em vídeos
    def detecting_faces_video(self):
        # Loop a ser mantido enquanto o vídeo estiver aberto
        while self.video.isOpened():
            # Verificando se cada frame de self.video foi lido e armazenado
            # ret é um valor booleano que indica se o quadro foi lido
            ret, frame = self.video.read()
            #  Indica que não foi possível ler o próximo quadro do vídeo.
            if not ret:
                break
            # Detectar faces no quadro de imagem frame.
            result = self.detector.detect_faces(frame)
            # loop sobre cada elemento (dicionário) presente na lista 'result'
            for face in result:
                # Os valores das chaves 'box' são extraídos e atribuídos às variáveis 
                # x, y, width e height. Essas informações representam as coordenadas 
                # e dimensões da caixa delimitadora (retângulo) ao redor da 
                # face detectada.
                x, y, w, h = face['box']
                # Desenha um retângulo na imagem original 
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # converte o quadro de imagem de formato BGR para o formato RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #  função geradora, que pode ser iterada para obter cada quadro 
            #  processado individualmente. 
            yield frame
````

````python
    #Função para detecção de faces em sua webcam
    def detecting_faces_webcam(self):
        # Inicia sua webcam
        cap = cv2.VideoCapture(0)
        # Loop que para quando não for possível ler o próximo frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Detecção de rosto usando MTCNN
            results = self.detector.detect_faces(frame)

            # Desenhar retângulos em torno dos rostos detectados
            for result in results:
                x, y, w, h = result['box']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Mostrar o quadro com os retângulos dos rostos detectados
            cv2.imshow('Webcam', frame)

            # Condição de saída do loop (pressionando a tecla "q")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # Libere os recursos
            cap.release()
            cv2.destroyAllWindows()
````

````python
if __name__ == '__main__':
    # Criação de um título para vídeos na barra lateral
    st.sidebar.title("ESCOLHA UM VÍDEO")
    # Função que dá permissão ao usuário para carregar seus próprios vídeos
    uploaded_file = st.sidebar.file_uploader("", type=["mp4", "avi"])
    if uploaded_file is not None:
        # Cria um arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        # Escreve a string como Bytes no arquivo temporário
        temp_file.write(uploaded_file.read())
        # Recebe o nome do arquivo temporário e o fecha
        video_path = temp_file.name
        temp_file.close()
        # Capturar fluxos de vídeo de arquivos de vídeo
        video = cv2.VideoCapture(video_path)
        # Retonar a classe FaceDetection recebendo o parâmetro "video"
        face_detection_video = FaceDetection(file_video=video)
        # Inicia a função para detecção em vídeos
        video_generator = face_detection_video.detecting_faces_video()
        # Criar e atualizar elementos de exibição interativos em aplicativos 
        stframe = st.empty()
        while True:
            try:
                # Obter o próximo quadro do vídeo
                frame = next(video_generator)
                # Exibir o quadro na interface
                stframe.image(frame, channels="RGB")
            # Indicar o final de uma iteração
            except StopIteration:
                break
    # Possibilidade de testar vídeos já carregados dentro da aplicação
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
````

````python
    # Criação de um título para imagens na barra lateral
    st.sidebar.title("ESCOLHA UMA IMAGEM")
    # Função para carregar imagens em seu próprio dispositivo
    upload_image = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])
    if upload_image is not None:
        # Decodificar e ler a imagem representada pelo array NumPy
        image = cv2.imdecode(np.fromstring(upload_image.read(), np.uint8), 1)
        # Chama a classe FaceDetection com o parâmetro "image"
        face_detection_image = FaceDetection(file_image=image)
        # Executa a função de detecção de faces em imagens
        image_generator = face_detection_image.detecting_faces_image()
        # Retorna a imagem na aplicação
        st.image(image_generator, channels="BGR")
````

````python
    # Criação de um título para a parte de webcam
    st.sidebar.title("WEBCAM")
    # Butão criado para iniciar a webcam
    start_webcam_button = st.sidebar.button("INICIAR WEBCAM")
    # Caso o botão seja apertado, irá chamar a classe FaceDetection executando a função
    # para detecção de faces na webcam
    if start_webcam_button:
        face_detection_webcam = FaceDetection()
        face_detection_webcam.detecting_faces_webcam()
````
# SUMMARY
Repository directed to the use of specific libraries for the identification of faces in image and video formats and even being able to be tested on your webcam.

# INTRODUCTION
The application was built aiming at the user's freedom to carry out their tests with their own photos and videos. It can even be used for facial recognition of specific people and street monitoring through security cameras (not yet applied within this repository).

# SOLUTION
Using the python library, [MTCNN](https://pypi.org/project/mtcnn/), it is possible to apply the face detection function to images and videos, loaded by the library [opencv](https:// docs.opencv.org/4.x/). The demonstration of the images/videos were made within a [streamlit](https://docs.streamlit.io) application.

# TOOLS
pycharm community Edition 2023.1

python 3.9.13

click==8.1.3

mtcnn==0.1.1

numpy==1.23.5

opencv-python==4.7.0.72

streamlit==1.22.0

google colab

# ABOUT THE CODE
````python
# Library used to build the application and put the project into production
import streamlit as st
# Creation of the rectangle and loading of images/videos/webcam
import cv2
# face detection
from mtcnn import MTCNN
# Convert a sequence of bytes to a NumPy array.
import numpy as np
# Create a temporary file on the file system with a unique name.
import tempfile
````

````python
# Class created for using the face detection function in videos and images
# loaded by opencv
class FaceDetection:
    def __init__(self, file_image='', file_video=''):
        # Instance of a face detector object 
        self.detector = MTCNN()
        # Instance of receiving the image
        self.image = file_image
        # Instance of receiving the video
        self.video = file_video
````

````python
    # Function used to apply face detection in images
    def detecting_faces_image(self):
        # perform face detection on the image
        result = self.detector.detect_faces(self.image)
        # loop over each element (dictionary) present in the 'result' list
        for faces in result:
            # The values of the 'box' keys are extracted and assigned to the variables x, y,
            # width and height. This information represents the coordinates and dimensions 
            # of the bounding box (rectangle) around the detected face.
            x, y, width, height = faces['box']
            # Draw a rectangle on the original image
            cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 0, 255), 2)
        # Returns the image with a rectangle on the face
        return self.image
````

````python
    # Function used to apply face detection in videos
    def detecting_faces_video(self):
        # Loop to be maintained while the video is open
        while self.video.isOpened():
            # Checking if each frame of self.video was read and stored
            # ret is a boolean value that indicates whether the frame was read
            ret, frame = self.video.read()
            # Indicates that the next frame of the video could not be read.
            if not ret:
                break
            # Detect faces in picture frame.
            result = self.detector.detect_faces(frame)
            # loop over each element (dictionary) present in the 'result' list
            for face in result:
                # The values of the 'box' keys are extracted and assigned to the variables
                # x, y, width and height. This information represents the coordinates
                # and dimensions of the bounding box (rectangle) around the
                # face detected.
                x, y, w, h = face['box']
                # Draw a rectangle on the original image
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # Convert image frame from BGR format to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Generator function, which can be iterated to get each frame
            # Processed individually.
            yield frame
````

````python
    # Function to detect faces on your webcam
    def detecting_faces_webcam(self):
        # Start your webcam
        cap = cv2.VideoCapture(0)
        # Loop that stops when it is not possible to read the next frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Face detection using MTCNN
            results = self.detector.detect_faces(frame)

            # Draw rectangles around detected faces
            for result in results:
                x, y, w, h = result['box']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Show the frame with the rectangles of the detected faces
            cv2.imshow('Webcam', frame)

            # Loop exit condition (by pressing "q" key)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # Release the resources
            cap.release()
            cv2.destroyAllWindows()
````

````python
if __name__ == '__main__':
    # Criação de um título para vídeos na barra lateral
    st.sidebar.title("ESCOLHA UM VÍDEO")
    # Função que dá permissão ao usuário para carregar seus próprios vídeos
    uploaded_file = st.sidebar.file_uploader("", type=["mp4", "avi"])
    if uploaded_file is not None:
        # Cria um arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        # Escreve a string como Bytes no arquivo temporário
        temp_file.write(uploaded_file.read())
        # Recebe o nome do arquivo temporário e o fecha
        video_path = temp_file.name
        temp_file.close()
        # Capturar fluxos de vídeo de arquivos de vídeo
        video = cv2.VideoCapture(video_path)
        # Retonar a classe FaceDetection recebendo o parâmetro "video"
        face_detection_video = FaceDetection(file_video=video)
        # Inicia a função para detecção em vídeos
        video_generator = face_detection_video.detecting_faces_video()
        # Criar e atualizar elementos de exibição interativos em aplicativos 
        stframe = st.empty()
        while True:
            try:
                # Obter o próximo quadro do vídeo
                frame = next(video_generator)
                # Exibir o quadro na interface
                stframe.image(frame, channels="RGB")
            # Indicar o final de uma iteração
            except StopIteration:
                break
    # Possibilidade de testar vídeos já carregados dentro da aplicação
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
````

````python
    # Criação de um título para imagens na barra lateral
    st.sidebar.title("ESCOLHA UMA IMAGEM")
    # Função para carregar imagens em seu próprio dispositivo
    upload_image = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])
    if upload_image is not None:
        # Decodificar e ler a imagem representada pelo array NumPy
        image = cv2.imdecode(np.fromstring(upload_image.read(), np.uint8), 1)
        # Chama a classe FaceDetection com o parâmetro "image"
        face_detection_image = FaceDetection(file_image=image)
        # Executa a função de detecção de faces em imagens
        image_generator = face_detection_image.detecting_faces_image()
        # Retorna a imagem na aplicação
        st.image(image_generator, channels="BGR")
````

````python
    # Criação de um título para a parte de webcam
    st.sidebar.title("WEBCAM")
    # Butão criado para iniciar a webcam
    start_webcam_button = st.sidebar.button("INICIAR WEBCAM")
    # Caso o botão seja apertado, irá chamar a classe FaceDetection executando a função
    # para detecção de faces na webcam
    if start_webcam_button:
        face_detection_webcam = FaceDetection()
        face_detection_webcam.detecting_faces_webcam()
````