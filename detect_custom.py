import cv2

def main():
    cascade = cv2.CascadeClassifier('classifier/cascade.xml')
    if cascade.empty():
        print("Erro ao carregar o cascade.xml. Verifique o caminho e o arquivo gerado.")
        return

    image_path = 'teste2.jpg'
    frame = cv2.imread(image_path)
    if frame is None:
        print("Erro ao carregar a imagem. Verifique o caminho e o arquivo.")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    objects = cascade.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=50, minSize=(50, 50))
    print(f"Número de detecções: {len(objects)}")

    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Detector de Lata', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
