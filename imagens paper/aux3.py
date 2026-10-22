import os
import colorsys
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    """Busca uma fonte com suporte a acentos compatível com Windows, Mac ou Linux."""
    # Lista de fontes comuns em diferentes sistemas operacionais
    font_list = [
        "arialbd.ttf" if bold else "arial.ttf",                   # Windows
        "Arial Bold.ttf" if bold else "Arial.ttf",                # Mac
        "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf", # Linux
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"       # Linux alternativo
    ]
    
    for font_name in font_list:
        try:
            return ImageFont.truetype(font_name, size)
        except IOError:
            continue
            
    print("AVISO: Nenhuma fonte padrão com acentos encontrada. O texto pode bugar.")
    return ImageFont.load_default()

def draw_text_centered(draw, pos, text, font, fill="black"):
    """Desenha um texto centralizado em uma determinada posição."""
    x, y = pos
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text((x - w / 2, y - h / 2), text, font=font, fill=fill, align="center")
    except AttributeError:
        draw.text((x - 50, y - 10), text, font=font, fill=fill)

def create_gradient_bar(width, height, color_type):
    """Cria as barras de gradiente para HSV e CIELAB."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for x in range(width):
        t = x / (width - 1)
        
        if color_type == 'H': # Matiz (Arco-íris)
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(t, 1.0, 1.0)]
        elif color_type == 'S': # Saturação (Cinza para Verde)
            r, g, b = int(128 * (1-t)), int(128 * (1-t) + 128 * t * 1.5), int(128 * (1-t))
            g = min(255, g)
        elif color_type == 'V' or color_type == 'L': # Luminosidade/Valor (Preto para Branco)
            r = g = b = int(t * 255)
        elif color_type == 'a': # Verde (-) para Vermelho (+) via Cinza
            if t < 0.5:
                # Verde (0,128,0) para Cinza (128,128,128)
                t2 = t * 2
                r = b = int(0 + 128 * t2)
                g = 128
            else:
                # Cinza (128,128,128) para Vermelho (255,0,0)
                t2 = (t - 0.5) * 2
                r = int(128 + 127 * t2)
                g = b = int(128 - 128 * t2)
        elif color_type == 'b': # Azul (-) para Amarelo (+) via Cinza
            if t < 0.5:
                # Azul (0,0,255) para Cinza (128,128,128)
                t2 = t * 2
                r = g = int(0 + 128 * t2)
                b = int(255 - 127 * t2)
            else:
                # Cinza (128,128,128) para Amarelo (255,255,0)
                t2 = (t - 0.5) * 2
                r = g = int(128 + 127 * t2)
                b = int(128 - 128 * t2)
        else:
            r = g = b = 255
            
        draw.line([(x, 0), (x, height)], fill=(r, g, b))
        
    return img

def create_rgb_channels(image, size):
    """Extrai os canais R, G e B de uma imagem e retorna 3 imagens coloridas isoladas."""
    img_resized = image.resize((size, size)).convert('RGB')
    r, g, b = img_resized.split()
    zero = Image.new('L', img_resized.size)
    
    img_r = Image.merge('RGB', (r, zero, zero))
    img_g = Image.merge('RGB', (zero, g, zero))
    img_b = Image.merge('RGB', (zero, zero, b))
    
    return img_r, img_g, img_b

def draw_arrow(draw, x, y):
    """Desenha a setinha de transição entre os painéis."""
    draw.polygon([(x, y-10), (x+15, y-10), (x+15, y-20), (x+30, y), (x+15, y+20), (x+15, y+10), (x, y+10)], fill="#4A4A4A")

def generate_color_spaces_diagram(input_path, output_path="diagrama_cores.jpg"):
    if not os.path.exists(input_path):
        print(f"ERRO: Arquivo '{input_path}' não encontrado.")
        return
        
    base_img = Image.open(input_path)
    
    # Configurações de layout
    canvas_w = 1200
    canvas_h = 750
    bg_color = (255, 255, 255)
    
    # Criar o canvas final
    final_img = Image.new('RGB', (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(final_img)
    
    # Fontes atualizadas para garantir os acentos
    font_title = get_font(24, bold=True)
    font_header = get_font(20, bold=True)
    font_sub = get_font(14)
    font_text = get_font(13)
    
    # Título Principal
    draw_text_centered(draw, (canvas_w//2, 50), "Representação cromática nos diferentes espaços de cor", font_title)
    
    # --- PARTE 1: IMAGEM ORIGINAL ---
    img_size = 140
    input_cropped = base_img.resize((img_size, img_size))
    final_img.paste(input_cropped, (40, 300))
    draw.rectangle([39, 299, 40+img_size, 300+img_size], outline="#CCCCCC", width=2)
    draw_text_centered(draw, (40 + img_size//2, 470), "Sub-bloco\nda imagem", font_sub)
    
    draw_arrow(draw, 195, 370)
    
    # --- PARTE 2: RGB ---
    box_w = 280
    box_h = 420
    box_x = 240
    box_y = 200
    
    # Textos de Cabeçalho RGB
    draw_text_centered(draw, (box_x + box_w//2, 130), "RGB", font_header, fill="#1B365D")
    draw_text_centered(draw, (box_x + box_w//2, 155), "(Canais de cor)", font_sub)
    
    # Caixa principal RGB
    draw.rounded_rectangle([box_x, box_y, box_x+box_w, box_y+box_h], radius=15, outline="#4A86E8", width=2)
    
    # Extrair e colar canais R, G, B
    ch_size = 75
    img_r, img_g, img_b = create_rgb_channels(base_img, ch_size)
    gap = 15
    start_ch_x = box_x + (box_w - (ch_size*3 + gap*2)) // 2
    
    final_img.paste(img_r, (start_ch_x, box_y + 60))
    final_img.paste(img_g, (start_ch_x + ch_size + gap, box_y + 60))
    final_img.paste(img_b, (start_ch_x + ch_size*2 + gap*2, box_y + 60))
    
    draw_text_centered(draw, (start_ch_x + ch_size//2, box_y + 40), "R", font_header)
    draw_text_centered(draw, (start_ch_x + ch_size + gap + ch_size//2, box_y + 40), "G", font_header)
    draw_text_centered(draw, (start_ch_x + ch_size*2 + gap*2 + ch_size//2, box_y + 40), "B", font_header)
    
    # Caixa de texto descritivo RGB
    txt_box_y = box_y + 250
    draw.rounded_rectangle([box_x+15, txt_box_y, box_x+box_w-15, txt_box_y+150], radius=10, fill="#F0F4FA", outline="#D0E0F0")
    texto_rgb = "Representação da cor\nbaseada na intensidade dos\ncanais vermelho (R),\nverde (G) e azul (B)\nregistrados pelo sensor\nda câmera."
    draw_text_centered(draw, (box_x + box_w//2, txt_box_y + 75), texto_rgb, font_text)

    draw_arrow(draw, box_x + box_w + 10, 370)

    # --- PARTE 3: HSV ---
    box_x = 570
    draw_text_centered(draw, (box_x + box_w//2, 130), "HSV", font_header, fill="#27702B")
    draw_text_centered(draw, (box_x + box_w//2, 165), "(Tonalidade, Saturação\ne Intensidade)", font_sub)
    
    draw.rounded_rectangle([box_x, box_y, box_x+box_w, box_y+box_h - 60], radius=15, outline="#6AA84F", width=2)
    
    bar_w = 240
    bar_h = 25
    bar_start_x = box_x + 20
    
    # Gradiente H
    grad_y = box_y + 50
    draw.text((bar_start_x, grad_y - 25), "H – Tonalidade (Hue)", fill="black", font=font_sub)
    final_img.paste(create_gradient_bar(bar_w, bar_h, 'H'), (bar_start_x, grad_y))
    draw.text((bar_start_x, grad_y + bar_h + 5), "0°", fill="black", font=font_sub)
    draw.text((bar_start_x + bar_w - 30, grad_y + bar_h + 5), "360°", fill="black", font=font_sub)
    
    # Gradiente S
    grad_y += 90
    draw.text((bar_start_x, grad_y - 25), "S – Saturação (Saturation)", fill="black", font=font_sub)
    final_img.paste(create_gradient_bar(bar_w, bar_h, 'S'), (bar_start_x, grad_y))
    draw.text((bar_start_x, grad_y + bar_h + 5), "0", fill="black", font=font_sub)
    draw.text((bar_start_x + bar_w - 10, grad_y + bar_h + 5), "1", fill="black", font=font_sub)
    
    # Gradiente V
    grad_y += 90
    draw.text((bar_start_x, grad_y - 25), "V – Intensidade (Value)", fill="black", font=font_sub)
    final_img.paste(create_gradient_bar(bar_w, bar_h, 'V'), (bar_start_x, grad_y))
    draw.text((bar_start_x, grad_y + bar_h + 5), "0", fill="black", font=font_sub)
    draw.text((bar_start_x + bar_w - 10, grad_y + bar_h + 5), "1", fill="black", font=font_sub)
    
    # Caixa descritiva HSV
    draw.rounded_rectangle([box_x, box_y+box_h - 40, box_x+box_w, box_y+box_h + 60], radius=10, fill="#EBF4E5", outline="#C9E2B3")
    texto_hsv = "Separa a informação de cor\nem tonalidade (H), saturação\n(S) e intensidade luminosa (V)."
    draw_text_centered(draw, (box_x + box_w//2, box_y+box_h + 10), texto_hsv, font_text)

    draw_arrow(draw, box_x + box_w + 10, 370)

    # --- PARTE 4: CIELAB ---
    box_x = 900
    draw_text_centered(draw, (box_x + box_w//2, 130), "CIELAB", font_header, fill="#4B2C83")
    draw_text_centered(draw, (box_x + box_w//2, 155), "(Perceptualmente uniforme)", font_sub)
    
    draw.rounded_rectangle([box_x, box_y, box_x+box_w, box_y+box_h - 60], radius=15, outline="#8E7CC3", width=2)
    
    bar_start_x = box_x + 20
    
    # Gradiente L*
    grad_y = box_y + 50
    draw.text((bar_start_x, grad_y - 25), "L* – Luminosidade", fill="black", font=font_sub)
    final_img.paste(create_gradient_bar(bar_w, bar_h, 'L'), (bar_start_x, grad_y))
    draw.rectangle([bar_start_x, grad_y, bar_start_x+bar_w, grad_y+bar_h], outline="gray")
    draw.text((bar_start_x, grad_y + bar_h + 5), "0", fill="black", font=font_sub)
    draw.text((bar_start_x + bar_w - 25, grad_y + bar_h + 5), "100", fill="black", font=font_sub)
    
    # Gradiente a*
    grad_y += 90
    draw.text((bar_start_x, grad_y - 25), "a* – Verde (-) a Vermelho (+)", fill="black", font=font_sub)
    final_img.paste(create_gradient_bar(bar_w, bar_h, 'a'), (bar_start_x, grad_y))
    draw.text((bar_start_x, grad_y + bar_h + 5), "-128", fill="black", font=font_sub)
    draw_text_centered(draw, (bar_start_x + bar_w//2, grad_y + bar_h + 12), "0", font_sub)
    draw.text((bar_start_x + bar_w - 30, grad_y + bar_h + 5), "+127", fill="black", font=font_sub)
    
    # Gradiente b*
    grad_y += 90
    draw.text((bar_start_x, grad_y - 25), "b* – Azul (-) a Amarelo (+)", fill="black", font=font_sub)
    final_img.paste(create_gradient_bar(bar_w, bar_h, 'b'), (bar_start_x, grad_y))
    draw.text((bar_start_x, grad_y + bar_h + 5), "-128", fill="black", font=font_sub)
    draw_text_centered(draw, (bar_start_x + bar_w//2, grad_y + bar_h + 12), "0", font_sub)
    draw.text((bar_start_x + bar_w - 30, grad_y + bar_h + 5), "+127", fill="black", font=font_sub)
    
    # Caixa descritiva CIELAB
    draw.rounded_rectangle([box_x, box_y+box_h - 40, box_x+box_w, box_y+box_h + 60], radius=10, fill="#EFE8F6", outline="#D9C9EB")
    texto_lab = "Representação perceptualmente\nuniforme da cor, com luminosidade (L*)\ne os eixos de cor a* (verde–vermelho)\ne b* (azul–amarelo)."
    draw_text_centered(draw, (box_x + box_w//2, box_y+box_h + 10), texto_lab, font_text)

    # Salvar a imagem final
    final_img.save(output_path, quality=95)
    print(f"SUCESSO! O diagrama foi salvo como: '{output_path}'")

# ==============================================================================
# EXECUÇÃO DO SCRIPT
# ==============================================================================
if __name__ == "__main__":
    # ---> COLOQUE O NOME DA SUA IMAGEM AQUI <---
    # A imagem original ("Sub-bloco da imagem") que será lida
    imagem_de_entrada = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Dataset_RL/pelo/2341.1 pelo.jpg' 
    
    # Nome do arquivo de saída
    imagem_de_saida = 'diagrama_espacos_cor.jpg'
    
    generate_color_spaces_diagram(imagem_de_entrada, imagem_de_saida)