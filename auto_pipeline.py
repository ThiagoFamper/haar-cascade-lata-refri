# rodar no terminal dps de rodar o auto pipeline
# opencv_createsamples -info positives.txt -num 250 -w 50 -h 50 -vec positives.vec
# opencv_traincascade -data classifier -vec positives.vec -bg negatives.txt -numPos 250 -numNeg 400 -numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -w 50 -h 50


import cv2
import os


def annotate_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro ao carregar a imagem: {image_path}")
        return None

    clone = img.copy()
    rois = []  # Lista para armazenar múltiplos ROIs

    while True:
        # Seleção do ROI
        roi = cv2.selectROI("Selecione a lata e pressione ENTER ou ESC para finalizar", clone, showCrosshair=True)

        if roi == (0, 0, 0, 0):  # Verifica se o ROI é inválido
            break  # Se o ROI for inválido (0,0,0,0), finalize

        # Se o ROI for válido, adiciona à lista
        x, y, w, h = roi
        if w == 0 or h == 0:
            print("ROI inválido. Selecione novamente.")
            continue

        rois.append((x, y, w, h))  # Adiciona o ROI na lista

        # Desenhando o ROI na imagem original para visualização
        cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Desenha o retângulo

        # Mostra a imagem com os ROIs selecionados
        cv2.imshow("Selecione a lata e pressione ENTER ou ESC para finalizar", clone)

    cv2.destroyWindow("Selecione a lata e pressione ENTER ou ESC para finalizar")

    if not rois:
        print("Nenhum ROI selecionado.")
        return None

    return rois


def gerar_arquivo_positives(positives_dir, output_file):
    with open(output_file, "w") as f:
        for filename in os.listdir(positives_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(positives_dir, filename)
                print(f"Anotando: {image_path}")
                rois = annotate_image(image_path)
                if rois:
                    for roi in rois:
                        x, y, w, h = roi
                        f.write(f"{image_path} 1 {x} {y} {w} {h}\n")
                else:
                    print(f"Anotação inválida para: {image_path}")
    print(f"Lista de anotações salva em: {output_file}")


def gerar_arquivo_negatives(negatives_dir, output_file):
    with open(output_file, "w") as f:
        for filename in os.listdir(negatives_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(negatives_dir, filename)
                f.write(image_path + "\n")
    print(f"Lista de imagens negativas salva em: {output_file}")


if __name__ == "__main__":
    positives_dir = os.path.join("dataset", "positives")
    negatives_dir = os.path.join("dataset", "negatives")

    gerar_arquivo_positives(positives_dir, "positives.txt")
    gerar_arquivo_negatives(negatives_dir, "negatives.txt")