💤 Detector de Sonolência com Alerta Sonoro
Este projeto utiliza visão computacional para detectar sinais de sonolência com base na abertura dos olhos. Quando os olhos permanecem fechados por mais de alguns segundos, um alerta sonoro é ativado para chamar a atenção do usuário — ideal para motoristas, estudantes ou profissionais que precisam se manter atentos.

🎯 Objetivo
Detectar automaticamente quando uma pessoa está com os olhos fechados por tempo prolongado e emitir um alerta sonoro para evitar acidentes ou perda de foco.

🧠 Tecnologias Utilizadas
OpenCV — para captura e processamento de vídeo

MediaPipe — para detecção de landmarks faciais

winsound — para emitir som no Windows

threading — para executar o alerta sonoro em paralelo

math, time — para cálculos e controle de tempo

⚙️ Como Funciona
A webcam é ativada e o rosto é detectado em tempo real.

São monitorados pontos específicos dos olhos (landmarks).

Se a distância entre os pontos indicar que os olhos estão fechados:

Um contador é iniciado.

Se os olhos permanecerem fechados por mais de 4 segundos, um alerta sonoro é ativado.

Quando os olhos se abrem novamente, o alerta é interrompido.

📦 Instalação
Instale as dependências:

bash
pip install opencv-python mediapipe
Execute o script:

bash
python detector_sonolencia.py
🖥️ Compatibilidade
✅ Windows (com winsound)

⚠️ Linux/Mac: requer adaptação do alerta sonoro (veja os comentários no código)

🔔 Personalização
Tempo de alerta: altere o valor tempo >= 4 para ajustar a sensibilidade.

Frequência e duração do som: modifique winsound.Beep(2000, 3000) conforme necessário.

🛑 Encerramento
Pressione a tecla q para encerrar o programa.

📸 Interface
Mensagens visuais na tela indicam:

"OLHOS ABERTOS"

"OLHOS FECHADOS"

"DORMINDO X SEG"

"NENHUMA FACE DETECTADA"

🤝 Contribuições
Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias, como:

Suporte multiplataforma para som

Detecção de piscadas ou múltiplas faces

Interface gráfica
