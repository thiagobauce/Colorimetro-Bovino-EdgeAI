import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

# --- Configurações e Fontes ---
def get_font(size, bold=False):
    """Tenta carregar uma fonte padrão com acentos. Fallback para fonte padrão se não encontrada."""
    font_paths = [
        # Windows
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        # Mac/Linux (alternativas comuns)
        "Arial Bold.ttf" if bold else "Arial.ttf",
        "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except IOError:
            continue
    print(f"AVISO: Nenhuma fonte padrão encontrada para tamanho {size}. Usando fonte básica.")
    return ImageFont.load_default()

def draw_text_centered(draw, pos, text, font, fill="black"):
    """Desenha um texto centralizado em uma determinada posição."""
    x, y = pos
    try:
        # Pillow moderno (>= 9.2.0)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback Pillow antigo (< 9.2.0)
        w, h = draw.textsize(text, font=font)
    
    draw.text((x - w / 2, y - h / 2), text, font=font, fill=fill, align="center")

def create_color_channel_image(channel_data, color_map, size):
    """Cria uma versão colorida isolada de um canal de cor de entrada."""
    channel_resized = Image.fromarray(channel_data).resize((size, size)).convert('L')
    zero = Image.new('L', channel_resized.size)
    if color_map == 'R': # Vermelho isolado
        return Image.merge('RGB', (channel_resized, zero, zero))
    elif color_map == 'G': # Verde isolado
        return Image.merge('RGB', (zero, channel_resized, zero))
    elif color_map == 'B': # Azul isolado
        return Image.merge('RGB', (zero, zero, channel_resized))
    return Image.merge('RGB', (channel_resized, channel_resized, channel_resized))

def create_cielab_output_images(rgb_image, size):
    """Converte RGB para CIELAB usando OpenCV e isola L*, a*, b* com visualizações intuitivas."""
    # Converter Pillow para Numpy e RGB para OpenCV BGR
    img_bgr = cv2.cvtColor(np.array(rgb_image.convert('RGB')), cv2.COLOR_RGB2BGR)
    
    # Transformação: RGB -> XYZ -> CIELAB (OpenCV cvtColor)
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    
    # Isolar canais L*, a*, b*
    l, a, b = cv2.split(img_lab)
    
    # Pegar as dimensões originais da imagem de entrada (ex: 220x220)
    h, w = l.shape
    
    # 1. L* (Luminosidade) - Exibido como escala de cinza
    l_display = Image.fromarray(l).resize((size, size)).convert('L')
    
    # 2. a* (Verde-Vermelho) - Visualização intuitiva
    # Cria a matriz com (h, w) em vez de (size, size)
    a_display_np = np.zeros((h, w, 3), dtype=np.uint8)
    a_display_np[:,:,1] = (255 - a_np_map(a)).astype(np.uint8) # G para verde
    a_display_np[:,:,0] = a_np_map(a).astype(np.uint8) # R para vermelho
    a_display_np[:,:,2] = 0 # B
    a_display_color = Image.fromarray(a_display_np, 'RGB')
    
    # 3. b* (Azul-Amarelo) - Visualização intuitiva
    b_display_np = np.zeros((h, w, 3), dtype=np.uint8)
    b_display_np[:,:,0] = b_np_map(b).astype(np.uint8) # R
    b_display_np[:,:,1] = b_np_map(b).astype(np.uint8) # G
    b_display_np[:,:,2] = (255 - b_np_map(b)).astype(np.uint8) # B
    b_display_color = Image.fromarray(b_display_np, 'RGB')

    # Redimensionar para o tamanho final exigido pelo painel (ch_size)
    a_display = a_display_color.resize((size, size))
    b_display = b_display_color.resize((size, size))
    
    return l_display, a_display, b_display

# Funções auxiliares de mapeamento para visualização intuitiva de a* e b*
def a_np_map(a_chan):
    # Valores < 128 (verde) mapeiam para 0-128; >128 (vermelho) mapeiam para 128-255
    return ((a_chan - 128) * 2 + 128).clip(0, 255)

def b_np_map(b_chan):
    # Valores < 128 (azul) mapeiam para 0-128; >128 (amarelo) mapeiam para 128-255
    return ((b_chan - 128) * 2 + 128).clip(0, 255)

def create_scale_bars(width, height, scale_type):
    """Cria as barras de escala para L*, a*, b* com gradientes corretos."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    if scale_type == 'L': # Escala de cinza 0 a 100
        for x in range(width):
            t = x / (width - 1)
            v = int(t * 255)
            draw.line([(x, 0), (x, height)], fill=(v, v, v))
    elif scale_type == 'a': # Verde(-) a Vermelho(+) via Cinza
        for x in range(width):
            t = x / (width - 1)
            if t < 0.5:
                # Verde (0,128,0) para Cinza (128,128,128)
                t2 = t * 2
                r = b = int(128 * t2)
                g = 128
            else:
                # Cinza (128,128,128) para Vermelho (255,0,0)
                t2 = (t - 0.5) * 2
                r = int(128 + 127 * t2)
                g = b = int(128 - 128 * t2)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))
    elif scale_type == 'b': # Azul(-) a Amarelo(+) via Cinza
        for x in range(width):
            t = x / (width - 1)
            if t < 0.5:
                # Azul (0,0,255) para Cinza (128,128,128)
                t2 = t * 2
                r = g = int(128 * t2)
                b = int(255 - 127 * t2)
            else:
                # Cinza (128,128,128) para Amarelo (255,255,0)
                t2 = (t - 0.5) * 2
                r = g = int(128 + 127 * t2)
                b = int(128 - 128 * t2)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))
            
    return img

def draw_arrow(draw, x, y, direction='down'):
    """Desenha a setinha de transição."""
    if direction == 'down':
        draw.polygon([(x-10, y), (x+10, y), (x+10, y+20), (x+20, y+20), (x, y+40), (x-20, y+20), (x-10, y+20)], fill="#1B365D")

def generate_conversion_diagram(input_path, output_path="diagrama_conversao_pele_escura.jpg"):
    if not os.path.exists(input_path):
        print(f"ERRO: Arquivo '{input_path}' não encontrado.")
        return
        
    original_img = Image.open(input_path).convert('RGB')
    
    # --- CORREÇÃO: Configurações de layout aumentadas ---
    canvas_w = 1100 # Aumentado de 900
    canvas_h = 1300 # Aumentado de 1000
    bg_color = (255, 255, 255)
    
    # Criar canvas final
    final_img = Image.new('RGB', (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(final_img)
    
    # Fontes
    font_title = get_font(24, bold=True)
    font_header = get_font(20, bold=True)
    font_sub_title = get_font(18)
    font_scale = get_font(16)
    
    # --- PARTE 1: IMAGEM RGB (sub-bloco) ---
    box_y = 60 # Mover para baixo
    box_h = 320 # Aumentado
    draw.rounded_rectangle([20, box_y, canvas_w-20, box_y+box_h], radius=20, fill="#F0F8FF", outline="#D0E0F0")
    
    # Título Principal
    draw_text_centered(draw, (canvas_w//2, box_y + 40), "Imagem RGB (sub-bloco)", font_title, fill="black")
    
    # Inserir imagens de entrada
    input_size = 220
    ch_size = 200
    gap = 40 # Gap horizontal entre a primeira imagem e as outras
    ch_gap = 80 # Gap horizontal maior entre os canais
    
    # Centralizar o bloco inteiro
    start_x_input = (canvas_w - (input_size + gap + ch_size*3 + ch_gap*2)) // 2
    
    input_cropped = original_img.resize((input_size, input_size))
    final_img.paste(input_cropped, (start_x_input, box_y + 100))
    
    img_np = np.array(original_img)
    r_chan = create_color_channel_image(img_np[:,:,0], 'R', ch_size)
    g_chan = create_color_channel_image(img_np[:,:,1], 'G', ch_size)
    b_chan = create_color_channel_image(img_np[:,:,2], 'B', ch_size)
    
    ch_start_x_R = start_x_input + input_size + gap
    
    final_img.paste(r_chan, (ch_start_x_R, box_y + 100))
    final_img.paste(g_chan, (ch_start_x_R + ch_size + ch_gap, box_y + 100))
    final_img.paste(b_chan, (ch_start_x_R + (ch_size + ch_gap)*2, box_y + 100))
    
    # Rótulos RGB
    draw_text_centered(draw, (ch_start_x_R + ch_size//2, box_y + 80), "R", font_header)
    draw_text_centered(draw, (ch_start_x_R + ch_size + ch_gap + ch_size//2, box_y + 80), "G", font_header)
    draw_text_centered(draw, (ch_start_x_R + (ch_size + ch_gap)*2 + ch_size//2, box_y + 80), "B", font_header)
    
    draw_arrow(draw, canvas_w//2, box_y + box_h + 10)

    # --- PARTE 2: CONVERSÃO OPENCV ---
    conv_box_y = box_y + box_h + 60
    conv_box_h = 220 # Aumentado de 160
    draw.rounded_rectangle([20, conv_box_y, canvas_w-20, conv_box_y+conv_box_h], radius=20, fill="#F0FFF0", outline="#D0F0D0")
    draw_text_centered(draw, (canvas_w//2, conv_box_y + 40), "Conversão OpenCV", font_title, fill="black")
    
    box_w_small = 160
    box_h_small = 60
    box_gap_conv = 140
    
    # Centralizar o bloco de caixas
    start_x_conv = (canvas_w - (box_w_small*3 + box_gap_conv*2)) // 2
    
    box_rgb = [start_x_conv, conv_box_y + 80, start_x_conv+box_w_small, conv_box_y+80+box_h_small]
    draw.rounded_rectangle(box_rgb, radius=10, fill="#FFE0B2", outline="#FFCC80")
    draw_text_centered(draw, ((box_rgb[0]+box_rgb[2])//2, (box_rgb[1]+box_rgb[3])//2), "RGB", font_header)
    
    # Seta
    draw.line([(box_rgb[2]+10, (box_rgb[1]+box_rgb[3])//2), (box_rgb[2]+box_gap_conv-10, (box_rgb[1]+box_rgb[3])//2)], fill="black", width=2)
    
    box_xyz = [start_x_conv + box_w_small + box_gap_conv, conv_box_y + 80, start_x_conv + box_w_small*2 + box_gap_conv, conv_box_y+80+box_h_small]
    draw.rounded_rectangle(box_xyz, radius=10, fill="#FFE0B2", outline="#FFCC80")
    draw_text_centered(draw, ((box_xyz[0]+box_xyz[2])//2, (box_xyz[1]+box_xyz[3])//2), "XYZ", font_header)
    
    # Seta
    draw.line([(box_xyz[2]+10, (box_xyz[1]+box_xyz[3])//2), (box_xyz[2]+box_gap_conv-10, (box_xyz[1]+box_xyz[3])//2)], fill="black", width=2)
    
    box_cielab = [canvas_w - start_x_conv - box_w_small, conv_box_y + 80, canvas_w - start_x_conv, conv_box_y+80+box_h_small]
    draw.rounded_rectangle(box_cielab, radius=10, fill="#FFE0B2", outline="#FFCC80")
    draw_text_centered(draw, ((box_cielab[0]+box_cielab[2])//2, (box_cielab[1]+box_cielab[3])//2), "CIELAB", font_header)
    
    # Texto descritivo centralizado e mais baixo
    draw_text_centered(draw, (canvas_w//2, conv_box_y + 170), "Transformação: RGB → XYZ → CIELAB\n(OpenCV cvtColor)", font_sub_title, fill="black")
    
    draw_arrow(draw, canvas_w//2, conv_box_y + conv_box_h + 10)

    # --- PARTE 3: SAÍDA CIELAB (OpenCV) ---
    out_box_y = conv_box_y + conv_box_h + 60
    out_box_h = 480 # Aumentado
    draw.rounded_rectangle([20, out_box_y, canvas_w-20, out_box_y+out_box_h], radius=20, fill="#E6E6FA", outline="#D0D0F0")
    draw_text_centered(draw, (canvas_w//2, out_box_y + 40), "Saída: Componentes CIELAB (OpenCV)", font_title, fill="black")
    
    # Gerar saídas CIELAB
    l_out, a_out, b_out = create_cielab_output_images(input_cropped, ch_size)
    
    # Centralizar as três imagens inferiores com um gap maior
    start_x_ch_out = (canvas_w - (ch_size*3 + ch_gap*2)) // 2
    
    final_img.paste(l_out, (start_x_ch_out, out_box_y + 120))
    final_img.paste(a_out, (start_x_ch_out + ch_size + ch_gap, out_box_y + 120))
    final_img.paste(b_out, (start_x_ch_out + (ch_size + ch_gap)*2, out_box_y + 120))
    
    # Rótulos Saída
    draw_text_centered(draw, (start_x_ch_out + ch_size//2, out_box_y + 100), "Lcv2 (Luminosidade)", font_sub_title)
    draw_text_centered(draw, (start_x_ch_out + ch_size + ch_gap + ch_size//2, out_box_y + 100), "acv2 (Verde-Vermelho)", font_sub_title)
    draw_text_centered(draw, (start_x_ch_out + (ch_size + ch_gap)*2 + ch_size//2, out_box_y + 100), "bcv2 (Azul-Amarelo)", font_sub_title)
    
    # Barras de escala
    scale_w = 230
    scale_h = 25
    scale_y = out_box_y + 360 # Mover para baixo
    
    # Usando centralização dinâmica para cada escala e texto
    # Escala Lcv2
    l_start = start_x_ch_out + (ch_size - scale_w)//2
    final_img.paste(create_scale_bars(scale_w, scale_h, 'L'), (l_start, scale_y))
    
    # Escala acv2
    a_start = start_x_ch_out + ch_size + ch_gap + (ch_size - scale_w)//2
    final_img.paste(create_scale_bars(scale_w, scale_h, 'a'), (a_start, scale_y))
    
    # Escala bcv2
    b_start = start_x_ch_out + (ch_size + ch_gap)*2 + (ch_size - scale_w)//2
    final_img.paste(create_scale_bars(scale_w, scale_h, 'b'), (b_start, scale_y))
    
    # --- CORREÇÃO DE SOBREPOSIÇÃO DE TEXTO ---
    # Usando centralização dinâmica para cada texto e maior espaçamento
    text_y_offset = scale_y + 45 
    
    # Rótulos Lcv2
    draw_text_centered(draw, (l_start, text_y_offset), "0", font_scale)
    draw_text_centered(draw, (l_start + scale_w, text_y_offset), "100", font_scale)
    
    # Rótulos acv2
    draw_text_centered(draw, (a_start, text_y_offset), "-128", font_scale)
    draw_text_centered(draw, (a_start + scale_w//2, text_y_offset), "0", font_scale)
    draw_text_centered(draw, (a_start + scale_w, text_y_offset), "+127", font_scale)
    
    # Rótulos bcv2
    draw_text_centered(draw, (b_start, text_y_offset), "-128", font_scale)
    draw_text_centered(draw, (b_start + scale_w//2, text_y_offset), "0", font_scale)
    draw_text_centered(draw, (b_start + scale_w, text_y_offset), "+127", font_scale)

    # Salvar resultado
    final_img.save(output_path, quality=95)
    print(f"Diagrama gerado com sucesso em: '{output_path}'")

# --- Execução ---
# Substitua pelo caminho real da sua imagem.
generate_conversion_diagram('/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Dataset_RL/pelo/2352 PELO.jpg')