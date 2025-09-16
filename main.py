import cv2
import mediapipe as mp
import math
import time
import winsound  # Para Windows
import threading  # Para controlar o som em thread separada

# import os  # Para Linux/Mac (descomente se necessário)

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

inicio = 0
status = ""
alerta_ativo = False  # Controla se o alerta está ativo
thread_alerta = None  # Thread para o som contínuo
tempo = 0  # Inicializar a variável tempo


def tocar_alerta_continuo():
    """Função para tocar o alerta sonoro continuamente"""
    global alerta_ativo
    while alerta_ativo:
        try:
            # Para Windows - Som contínuo mais forte e longo
            winsound.Beep(2000, 3000)  # Frequência 2000Hz por 3 segundos (mais alto e forte)
            # Se ainda estiver ativo, continua sem pausa

            # Para Linux/Mac (descomente as linhas abaixo e comente o winsound)
            # while alerta_ativo:
            #     os.system('speaker-test -t sine -f 2000 &')  # Linux - som contínuo
            #     time.sleep(0.1)
            # os.system('killall speaker-test')  # Para o som no Linux

        except:
            print("ALERTA: ACORDAR! OLHOS FECHADOS POR MUITO TEMPO!")
            time.sleep(0.1)  # Pausa mínima se houver erro


def iniciar_alerta():
    """Inicia o alerta sonoro contínuo"""
    global alerta_ativo, thread_alerta
    if not alerta_ativo:
        alerta_ativo = True
        thread_alerta = threading.Thread(target=tocar_alerta_continuo)
        thread_alerta.daemon = True
        thread_alerta.start()


def parar_alerta():
    """Para o alerta sonoro"""
    global alerta_ativo
    alerta_ativo = False


def resetar_contador():
    """Reseta o contador de tempo quando não há detecção"""
    global inicio, tempo, status
    inicio = time.time()
    tempo = 0
    status = ""
    if alerta_ativo:
        parar_alerta()


while True:
    check, img = video.read()

    # Verifica se a câmera está funcionando
    if not check:
        print("Erro: Não foi possível capturar o frame da câmera")
        break

    img = cv2.resize(img, (1000, 720))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    h, w, _ = img.shape

    # Sempre mostra o status da câmera no canto superior esquerdo
    cv2.putText(img, "Camera Ativa", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Verifica se há detecção de face
    if results.multi_face_landmarks is not None:
        face_detected = False

        for face in results.multi_face_landmarks:
            face_detected = True

            # Pontos dos olhos
            di1x, di1y = int((face.landmark[159].x) * w), int((face.landmark[159].y) * h)
            di2x, di2y = int((face.landmark[145].x) * w), int((face.landmark[145].y) * h)
            es1x, es1y = int((face.landmark[386].x) * w), int((face.landmark[386].y) * h)
            es2x, es2y = int((face.landmark[374].x) * w), int((face.landmark[374].y) * h)

            # Desenha os pontos dos olhos
            cv2.circle(img, (di1x, di1y), 1, (255, 0, 0), 2)
            cv2.circle(img, (di2x, di2y), 1, (255, 0, 0), 2)
            cv2.circle(img, (es1x, es1y), 1, (255, 0, 0), 2)
            cv2.circle(img, (es2x, es2y), 1, (255, 0, 0), 2)

            # Calcula a distância entre os pontos dos olhos
            distDi = math.hypot(di1x - di2x, di1y - di2y)
            distEs = math.hypot(es1x - es2x, es1y - es2y)

            if distDi <= 10 and distEs <= 10:
                # Olhos fechados
                cv2.rectangle(img, (100, 60), (390, 110), (0, 0, 255), -1)
                cv2.putText(img, "OLHOS FECHADOS", (105, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                situacao = "F"
                if situacao != status:
                    inicio = time.time()
            else:
                # Olhos abertos
                cv2.rectangle(img, (100, 60), (370, 110), (0, 255, 0), -1)
                cv2.putText(img, "OLHOS ABERTOS", (105, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                situacao = "A"
                if status == "F":  # Se estava com olhos fechados, reseta o contador
                    resetar_contador()
                else:
                    inicio = time.time()
                    tempo = int(time.time() - inicio)

                # Para o alerta quando os olhos abrem
                if alerta_ativo:
                    parar_alerta()

            # Calcula o tempo com olhos fechados
            if situacao == 'F':
                tempo = int(time.time() - inicio)

            status = situacao

            # Verifica se está dormindo há mais de 3 segundos
            if tempo >= 4:
                cv2.rectangle(img, (300, 150), (850, 220), (0, 0, 255), -1)
                cv2.putText(img, f'DORMINDO {tempo} SEG', (310, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (255, 255, 255), 5)

                # Inicia o alerta contínuo se não estiver ativo
                if not alerta_ativo:
                    iniciar_alerta()

            print(f"Tempo: {tempo}")

        # Se detectou pelo menos uma face, não precisa fazer mais nada

    else:
        # Nenhuma face detectada - mostra mensagem e reseta contador
        cv2.rectangle(img, (100, 60), (450, 110), (255, 165, 0), -1)  # Cor laranja
        cv2.putText(img, "NENHUMA FACE DETECTADA", (105, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Reseta o contador quando não há detecção
        resetar_contador()

        print("Nenhuma face detectada")

    # Sempre mostra a imagem, independente de haver detecção ou não
    cv2.imshow('Detector de Sonolencia', img)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Para o alerta antes de fechar
parar_alerta()
video.release()
cv2.destroyAllWindows()