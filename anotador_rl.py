import os
import cv2
import json
import numpy as np
import sys
import pvc_preprocessor

# ==========================================
# CONFIGURAÇÕES
# ==========================================
PASTAS_IMAGENS = [
    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Foto colorimetro-Julho2026',
    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Fotos colorímetro- fevereiro-2026',
    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/fotos colorímetro-dezembro-2025'
]

ARQUIVO_FEEDBACK = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/rl_feedback.json'

PASTA_SAIDA_PELE = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Dataset_RL/pele'
PASTA_SAIDA_PELO = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Dataset_RL/pelo'

def load_feedback():
    if os.path.exists(ARQUIVO_FEEDBACK):
        with open(ARQUIVO_FEEDBACK, 'r') as f:
            return json.load(f)
    return {}

def save_feedback(data):
    with open(ARQUIVO_FEEDBACK, 'w') as f:
        json.dump(data, f, indent=4)

def salvar_crops(pasta_origem, nome_pele, gt_coords):
    """
    Recorta a imagem da pele usando o gt_coords.
    Se existir a imagem de pelo correspondente, recorta 512x512 no centro do PVC.
    """
    caminho_pele = os.path.join(pasta_origem, nome_pele)
    
    # --- PELE ---
    img_pele = cv2.imread(caminho_pele)
    if img_pele is None: return
    pvc_crop_pele, _, _ = pvc_preprocessor.detectar_e_recortar_abertura_pvc(img_pele)
    
    x1, y1, x2, y2 = gt_coords
    # Garante limites
    h_p, w_p = pvc_crop_pele.shape[:2]
    x1, x2 = max(0, min(x1, w_p)), max(0, min(x2, w_p))
    y1, y2 = max(0, min(y1, h_p)), max(0, min(y2, h_p))
    crop_pele = pvc_crop_pele[y1:y2, x1:x2]
    
    os.makedirs(PASTA_SAIDA_PELE, exist_ok=True)
    cv2.imwrite(os.path.join(PASTA_SAIDA_PELE, nome_pele), crop_pele)
    
    # --- PELO ---
    nome_pelo = nome_pele.replace("PELE", "PELO").replace("pele", "pelo")
    caminho_pelo = os.path.join(pasta_origem, nome_pelo)
    
    if os.path.exists(caminho_pelo):
        img_pelo = cv2.imread(caminho_pelo)
        if img_pelo is not None:
            pvc_crop_pelo, _, _ = pvc_preprocessor.detectar_e_recortar_abertura_pvc(img_pelo)
            hp, wp = pvc_crop_pelo.shape[:2]
            cx, cy = wp // 2, hp // 2
            
            # Recorte 512x512 centrado
            px1 = max(0, cx - 256)
            px2 = min(wp, cx + 256)
            py1 = max(0, cy - 256)
            py2 = min(hp, cy + 256)
            
            crop_pelo = pvc_crop_pelo[py1:py2, px1:px2]
            
            os.makedirs(PASTA_SAIDA_PELO, exist_ok=True)
            cv2.imwrite(os.path.join(PASTA_SAIDA_PELO, nome_pelo), crop_pelo)

def redimensionar(img, max_dim=800):
    h, w = img.shape[:2]
    escala = min(max_dim/w, max_dim/h)
    novo_w, novo_h = int(w * escala), int(h * escala)
    return cv2.resize(img, (novo_w, novo_h)), escala

def calcular_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

