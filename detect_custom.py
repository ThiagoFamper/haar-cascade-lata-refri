import cv2

def main():
    # Carrega o classificador treinado
    cascade = cv2.CascadeClassifier('classifier/cascade.xml')
    if cascade.empty():
        print("Erro ao carregar o cascade.xml. Verifique o caminho e o arquivo gerado.")
        return

    # Carrega a imagem de teste
    image_path = 'teste.png'
    frame = cv2.imread(image_path)
    if frame is None:
        print("Erro ao carregar a imagem. Verifique o caminho e o arquivo.")
        return

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Realiza a detecção com parâmetros ajustáveis
    objects = cascade.detectMultiScale(gray, scaleFactor=1.03, minNeighbors=3, minSize=(50, 50))
    print(f"Número de detecções: {len(objects)}")

    # Desenha retângulos ao redor de cada detecção
    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Detector com Imagem', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
