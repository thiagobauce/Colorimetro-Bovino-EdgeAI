"""
Módulo de Pré-Processamento de Imagens do Colorímetro.

Etapa 1: Isolamento da Abertura Circular do Cano PVC (fundo externo → branco 255)
Etapa 2: Detecção adaptativa da Mancha de Pele dentro da abertura (PELE vs PELO)
"""

import cv2
import numpy as np


# ─────────────────────────────────────────────────────────────
# ETAPA 1: Remoção do Fundo Preto do Cano PVC
# ─────────────────────────────────────────────────────────────

def _detectar_circulo_abertura(gray, blur_kernel=(25, 25)):
    """
    Detecta o círculo da abertura do cano PVC na imagem grayscale.
    Usa três estratégias em cascata:
      1. Contorno do maior blob iluminado após threshold Otsu (valida circularidade)
      2. HoughCircles (robusto para pelo escuro que deforma o contorno)
      3. Fallback geométrico (centro + raio conservador)

    Retorna (cx, cy, radius) em pixels.
    """
    h, w = gray.shape
    blur = cv2.GaussianBlur(gray, blur_kernel, 0)

    # --- Estratégia A: Maior blob iluminado com validação de circularidade ---
    otsu_val, _ = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh_val = max(otsu_val * 0.65, 30)
    _, binary = cv2.threshold(blur, thresh_val, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    cnts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if cnts:
        c_max = max(cnts, key=cv2.contourArea)
        area_cnt = cv2.contourArea(c_max)
        (cx, cy), r = cv2.minEnclosingCircle(c_max)
        area_min_circle = np.pi * r ** 2
        # Circularidade: razão entre área real do contorno e área do círculo mínimo
        # Um círculo perfeito = 1.0; formas deformadas ficam abaixo de 0.75
        circularidade = area_cnt / area_min_circle if area_min_circle > 0 else 0
        # Aceitar se cobrir pelo menos 5% da imagem E for suficientemente circular
        if area_cnt > 0.05 * h * w and circularidade >= 0.72:
            return int(cx), int(cy), int(r)

    # --- Estratégia B: HoughCircles (detecta anel do PVC mesmo com pelo escuro) ---
    gray_blur2 = cv2.GaussianBlur(gray, (15, 15), 0)
    min_r = int(min(h, w) * 0.18)
    max_r = int(min(h, w) * 0.55)
    circles = cv2.HoughCircles(
        gray_blur2, cv2.HOUGH_GRADIENT, dp=1.5,
        minDist=min(h, w) // 2,
        param1=50, param2=40,
        minRadius=min_r, maxRadius=max_r
    )
    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)
        # Selecionar o círculo mais próximo do centro da imagem
        center = np.array([w // 2, h // 2])
        best = min(circles, key=lambda c: np.linalg.norm(c[:2] - center))
        return int(best[0]), int(best[1]), int(best[2])

    # --- Estratégia C: Fallback — centro + raio conservador ---
    return w // 2, h // 2, int(min(h, w) * 0.40)



def detectar_e_recortar_abertura_pvc(
    img_bgr,
    margin_pct=0.02,
    target_size=None,
    apply_circular_mask=True,
    blur_kernel=(25, 25),
    bg_color=(255, 255, 255)
):
    """
    Isola a abertura circular do cano PVC e pinta o fundo externo com bg_color (padrão: branco 255).

    Parâmetros:
    -----------
    img_bgr       : np.ndarray  — Imagem BGR de entrada.
    margin_pct    : float       — Margem interna (% do raio) para eliminar borda de plástico.
    target_size   : tuple|None  — (w, h) para redimensionamento. None = resolução original.
    apply_circular_mask : bool  — Se True, preenche o exterior com bg_color.
    blur_kernel   : tuple       — Kernel Gaussiano para suavização na detecção.
    bg_color      : tuple       — Cor BGR do fundo externo (padrão branco = (255,255,255)).

    Retorna:
    --------
    cropped_img  : np.ndarray  — Imagem recortada com fundo tratado.
    mask         : np.ndarray  — Máscara binária da abertura circular.
    metadata     : dict        — {center, radius, effective_radius, bbox}
    """
    h_orig, w_orig = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    cx, cy, radius = _detectar_circulo_abertura(gray, blur_kernel=blur_kernel)
    effective_radius = int(radius * (1.0 - margin_pct))

    # Máscara circular
    mask = np.zeros((h_orig, w_orig), dtype=np.uint8)
    cv2.circle(mask, (cx, cy), effective_radius, 255, -1)

    # Aplicar fundo branco fora da abertura
    processed = img_bgr.copy()
    if apply_circular_mask:
        processed[mask == 0] = bg_color

    # Recorte Bounding Box quadrado centrado
    r = effective_radius
    x1 = max(0, cx - r)
    y1 = max(0, cy - r)
    x2 = min(w_orig, cx + r)
    y2 = min(h_orig, cy + r)

    cropped_img = processed[y1:y2, x1:x2]
    cropped_mask = mask[y1:y2, x1:x2]

    if target_size is not None:
        cropped_img = cv2.resize(cropped_img, target_size, interpolation=cv2.INTER_AREA)
        cropped_mask = cv2.resize(cropped_mask, target_size, interpolation=cv2.INTER_NEAREST)

    metadata = {
        'center': (cx, cy),
        'radius': radius,
        'effective_radius': effective_radius,
        'bbox': (x1, y1, x2 - x1, y2 - y1)
    }
    return cropped_img, cropped_mask, metadata


# ─────────────────────────────────────────────────────────────
# ETAPA 2: Detecção Adaptativa da Mancha de Pele
# ─────────────────────────────────────────────────────────────

def detectar_mancha_pele(
    img_bgr,
    percentual_borda=0.05,
    proporcao_max_mancha=0.60,
    debug=False
):
    """
    Detecta e recorta a mancha de pele (região raspada escura) dentro da abertura do colorímetro.

    Estratégia automática:
    ─ PELE: mancha escura isolada → detecta e recorta apenas a mancha + padding.
    ─ PELO: amostra uniforme sem mancha → retorna a abertura inteira.

    A distinção é feita pelos percentis da luminância interna:
    · p5 < 60 AND std > 30  →  PELE (pixels muito escuros presentes = mancha)
    · caso contrário        →  PELO (sem contraste de mancha)

    Parâmetros:
    -----------
    img_bgr             : np.ndarray  — Imagem BGR (já com fundo branco externo).
    percentual_borda    : float       — Padding em % do tamanho da mancha (padrão 5%).
    proporcao_max_mancha: float       — Se a mancha cobrir mais que X% da abertura,
                                        considera fallback (amostra inteira).
    debug               : bool        — Se True, retorna dicionário com imagens de debug.

    Retorna:
    --------
    crop_final : np.ndarray  — Imagem recortada da mancha (ou abertura inteira para PELO).
    bbox_crop  : tuple       — (x1, y1, x2, y2) na imagem original.
    tipo       : str         — 'PELE_MANCHA', 'PELO_ABERTURA_INTEIRA', ou 'FALLBACK'.
    info       : dict        — Metadados (p5, std, thresh, area_pct, etc.).
    """
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    max_h, max_w = gray.shape

    # ── Passo 1: Isolar a abertura (blobde luz / excluir fundo branco) ──
    _, thresh_luz = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    contornos_luz, _ = cv2.findContours(thresh_luz, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contornos_luz:
        crop = img_bgr.copy()
        return crop, (0, 0, max_w, max_h), 'FALLBACK_SEM_ABERTURA', {}

    maior_luz = max(contornos_luz, key=cv2.contourArea)
    area_abertura = cv2.contourArea(maior_luz)
    bx, by, bw, bh = cv2.boundingRect(maior_luz)

    mascara_abertura = np.zeros_like(gray)
    cv2.drawContours(mascara_abertura, [maior_luz], -1, 255, thickness=cv2.FILLED)

    # ── Passo 2: Pintar fundo branco e analisar contraste ──
    gray_iso = gray.copy()
    gray_iso[mascara_abertura == 0] = 255

    pixels_int = gray_iso[mascara_abertura > 0]
    p5  = int(np.percentile(pixels_int, 5))
    p25 = int(np.percentile(pixels_int, 25))
    p50 = int(np.percentile(pixels_int, 50))
    std = int(np.std(pixels_int))

    info = {'p5': p5, 'p25': p25, 'p50': p50, 'std': std, 'area_abertura': int(area_abertura)}

    # ── Passo 3: Decisão PELE vs PELO ──
    tem_mancha = (p5 < 60) and (std > 30)

    if not tem_mancha:
        # ── PELO: retornar abertura inteira ──
        pad_w = int(bw * percentual_borda)
        pad_h = int(bh * percentual_borda)
        y1 = max(0, by - pad_h)
        y2 = min(max_h, by + bh + pad_h)
        x1 = max(0, bx - pad_w)
        x2 = min(max_w, bx + bw + pad_w)
        crop = img_bgr[y1:y2, x1:x2]
        info['tipo_detectado'] = 'PELO'
        return crop, (x1, y1, x2, y2), 'PELO_ABERTURA_INTEIRA', info

    # ── PELE: detectar mancha escura ──
    thresh_mancha = min(p50 - 10, 105)
    info['thresh_mancha'] = thresh_mancha

    # Excluir zona da etiqueta (top 20% da abertura)
    # A etiqueta com o número do animal fica sempre na parte superior
    mascara_sem_label = mascara_abertura.copy()
    label_cutoff = by + int(bh * 0.22)
    mascara_sem_label[:label_cutoff, :] = 0

    gray_iso_sem_label = gray.copy()
    gray_iso_sem_label[mascara_sem_label == 0] = 255

    blur_mancha = cv2.GaussianBlur(gray_iso_sem_label, (151, 151), 0)
    _, mascara_mancha = cv2.threshold(blur_mancha, thresh_mancha, 255, cv2.THRESH_BINARY_INV)

    kernel_m = np.ones((61, 61), np.uint8)
    mascara_mancha = cv2.morphologyEx(mascara_mancha, cv2.MORPH_CLOSE, kernel_m)
    mascara_mancha = cv2.morphologyEx(mascara_mancha, cv2.MORPH_OPEN, kernel_m)

    contornos_m, _ = cv2.findContours(mascara_mancha, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contornos_m:
        crop = img_bgr[by:by+bh, bx:bx+bw]
        info['tipo_detectado'] = 'PELE_FALLBACK_SEM_CONTORNO'
        return crop, (bx, by, bx+bw, by+bh), 'FALLBACK', info

    # Filtrar: manter só contornos com área >= 10% da abertura (ignora patches de pelo aleatórios)
    area_min = 0.10 * (bw * bh)
    contornos_validos = [c for c in contornos_m if cv2.contourArea(c) >= area_min]

    if not contornos_validos:
        # Nenhum contorno suficientemente grande → fallback para abertura inteira
        crop = img_bgr[by:by+bh, bx:bx+bw]
        info['tipo_detectado'] = 'PELE_FALLBACK_PEQUENA'
        return crop, (bx, by, bx+bw, by+bh), 'FALLBACK', info

    maior_m = max(contornos_validos, key=cv2.contourArea)
    X, Y, W, H = cv2.boundingRect(maior_m)
    area_mancha = W * H
    proporcao = area_mancha / (bw * bh) if bw * bh > 0 else 1.0
    info['area_mancha'] = area_mancha
    info['proporcao_mancha'] = round(proporcao, 3)

    if proporcao > proporcao_max_mancha:
        # Mancha muito grande → abertura inteira
        crop = img_bgr[by:by+bh, bx:bx+bw]
        info['tipo_detectado'] = 'PELE_FALLBACK_GRANDE'
        return crop, (bx, by, bx+bw, by+bh), 'FALLBACK', info

    # Crop preciso da mancha + padding
    pad_w = int(W * percentual_borda)
    pad_h = int(H * percentual_borda)
    y1 = max(0, Y - pad_h)
    y2 = min(max_h, Y + H + pad_h)
    x1 = max(0, X - pad_w)
    x2 = min(max_w, X + W + pad_w)
    crop = img_bgr[y1:y2, x1:x2]
    info['tipo_detectado'] = 'PELE_MANCHA'
    info['mancha_bbox'] = (X, Y, W, H)

    return crop, (x1, y1, x2, y2), 'PELE_MANCHA', info


# ─────────────────────────────────────────────────────────────
# PIPELINE COMPLETO: PVC → Mancha (uma chamada)
# ─────────────────────────────────────────────────────────────

def pipeline_completo(
    img_bgr_original,
    margin_pvc=0.02,
    percentual_borda=0.05,
    target_size_pvc=None
):
    """
    Executa o pipeline completo em uma imagem original:
      1. Isola abertura do PVC e preenche com branco 255
      2. Detecta a mancha de pele (ou usa abertura inteira para pelo)

    Retorna:
    --------
    pvc_crop  : imagem com fundo branco, recortada na abertura
    spot_crop : imagem da mancha (ou abertura inteira)
    tipo      : 'PELE_MANCHA' | 'PELO_ABERTURA_INTEIRA' | 'FALLBACK'
    meta      : dicionário com todos os metadados
    """
    pvc_crop, pvc_mask, pvc_meta = detectar_e_recortar_abertura_pvc(
        img_bgr_original,
        margin_pct=margin_pvc,
        target_size=target_size_pvc,
        bg_color=(255, 255, 255)
    )
    spot_crop, spot_bbox, tipo, spot_info = detectar_mancha_pele(
        pvc_crop,
        percentual_borda=percentual_borda
    )
    meta = {**pvc_meta, **spot_info, 'spot_bbox': spot_bbox, 'tipo': tipo}
    return pvc_crop, spot_crop, tipo, meta


if __name__ == "__main__":
    import argparse
    import re
    import json

    parser = argparse.ArgumentParser(
        description="Pipeline de Pré-Processamento do Colorímetro (PVC → Mancha)"
    )
    parser.add_argument(
        "--pastas", nargs="+", required=True,
        metavar="PASTA",
        help="Uma ou mais pastas de origem com imagens de pele/pelo"
    )
    parser.add_argument(
        "--out_pvc", default="Amostras_Sincronizadas_YOLO",
        metavar="DIR",
        help="Diretório de saída para crops com fundo PVC removido (padrão: Amostras_Sincronizadas_YOLO)"
    )
    parser.add_argument(
        "--out_mancha", default="Amostras_Mancha",
        metavar="DIR",
        help="Diretório de saída para crops da mancha de pele (padrão: Amostras_Mancha)"
    )
    parser.add_argument(
        "--out_debug", default=None,
        metavar="DIR",
        help="Diretório de saída para painéis visuais de debug (opcional)"
    )
    parser.add_argument(
        "--margin_pvc", type=float, default=0.02,
        metavar="FLOAT",
        help="Margem interna do círculo PVC em %% do raio (padrão: 0.02)"
    )
    parser.add_argument(
        "--borda_mancha", type=float, default=0.05,
        metavar="FLOAT",
        help="Padding ao redor da mancha detectada em %% do tamanho (padrão: 0.05)"
    )
    parser.add_argument(
        "--log", default="pipeline_log.json",
        metavar="FILE",
        help="Arquivo JSON de log com metadados de cada amostra (padrão: pipeline_log.json)"
    )
    args = parser.parse_args()

    import os
    import cv2
    import numpy as np

    os.makedirs(args.out_pvc,    exist_ok=True)
    os.makedirs(args.out_mancha, exist_ok=True)
    if args.out_debug:
        os.makedirs(args.out_debug, exist_ok=True)

    log_entries = []
    total_ok = total_fail = 0

    for pasta in args.pastas:
        if not os.path.exists(pasta):
            print(f"[AVISO] Pasta não encontrada: {pasta}")
            continue

        arquivos = os.listdir(pasta)
        pele_map, pelo_map = {}, {}
        for f in arquivos:
            if not f.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            nums = re.findall(r"\d+", f)
            if not nums:
                continue
            aid = nums[0]
            if "pele" in f.lower():
                pele_map[aid] = f
            elif "pelo" in f.lower():
                pelo_map[aid] = f

        ids_comuns = sorted(set(pele_map) & set(pelo_map), key=int)
        coleta = os.path.basename(pasta)
        print(f"  {coleta!r}: {len(ids_comuns)} pares encontrados")

        for aid in ids_comuns:
            try:
                # ── PELE ──
                img_pele = cv2.imread(os.path.join(pasta, pele_map[aid]))
                pvc_pele, spot_pele, tipo_pele, meta_pele = pipeline_completo(
                    img_pele,
                    margin_pvc=args.margin_pvc,
                    percentual_borda=args.borda_mancha
                )
                cv2.imwrite(os.path.join(args.out_pvc,    f"{aid}_PELE_pvc.jpg"),    pvc_pele)
                cv2.imwrite(os.path.join(args.out_mancha, f"{aid}_PELE_mancha.jpg"), spot_pele)

                # ── PELO: mesma geometria PVC da pele (sincronização do círculo) ──
                img_pelo = cv2.imread(os.path.join(pasta, pelo_map[aid]))
                cx, cy = meta_pele["center"]
                r      = meta_pele["effective_radius"]
                h_p, w_p = img_pelo.shape[:2]
                mask_pelo = np.zeros((h_p, w_p), dtype=np.uint8)
                cv2.circle(mask_pelo, (cx, cy), r, 255, -1)
                pelo_masked = img_pelo.copy()
                pelo_masked[mask_pelo == 0] = (255, 255, 255)
                pvc_x1, pvc_y1 = max(0, cx - r), max(0, cy - r)
                pvc_x2, pvc_y2 = min(w_p, cx + r), min(h_p, cy + r)
                pvc_pelo = pelo_masked[pvc_y1:pvc_y2, pvc_x1:pvc_x2]
                cv2.imwrite(os.path.join(args.out_pvc, f"{aid}_PELO_pvc.jpg"), pvc_pelo)

                # ── PELO mancha: MESMAS coordenadas de spot_bbox da PELE ──
                # spot_bbox é (x1, y1, x2, y2) relativo ao pvc_crop (mesmo tamanho para pele e pelo)
                sx1, sy1, sx2, sy2 = meta_pele["spot_bbox"]
                # Garantir que as coords cabem no crop do pelo
                ph, pw = pvc_pelo.shape[:2]
                sx1c = max(0, min(sx1, pw)); sx2c = max(0, min(sx2, pw))
                sy1c = max(0, min(sy1, ph)); sy2c = max(0, min(sy2, ph))
                spot_pelo = pvc_pelo[sy1c:sy2c, sx1c:sx2c]
                # Se ficou vazio (ex: FALLBACK que usou abertura inteira), usa pvc_pelo inteiro
                if spot_pelo.size == 0:
                    spot_pelo = pvc_pelo
                cv2.imwrite(os.path.join(args.out_mancha, f"{aid}_PELO_mancha.jpg"), spot_pelo)

                # ── Debug visual ──
                if args.out_debug:
                    vis = 600
                    panel = np.hstack([
                        cv2.resize(img_pele,  (vis, vis)),
                        cv2.resize(pvc_pele,  (vis, vis)),
                        cv2.resize(spot_pele, (vis, vis)),
                        cv2.resize(img_pelo,  (vis, vis)),
                        cv2.resize(pvc_pelo,  (vis, vis)),
                    ])
                    cv2.putText(panel, f"ID {aid} | {tipo_pele}", (10, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
                    cv2.imwrite(os.path.join(args.out_debug, f"{aid}_{coleta[:3]}_debug.jpg"), panel)

                log_entries.append({
                    "coleta": coleta, "animal_id": int(aid), "tipo_pele": tipo_pele,
                    "p5": meta_pele.get("p5"), "std": meta_pele.get("std"),
                    "pvc_cx": cx, "pvc_cy": cy, "pvc_r": r,
                })
                total_ok += 1
                print(f"    ✓ ID {aid:>6} | {tipo_pele}")

            except Exception as e:
                print(f"    ✗ ID {aid}: {e}")
                total_fail += 1

    with open(args.log, "w", encoding="utf-8") as f:
        json.dump(log_entries, f, ensure_ascii=False, indent=2)

    print(f"\n  Concluído: {total_ok} OK | {total_fail} falhas")
    print(f"  PVC crops : {args.out_pvc}")
    print(f"  Manchas   : {args.out_mancha}")
    print(f"  Log JSON  : {args.log}")
