import cv2
import pytesseract

# Caso o executável não esteja no PATH usado pelo Python, ajuste aqui:

notbook = pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
pc = pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Carrega o cascade de placa (substitua pelo arquivo adequado ao seu país, se necessário)
plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

def reconhecer_placa(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(
        gray,
        scaleFactor=1.04,
        minNeighbors=1,
        minSize=(60,20)
    )

    placas_detectadas = []
    for (x, y, w, h) in plates:
        placa_roi = gray[y:y+h, x:x+w]
        
        # Pré-processamento para melhorar OCR
        placa_roi = cv2.bilateralFilter(placa_roi, 11, 17, 17)
        _, placa_roi = cv2.threshold(placa_roi, 150, 255, cv2.THRESH_BINARY)
        
        # Só caracteres alfanuméricos
        custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 7'
        texto = pytesseract.image_to_string(placa_roi, config=custom_config)
        texto = ''.join(filter(str.isalnum, texto))
        
        placas_detectadas.append((texto, (x, y, w, h)))
        
        # Desenha resultado
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, texto, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        
    return frame, placas_detectadas

def main(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erro ao abrir o vídeo")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, placas = reconhecer_placa(frame)
        for placa, _ in placas:
            print("Placa detectada:", placa)

        cv2.imshow('Deteccao de Placas', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main('v3.mp4')
