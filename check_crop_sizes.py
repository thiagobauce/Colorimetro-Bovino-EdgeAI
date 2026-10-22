import os
import cv2
import numpy as np

def analyze_directory(dir_path):
    if not os.path.exists(dir_path):
        print(f"Diretório não encontrado: {dir_path}")
        return

    print(f"\nAnalizando diretório: {dir_path}")
    print("-" * 50)
    
    arquivos = [f for f in os.listdir(dir_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not arquivos:
        print("Nenhuma imagem encontrada.")
        return

    larguras = []
    alturas = []
    tamanhos_arquivos = []
    menor_area = float('inf')
    maior_area = 0
    menor_img = ""
    maior_img = ""

    for f in arquivos:
        filepath = os.path.join(dir_path, f)
        tamanho_kb = os.path.getsize(filepath) / 1024
        tamanhos_arquivos.append(tamanho_kb)
        
        # Carrega apenas as dimensões da imagem (sem carregar toda a matriz se possível, mas cv2.imread é ok aqui)
        img = cv2.imread(filepath)
        if img is None:
            print(f"  [ERRO] Não foi possível ler: {f}")
            continue
            
        h, w = img.shape[:2]
        larguras.append(w)
        alturas.append(h)
        area = w * h
        
        if area < menor_area:
            menor_area = area
            menor_img = f"{f} ({w}x{h})"
            
        if area > maior_area:
            maior_area = area
            maior_img = f"{f} ({w}x{h})"

    if not larguras:
        return

    avg_w = int(np.mean(larguras))
    avg_h = int(np.mean(alturas))
    avg_kb = np.mean(tamanhos_arquivos)
    
    print(f"Total de imagens processadas : {len(larguras)}")
    print(f"Dimensão média               : {avg_w} x {avg_h}")
    print(f"Tamanho médio em disco       : {avg_kb:.2f} KB")
    print(f"Menor imagem                 : {menor_img}")
    print(f"Maior imagem                 : {maior_img}")
    print(f"Largura (Min/Max)            : {min(larguras)} / {max(larguras)}")
    print(f"Altura (Min/Max)             : {min(alturas)} / {max(alturas)}")
    print("-" * 50)


if __name__ == "__main__":
    base_dir = "/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro"
    dir_manchas = os.path.join(base_dir, "Amostras_Mancha")
    dir_pvc = os.path.join(base_dir, "Amostras_Sincronizadas_YOLO")

    analyze_directory(dir_pvc)
    analyze_directory(dir_manchas)
