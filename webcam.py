import cv2

cap = cv2.VideoCapture(3)  # Tente com 0, se não funcionar, tente com 1, 2, etc.

if not cap.isOpened():
    print("Erro ao acessar a câmera")
else:
    print("Câmera acessada com sucesso!")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame")
        break

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
