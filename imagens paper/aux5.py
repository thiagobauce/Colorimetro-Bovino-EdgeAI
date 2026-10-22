import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

# --- Configurações globais e fontes robustas ---
def get_font(size, bold=False):
    """Tenta carregar uma fonte sans-serif limpa e clara com suporte a acentos."""
    font_paths = [
        # Windows
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        # Mac/Linux (alternativas comuns que suportam acentos)
        "Arial Bold.ttf" if bold else "Arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "FreeSansBold.ttf" if bold else "FreeSans.ttf",
        "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except IOError:
            continue
    # Fallback para fonte padrão se nenhuma for encontrada (pode bug acentos)
    return ImageFont.load_default()

def draw_text_centered(draw, pos, text, font, fill="black"):
    """Desenha um texto centralizado em uma determinada posição, com fallback para Pillow antigo."""
    x, y = pos
    try:
        # Pillow moderno (>= 9.2.0)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback Pillow antigo (< 9.2.0)
        try:
            w, h = draw.textsize(text, font=font)
        except AttributeError:
            w, h = 80, 16 # Fallback final para evitar crash

    draw.text((x - w / 2, y - h / 2), text, font=font, fill=fill, align="center")

# --- Processamento de Imagens e Cálculos ---
def prepare_image_data(input_path):
    """Carrega a imagem de entrada e calcula as estatísticas necessárias."""
    if not os.path.exists(input_path):
        print(f"AVISO: Arquivo '{input_path}' não encontrado. Simulando dados de textura marrom.")
        # Criar imagem de textura simulada (marrom claro)
        base_img = Image.new('RGB', (100, 100), color='#D2B48C')
    else:
        base_img = Image.open(input_path).convert('RGB')
        
    img_np = np.array(base_img)
    
    # 1. Isolar canais RGB
    r, g, b = base_img.split()
    zero = Image.new('L', base_img.size)
    img_r_isolate = Image.merge('RGB', (r, zero, zero))
    img_g_isolate = Image.merge('RGB', (zero, g, zero))
    img_b_isolate = Image.merge('RGB', (zero, zero, b))
    
    # 2. Calcular médias de canais
    r_mean = np.mean(img_np[:,:,0])
    g_mean = np.mean(img_np[:,:,1])
    b_mean = np.mean(img_np[:,:,2])
    
    # 3. Converter para HSV e CIELAB (OpenCV style)
    bgr_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    hsv_np = cv2.cvtColor(bgr_np, cv2.COLOR_BGR2HSV)
    h_mean = np.mean(hsv_np[:,:,0])
    s_mean = np.mean(hsv_np[:,:,1])
    v_mean = np.mean(hsv_np[:,:,2])
    
    lab_np = cv2.cvtColor(bgr_np, cv2.COLOR_BGR2LAB)
    lcv2_mean = np.mean(lab_np[:,:,0])
    acv2_mean = np.mean(lab_np[:,:,1])
    bcv2_mean = np.mean(lab_np[:,:,2])
    
    # 4. Calcular atributos derivados
    epsilon = 1e-6 # Pequeno valor para evitar divisão por zero
    rg = r_mean / (g_mean + epsilon)
    rb = r_mean / (b_mean + epsilon)
    gb = g_mean / (b_mean + epsilon)
    diflv = lcv2_mean - v_mean
    somargb = r_mean + g_mean + b_mean
    
    results = {
        'original': base_img,
        'isolates': (img_r_isolate, img_g_isolate, img_b_isolate),
        'derived': (rg, rb, gb, diflv, somargb),
        'all_14': (r_mean, g_mean, b_mean, h_mean, s_mean, v_mean, lcv2_mean, acv2_mean, bcv2_mean, rg, rb, gb, diflv, somargb)
    }
    return results

# --- Funções de Desenho ---
def draw_colorful_block(draw, pos, size, text, fill_color, font, label_fill="black"):
    """Desenha um bloco colorido rotulado com largura dinâmica (para vetor)."""
    x, y = pos
    draw.rounded_rectangle([x, y, x+size[0], y+size[1]], radius=3, fill=fill_color, outline="#666", width=1)
    draw_text_centered(draw, (x + size[0]//2, y + size[1]//2), text, font, fill=label_fill)

def draw_arrow(draw, start_pos, direction='down'):
    """Desenha uma setinha de fluxo para baixo."""
    x, y = start_pos
    if direction == 'down':
        draw.polygon([(x-10, y), (x+10, y), (x+10, y+20), (x+20, y+20), (x, y+45), (x-20, y+20), (x-10, y+20)], fill="#1B365D")

def generate_diagram(input_path, output_path="diagrama_extracao_atributos.png"):
    """Gera o infográfico técnico completo."""
    data = prepare_image_data(input_path)
    
    # Configurações de layout - AUMENTADO TAMANHO TOTAL
    canvas_w = 1400
    canvas_h = 1500 # Aumentado de 1350 para dar mais espaço vertical
    bg_color = (255, 255, 255)
    
    # Criar canvas final
    final_img = Image.new('RGB', (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(final_img)
    
    # Fontes
    font_title = get_font(24, bold=True)
    font_header = get_font(20, bold=True)
    font_sub_title = get_font(18)
    font_label = get_font(16)
    font_formula = get_font(14)
    
    # Título Principal
    draw_text_centered(draw, (canvas_w//2, 40), "Processo de Extração de Atributos de Cor", font_title, fill="black")
    
    current_y = 100
    gap_between_sections = 100 # Aumentado espaçamento

    # --- SEÇÃO 1: CANAIS RGB ---
    section_h = 320
    draw.rounded_rectangle([20, current_y, canvas_w-20, current_y+section_h], radius=20, fill="#F0F8FF", outline="#D0E0F0")
    draw_text_centered(draw, (canvas_w//2, current_y + 40), "1. Canais RGB", font_header, fill="black")
    
    img_r, img_g, img_b = data['isolates']
    img_size_s1 = 200
    start_ch_x = (canvas_w - (img_size_s1*3 + 100)) // 2
    
    img_y = current_y + 110
    final_img.paste(img_r.resize((img_size_s1, img_size_s1)), (start_ch_x, img_y))
    final_img.paste(img_g.resize((img_size_s1, img_size_s1)), (start_ch_x + img_size_s1 + 50, img_y))
    final_img.paste(img_b.resize((img_size_s1, img_size_s1)), (start_ch_x + (img_size_s1 + 50)*2, img_y))
    
    # Rótulos RGB - MOVIDOS PARA CIMA DAS IMAGENS
    text_y_labels = img_y - 25
    draw_text_centered(draw, (start_ch_x + img_size_s1//2, text_y_labels), "R", font_header)
    draw_text_centered(draw, (start_ch_x + img_size_s1 + 50 + img_size_s1//2, text_y_labels), "G", font_header)
    draw_text_centered(draw, (start_ch_x + (img_size_s1 + 50)*2 + img_size_s1//2, text_y_labels), "B", font_header)
    
    draw_arrow(draw, (canvas_w//2, current_y + section_h + 10))
    current_y += section_h + gap_between_sections

    # --- SEÇÃO 2: ATRIBUTOS DERIVADOS ---
    section_h = 240
    draw.rounded_rectangle([20, current_y, canvas_w-20, current_y+section_h], radius=20, fill="#F0FFF0", outline="#D0F0D0")
    draw_text_centered(draw, (canvas_w//2, current_y + 30), "2. Atributos derivados (razões e diferenças)", font_header, fill="black")
    
    # Caixas de fórmula
    box_w = 170
    box_h = 150
    box_gap = 40
    start_box_x = (canvas_w - (box_w*5 + box_gap*4)) // 2
    
    box_formulas = [
        ("RG", "R / (G + \u03B5)"),
        ("RB", "R / (B + \u03B5)"),
        ("GB", "G / (B + \u03B5)"),
        ("DifLV", "L_{cv2} - V"),
        ("SomaRGB", "R + G + B")
    ]
    
    for i, (label, formula) in enumerate(box_formulas):
        bx = start_box_x + i * (box_w + box_gap)
        draw.rounded_rectangle([bx, current_y + 70, bx+box_w, current_y + 70 + box_h], radius=10, fill="white", outline="#CCCCCC")
        draw_text_centered(draw, (bx + box_w//2, current_y + 90), label, font_header)
        draw_text_centered(draw, (bx + box_w//2, current_y + 160), formula, font_formula)
        
    draw_arrow(draw, (canvas_w//2, current_y + section_h + 10))
    current_y += section_h + gap_between_sections

    # --- SEÇÃO 3: CONJUNTO TOTAL DE ATRIBUTOS ---
    # CORREÇÃO: AUMENTADO TAMANHO DOS PAINÉIS E DOS BLOCOS
    section_h = 360 # Aumentado
    draw.rounded_rectangle([20, current_y, canvas_w-20, current_y+section_h], radius=20, fill="#E6E6FA", outline="#D0D0F0")
    draw_text_centered(draw, (canvas_w//2, current_y + 30), "3. Conjunto total de atributos", font_header, fill="black")
    draw_text_centered(draw, (canvas_w//2, current_y + 70), "Os 14 atributos que compõem o vetor de características:", font_sub_title, fill="black")
    
    subgroup_h = 160 # Aumentado de 130 para dar mais espaço interno
    subgroup_gap = 30
    
    subgroups = [
        ("RGB (3)", "#D0E0F0", ["R", "G", "B"], "#A9CCE3"),
        ("HSV (3)", "#EBF4E5", ["H", "S", "V"], "#C9E2B3"),
        ("CIELAB (3)", "#EFE8F6", ["L_{cv2}", "a_{cv2}", "b_{cv2}"], "#D9C9EB"),
        ("Derivados (5)", "#E2F0D9", ["RG", "RB", "GB", "DifLV", "SomaRGB"], "#C5E0B4")
    ]
    
    block_gap = 15 # Aumentado espaçamento entre blocos
    
    # Primeiro calcular larguras para centralizar
    subgroup_widths = []
    subgroup_block_widths = []
    
    for i, (label, fill_col, blocks, block_fill) in enumerate(subgroups):
        total_group_blocks_w = 0
        block_widths = []
        for b_label in blocks:
            try:
                txt_w = draw.textsize(b_label, font=font_formula)[0]
            except AttributeError:
                txt_w = draw.textbbox((0, 0), b_label, font=font_formula)[2] - draw.textbbox((0, 0), b_label, font=font_formula)[0]
            
            b_w = max(60, txt_w + 20) # Aumentado tamanho base e padding
            block_widths.append(b_w)
            total_group_blocks_w += b_w + block_gap
        
        total_group_blocks_w -= block_gap # Remover o último gap
        subgroup_block_widths.append((total_group_blocks_w, block_widths))
        
        sg_w = max(200, total_group_blocks_w + 40) # Padding interno do subgroup
        subgroup_widths.append(sg_w)
        
    total_subgroups_w = sum(subgroup_widths) + subgroup_gap * (len(subgroups) - 1)
    start_sub_x = (canvas_w - total_subgroups_w) // 2
    
    current_sx = start_sub_x
    for i, (label, fill_col, blocks, block_fill) in enumerate(subgroups):
        sg_w = subgroup_widths[i]
        total_group_blocks_w, block_widths = subgroup_block_widths[i]
        
        draw.rounded_rectangle([current_sx, current_y + 110, current_sx+sg_w, current_y + 110 + subgroup_h], radius=10, fill=fill_col, outline="#BBB")
        draw_text_centered(draw, (current_sx + sg_w//2, current_y + 130), label, font_header)
        
        start_block_x = current_sx + (sg_w - total_group_blocks_w) // 2
        current_block_x = start_block_x
        block_height = 50 # Aumentado de 40
        
        for j, b_label in enumerate(blocks):
            b_w = block_widths[j]
            # Helper function para desenhar os blocos coloridos maiores
            bx = current_block_x
            by = current_y + 160 # Baixado um pouco
            draw.rounded_rectangle([bx, by, bx+b_w, by+block_height], radius=3, fill=block_fill, outline="#666", width=1)
            draw_text_centered(draw, (bx + b_w//2, by + block_height//2), b_label, font_formula)
            
            current_block_x += b_w + block_gap
            
        current_sx += sg_w + subgroup_gap
            
    # Total count movido mais para baixo para não sobrepor
    draw_text_centered(draw, (canvas_w//2, current_y + 320), "Total: 14 atributos", font_header)
    draw_arrow(draw, (canvas_w//2, current_y + section_h + 10))
    current_y += section_h + gap_between_sections

    # --- SEÇÃO 4: VETOR DE CARACTERÍSTICAS ---
    # CORREÇÃO: AUMENTADO TAMANHO DOS BLOCOS DO VETOR
    section_h = 240 # Aumentado
    draw.rounded_rectangle([20, current_y, canvas_w-20, current_y+section_h], radius=20, fill="#FFF8E1", outline="#FFE082")
    draw_text_centered(draw, (canvas_w//2, current_y + 30), "4. Vetor de características de cada sub-bloco", font_header, fill="black")
    
    vector_box_y = current_y + 80
    vector_box_h = 70 # Aumentado
    vector_box_gap = 10 # Aumentado
    block_height_s4 = 55 # Aumentado de 45
    
    # Centralizar e alinhar vetor dinamicamente
    labels_14 = [
        "R", "G", "B", 
        "H", "S", "V", 
        "L_{cv2}", "a_{cv2}", "b_{cv2}",
        "RG", "RB", "GB", "DifLV", "SomaRGB"
    ]
    
    block_fills = [
        ("#A9CCE3", 3), # RGB
        ("#C9E2B3", 3), # HSV
        ("#D9C9EB", 3), # CIELAB
        ("#C5E0B4", 5)  # Derivados
    ]
    
    blocks_info = []
    total_vector_w = 0
    k = 0
    for fill_col, count in block_fills:
        for _ in range(count):
            label = labels_14[k]
            # Calcular largura do texto
            try:
                txt_w = draw.textsize(label, font=font_formula)[0]
            except AttributeError:
                bbox_txt = draw.textbbox((0, 0), label, font=font_formula)
                txt_w = bbox_txt[2] - bbox_txt[0]
            
            block_w = max(60, txt_w + 16)
            blocks_info.append((label, fill_col, block_w))
            total_vector_w += block_w + vector_box_gap
            k += 1
            
    total_vector_w -= vector_box_gap
    label_w = 120
    start_x = (canvas_w - (label_w + total_vector_w)) // 2
    
    # Legenda "Vetor X_k:"
    draw_text_centered(draw, (start_x + label_w // 2, vector_box_y + vector_box_h // 2), "Vetor X_k:", font_header)
    
    current_x = start_x + label_w
    for label, fill_col, block_w in blocks_info:
        block_pos = (current_x, vector_box_y + (vector_box_h - block_height_s4) // 2)
        block_size_dynamic = (block_w, block_height_s4)
        draw_colorful_block(draw, block_pos, block_size_dynamic, label, fill_col, font_formula)
        current_x += block_w + vector_box_gap
            
    # Legenda "14 atributos" centralizada abaixo do vetor
    draw_text_centered(draw, (start_x + label_w + total_vector_w // 2, vector_box_y + vector_box_h + 40), "14 atributos", font_header)

    # Salvar resultado
    final_img.save(output_path, quality=95)
    print(f"Diagrama gerado com sucesso em: '{output_path}'")


# --- Execução ---
# Substitua pelo caminho real da sua imagem
imagem_de_entrada = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Dataset_RL/pelo/pelo 2418.3.jpg' 
imagem_de_saida = 'diagrama_extracao_atributos.png'

generate_diagram(imagem_de_entrada, imagem_de_saida)