class BBoxEditor:
    def __init__(self, win_name, img, initial_bbox):
        self.win_name = win_name
        self.h_img, self.w_img = img.shape[:2]
        
        self.tela_base = np.zeros((self.h_img + 80, self.w_img, 3), dtype=np.uint8)
        self.tela_base[:self.h_img, :] = img
        
        self.bbox = list(initial_bbox)
        self.dragging = None
        self.box_w = 0
        self.box_h = 0
        self.acao = None
        self.drew_new_box = False
        
        cv2.setMouseCallback(self.win_name, self.mouse_cb)

    def mouse_cb(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if y >= self.h_img:
                if x < self.w_img // 2:
                    self.acao = 'salvar'
                else:
                    self.acao = 'cancelar'
                return
                
            corners = [
                (self.bbox[0], self.bbox[1]), # 0: TL
                (self.bbox[2], self.bbox[1]), # 1: TR
                (self.bbox[0], self.bbox[3]), # 2: BL
                (self.bbox[2], self.bbox[3])  # 3: BR
            ]
            for i, (cx, cy) in enumerate(corners):
                if abs(x - cx) < 25 and abs(y - cy) < 25:
                    self.dragging = i
                    return
            
            # Clicou fora das bolinhas -> Desenhar do zero
            self.dragging = 5
            self.bbox = [x, y, x, y]
            self.drew_new_box = True
                
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.dragging is not None:
                if self.dragging == 0:
                    self.bbox[0], self.bbox[1] = x, y
                elif self.dragging == 1:
                    self.bbox[2], self.bbox[1] = x, y
                elif self.dragging == 2:
                    self.bbox[0], self.bbox[3] = x, y
                elif self.dragging == 3:
                    self.bbox[2], self.bbox[3] = x, y
                elif self.dragging == 5:
                    self.bbox[2], self.bbox[3] = x, y
                    
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = None

    def run(self):
        while True:
            tela = self.tela_base.copy()
            x1, y1, x2, y2 = [int(v) for v in self.bbox]
            
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            
            x1, x2 = max(0, min(x1, self.w_img)), max(0, min(x2, self.w_img))
            y1, y2 = max(0, min(y1, self.h_img)), max(0, min(y2, self.h_img))
            
            cv2.rectangle(tela, (x1, y1), (x2, y2), (0, 255, 0), 2)
            for cx, cy in [(x1,y1), (x2,y1), (x1,y2), (x2,y2)]:
                cv2.circle(tela, (cx, cy), 8, (0, 0, 255), -1)
                
            cv2.putText(tela, "AJUSTANDO... Arraste os pontos vermelhos", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 3)
            cv2.putText(tela, "AJUSTANDO... Arraste os pontos vermelhos", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            bw = self.w_img // 2
            cv2.rectangle(tela, (0, self.h_img), (bw, self.h_img+80), (0, 200, 0), -1)
            cv2.rectangle(tela, (bw, self.h_img), (self.w_img, self.h_img+80), (0, 0, 200), -1)
            
            cv2.rectangle(tela, (0, self.h_img), (bw, self.h_img+80), (0, 0, 0), 2)
            cv2.rectangle(tela, (bw, self.h_img), (self.w_img, self.h_img+80), (0, 0, 0), 2)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(tela, "SALVAR", (bw//2 - 60, self.h_img+50), font, 1, (255,255,255), 3)
            cv2.putText(tela, "CANCELAR", (bw + bw//2 - 70, self.h_img+50), font, 1, (255,255,255), 3)
            
            cv2.imshow(self.win_name, tela)
            k = cv2.waitKey(20) & 0xFF
            
            if k in [13, 32] or self.acao == 'salvar':
                return (x1, y1, x2, y2), self.drew_new_box
            elif k in [ord('c'), ord('C'), 27] or self.acao == 'cancelar':
                return None, False


def main():
    print("Iniciando Ferramenta de Anotação/Feedback para RL...")
    feedback = load_feedback()
    
    arquivos_totais = []
    for pasta in PASTAS_IMAGENS:
        if os.path.exists(pasta):
            imgs = sorted([f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.png')) and "pele" in f.lower()])
            for img in imgs:
                arquivos_totais.append((pasta, img))
                
    cv2.namedWindow("Anotador Feedback RL")
    
    idx = 0
    while idx < len(arquivos_totais):
        feedback = load_feedback()
        pasta, arquivo = arquivos_totais[idx]
        
        dados_vlm = None
        if arquivo in feedback:
            if feedback[arquivo].get('reward') is not None:
                idx += 1
                continue 
            else:
                dados_vlm = feedback[arquivo]
                
        caminho = os.path.join(pasta, arquivo)
        img_bgr = cv2.imread(caminho)
        if img_bgr is None:
            idx += 1
            continue
        
        pvc_crop, _, pvc_meta = pvc_preprocessor.detectar_e_recortar_abertura_pvc(img_bgr)
        
        if dados_vlm and dados_vlm.get('auto_coords') is not None:
            pvc_x1, pvc_y1, _, _ = pvc_meta['bbox']
            vx1, vy1, vx2, vy2 = dados_vlm['auto_coords']
            ax1 = vx1 - pvc_x1
            ay1 = vy1 - pvc_y1
            ax2 = vx2 - pvc_x1
            ay2 = vy2 - pvc_y1
            
            h_pvc, w_pvc = pvc_crop.shape[:2]
            ax1, ax2 = max(0, min(ax1, w_pvc)), max(0, min(ax2, w_pvc))
            ay1, ay2 = max(0, min(ay1, h_pvc)), max(0, min(ay2, h_pvc))
            
            coords_auto = (ax1, ay1, ax2, ay2)
            status_auto = dados_vlm.get('status_auto', 'VISION_REASONER')
            fonte_texto = f"IA (Prompt: {dados_vlm.get('prompt_id')}) -> Box: {vx1},{vy1},{vx2},{vy2}"
        else:
            _, coords_auto, status_auto, _ = pvc_preprocessor.detectar_mancha_pele(pvc_crop)
            ax1, ay1, ax2, ay2 = coords_auto
            fonte_texto = "OpenCV (Classico)"
            
        img_display, escala = redimensionar(pvc_crop, 850)
        
        d_ax1, d_ay1 = int(ax1 * escala), int(ay1 * escala)
        d_ax2, d_ay2 = int(ax2 * escala), int(ay2 * escala)
        
        h_tela, w_tela = img_display.shape[:2]
        
        tela_base = np.zeros((h_tela + 80, w_tela, 3), dtype=np.uint8)
        tela_base[:h_tela, :] = img_display
        
        bw = w_tela // 4
        btn_ok = (0, bw)
        btn_c  = (bw, 2*bw)
        btn_p  = (2*bw, 3*bw)
        btn_q  = (3*bw, w_tela)
        
        acao_global = [None]
        def menu_mouse_cb(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                if y >= h_tela:
                    if btn_ok[0] <= x <= btn_ok[1]: acao_global[0] = 'ok'
                    elif btn_c[0] <= x <= btn_c[1]: acao_global[0] = 'c'
                    elif btn_p[0] <= x <= btn_p[1]: acao_global[0] = 'p'
                    elif btn_q[0] <= x <= btn_q[1]: acao_global[0] = 'q'
        
        while True:
            acao_global[0] = None
            cv2.setMouseCallback("Anotador Feedback RL", menu_mouse_cb)
            
            tela = tela_base.copy()
            cv2.rectangle(tela, (d_ax1, d_ay1), (d_ax2, d_ay2), (0, 0, 255), 2)
            
            cv2.putText(tela, f"Arquivo: {arquivo} | {fonte_texto}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)
            cv2.putText(tela, f"Arquivo: {arquivo} | {fonte_texto}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
            
            # Print prompt (wrapped)
            prompt = dados_vlm.get('prompt_text', 'N/A') if dados_vlm else 'OpenCV pipeline (Sem prompt)'
            words = prompt.split(' ')
            linhas_prompt = []
            linha_atual = "Query: "
            for w in words:
                if len(linha_atual) + len(w) > 85:
                    linhas_prompt.append(linha_atual)
                    linha_atual = w + " "
                else:
                    linha_atual += w + " "
            linhas_prompt.append(linha_atual)
            
            for i_line, text_line in enumerate(linhas_prompt):
                y_pos = 55 + (i_line * 25)
                cv2.putText(tela, text_line.strip(), (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3)
                cv2.putText(tela, text_line.strip(), (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
            
            cv2.rectangle(tela, (btn_ok[0], h_tela), (btn_ok[1], h_tela+80), (0, 200, 0), -1)
            cv2.rectangle(tela, (btn_c[0], h_tela), (btn_c[1], h_tela+80), (0, 150, 255), -1)
            cv2.rectangle(tela, (btn_p[0], h_tela), (btn_p[1], h_tela+80), (200, 200, 0), -1)
            cv2.rectangle(tela, (btn_q[0], h_tela), (btn_q[1], h_tela+80), (50, 50, 200), -1)
            
            for b in [btn_ok[1], btn_c[1], btn_p[1]]:
                cv2.line(tela, (b, h_tela), (b, h_tela+80), (0,0,0), 2)
            cv2.line(tela, (0, h_tela), (w_tela, h_tela), (0,0,0), 2)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(tela, "OK", (btn_ok[0] + bw//2 - 25, h_tela+50), font, 1, (255,255,255), 3)
            cv2.putText(tela, "CORRIGIR", (btn_c[0] + bw//2 - 70, h_tela+50), font, 1, (255,255,255), 3)
            cv2.putText(tela, "PULAR", (btn_p[0] + bw//2 - 50, h_tela+50), font, 1, (255,255,255), 3)
            cv2.putText(tela, "SAIR", (btn_q[0] + bw//2 - 35, h_tela+50), font, 1, (255,255,255), 3)
                        
            cv2.imshow("Anotador Feedback RL", tela)
            key = cv2.waitKey(20) & 0xFF
            
            if key in [ord('q'), ord('Q'), 27] or acao_global[0] == 'q':
                print("Saindo...")
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                sys.exit(0)
                
            elif key in [ord('p'), ord('P')] or acao_global[0] == 'p':
                print(f"Pulou: {arquivo}")
                idx += 1
                break
                
            elif key in [13, 32] or acao_global[0] == 'ok':
                print(f"[{arquivo}] Aceito! Reward: 1.0")
                novo_dado = {
                    'auto_coords': coords_auto,
                    'gt_coords': coords_auto,
                    'status_auto': status_auto,
                    'reward': 1.0 
                }
                if dados_vlm:
                    novo_dado['prompt_id'] = dados_vlm.get('prompt_id')
                    novo_dado['prompt_text'] = dados_vlm.get('prompt_text')
                    
                feedback[arquivo] = novo_dado
                save_feedback(feedback)
                salvar_crops(pasta, arquivo, coords_auto)
                idx += 1
                break
                
            elif key in [ord('c'), ord('C')] or acao_global[0] == 'c':
                editor = BBoxEditor("Anotador Feedback RL", img_display, (d_ax1, d_ay1, d_ax2, d_ay2))
                bbox, drew_new_box = editor.run()
                
                if bbox is None: 
                    continue 
                
                dx1, dy1, dx2, dy2 = bbox
                gx1, gy1 = int(dx1 / escala), int(dy1 / escala)
                gx2, gy2 = int(dx2 / escala), int(dy2 / escala)
                gt_coords = (gx1, gy1, gx2, gy2)
                
                if drew_new_box:
                    reward = 0.0
                    print(f"[{arquivo}] Desenhado do zero! Reward fixado em 0.0")
                else:
                    reward = calcular_iou(coords_auto, gt_coords)
                    print(f"[{arquivo}] Corrigido! Reward: {reward:.4f}")
                    
                novo_dado = {
                    'auto_coords': coords_auto,
                    'gt_coords': gt_coords,
                    'status_auto': status_auto,
                    'reward': reward
                }
                if dados_vlm:
                    novo_dado['prompt_id'] = dados_vlm.get('prompt_id')
                    novo_dado['prompt_text'] = dados_vlm.get('prompt_text')
                    
                feedback[arquivo] = novo_dado
                save_feedback(feedback)
                salvar_crops(pasta, arquivo, gt_coords)
                idx += 1
                break

    cv2.destroyAllWindows()
    cv2.waitKey(1)
    print("Todas as imagens da pasta foram anotadas!")
    sys.exit(0)

if __name__ == '__main__':
    main()
