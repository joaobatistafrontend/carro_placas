import cv2

classifier = cv2.CascadeClassifier('haarcascade_car.xml')  # ou 'cars.xml'

def detecta_carros(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # conversão para cinza
    carros = classifier.detectMultiScale(gray,
                                         scaleFactor=1.04, # valores menores = mais detecção, mais lento
                                         minNeighbors=1, # valores menores = mais falsos positivos
                                         minSize=(60, 60),flags=1)
    for (x, y, w, h) in carros:
        cv2.rectangle(frame, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)
    return frame

def Simulator(video):
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        carros_frame = detecta_carros(frame)
        cv2.imshow('frame', carros_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

video = cv2.VideoCapture('v2.mp4')
Simulator(video)
