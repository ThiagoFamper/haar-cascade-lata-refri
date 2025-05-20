# rodar no terminal dps de rodar o auto pipeline
# opencv_createsamples -info positives_annotations.txt -num 30 -w 50 -h 50 -vec positives.vec
# mkdir classifier opencv_traincascade -data classifier -vec positives.vec -bg negatives.txt -numPos 30 -numNeg 50 -numStages 20 -w 50 -h 50

import cv2
import os


def annotate_image(image_path):
    """
    Abre a imagem e permite selecionar a região (ROI) da lata.
    Retorna a tupla (x, y, w, h) se a seleção for válida, senão None.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro ao carregar a imagem: {image_path}")
        return None

    # Exibe a imagem e permite a seleção da região
    clone = img.copy()
    roi = cv2.selectROI("Selecione a área da lata e pressione ENTER ou SPACE", clone, showCrosshair=True)
    cv2.destroyWindow("Selecione a área da lata e pressione ENTER ou SPACE")

    x, y, w, h = roi
    if w == 0 or h == 0:
        print("ROI inválida. Selecione novamente.")
        return None

    height, width = img.shape[:2]
    if x < 0 or y < 0 or (x + w) > width or (y + h) > height:
        print(f"ROI fora dos limites da imagem {image_path}. Dimensões da imagem: {width}x{height}")
        return None

    return (x, y, w, h)


def gerar_arquivo_positives(positives_dir, output_file):
    """
    Percorre as imagens em 'positives_dir', anota e gera um arquivo com o formato:
    caminho/para/imagem.jpg 1 x y w h
    """
    with open(output_file, "w") as f:
        for filename in os.listdir(positives_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(positives_dir, filename)
                print(f"Anotando: {image_path}")
                roi = annotate_image(image_path)
                if roi:
                    x, y, w, h = roi
                    f.write(f"{image_path} 1 {x} {y} {w} {h}\n")
                else:
                    print(f"Anotação inválida para: {image_path}")
    print(f"Lista de anotações salva em: {output_file}")


def gerar_arquivo_negatives(negatives_dir, output_file):
    """
    Gera o arquivo negatives.txt com o caminho para cada imagem negativa.
    """
    with open(output_file, "w") as f:
        for filename in os.listdir(negatives_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(negatives_dir, filename)
                f.write(image_path + "\n")
    print(f"Lista de imagens negativas salva em: {output_file}")


if __name__ == "__main__":
    positives_dir = os.path.join("dataset", "positives")
    negatives_dir = os.path.join("dataset", "negatives")

    gerar_arquivo_positives(positives_dir, "positives_annotations.txt")
    gerar_arquivo_negatives(negatives_dir, "negatives.txt")
