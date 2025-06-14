import cv2

def main():
    cascade = cv2.CascadeClassifier('classifier/cascade.xml')
    if cascade.empty():
        print("Erro ao carregar o cascade.xml. Verifique o caminho e o arquivo gerado.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao acessar a webcam.")
        return

    print("Pressione 'q' para sair.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame da webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        print(f"Número de detecções: {len(objects)}")

        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Detector de Lata (Webcam)', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()