import os
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# CONFIGURAÇÃO DOS CAMINHOS DAS FOTOS
# Substitua os caminhos abaixo pelos locais reais das fotos que você fez upload.
# ==============================================================================
FOTO_DISPOSITIVO = "/home/workstation_2x_3080/Documents/WhatsApp Image 2026-07-26 at 19.37.01.jpeg"       # Foto do cilindro azul sozinho (impressão 3D)
FOTO_SMARTPHONE = "/home/workstation_2x_3080/Documents/WhatsApp Image 2026-07-26 at 19.36.08.jpeg"        # Foto capturando com o smartphone no curral
FOTO_COLORIMETRO = "/home/workstation_2x_3080/Documents/WhatsApp Image 2026-07-26 at 19.38.02.jpeg"       # Foto da medição com o colorímetro

NOME_ARQUIVO_SAIDA = "diagrama_aquisicao_dados.png"

def get_font(size, bold=False):
    font_paths = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
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
    return ImageFont.load_default()

def draw_text_centered(draw, pos, text, font, fill="black"):
    x, y = pos
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except AttributeError:
        try:
            w, h = draw.textsize(text, font=font)
        except AttributeError:
            w, h = 80, 16
    draw.text((x - w / 2, y - h / 2), text, font=font, fill=fill, align="center")

def draw_text_multiline_centered(draw, pos, text, font, fill="black", line_spacing=5):
    x, y = pos
    lines = text.split('\n')
    
    total_h = 0
    line_heights = []
    for line in lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]
        except:
            h = 16
        line_heights.append(h)
        total_h += h + line_spacing
    total_h -= line_spacing
    
    current_y = y - total_h / 2
    for i, line in enumerate(lines):
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
        except:
            w = 80
        draw.text((x - w / 2, current_y), line, font=font, fill=fill)
        current_y += line_heights[i] + line_spacing

def add_rounded_image(canvas, img_path, pos, size, radius):
    """Carrega uma imagem, faz um crop centralizado proporcional, arredonda os cantos e cola no canvas."""
    try:
        img = Image.open(img_path).convert("RGB")
    except Exception as e:
        print(f"Aviso: Não foi possível carregar '{img_path}'. Usando espaço reservado (placeholder).")
        img = Image.new("RGB", size, (220, 220, 220))
        d = ImageDraw.Draw(img)
        d.line((0,0) + size, fill=(150,150,150), width=3)
        d.line((0,size[1], size[0],0), fill=(150,150,150), width=3)
        draw_text_centered(d, (size[0]//2, size[1]//2), "Sem Imagem", get_font(18, True), fill="#666")
    
    target_ratio = size[0] / size[1]
    img_ratio = img.width / img.height
    
    if img_ratio > target_ratio:
        new_w = int(img.height * target_ratio)
        offset = (img.width - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, img.height))
    else:
        new_h = int(img.width / target_ratio)
        offset = (img.height - new_h) // 2
        img = img.crop((0, offset, img.width, offset + new_h))
        
    img = img.resize(size, Image.Resampling.LANCZOS)
    
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    
    canvas.paste(img, pos, mask)

def draw_arrow_right(draw, start_pos, fill="#1B365D", length=40):
    x, y = start_pos
    draw.polygon([
        (x, y-8), 
        (x+length-15, y-8), 
        (x+length-15, y-18), 
        (x+length, y), 
        (x+length-15, y+18), 
        (x+length-15, y+8), 
        (x, y+8)
    ], fill=fill)

def generate_diagram(output_path="diagrama_aquisicao_dados.png"):
    canvas_w = 1350
    canvas_h = 750
    bg_color = (255, 255, 255)
    img = Image.new('RGB', (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(img)

    font_title = get_font(34, bold=True)
    font_header = get_font(22, bold=True)
    font_desc = get_font(19)

    # Título Principal
    draw_text_centered(draw, (canvas_w//2, 60), "ETAPA DE AQUISIÇÃO DE DADOS EM CAMPO", font_title, fill="#1B365D")
    draw.line([100, 110, canvas_w-100, 110], fill="#D0E0F0", width=4)

    # Configuração dos 3 painéis
    panel_w = 360
    panel_h = 560
    gap = 70
    start_x = (canvas_w - (3 * panel_w + 2 * gap)) // 2
    y_panel = 150
    
    panels = [
        {
            "title": "1. Dispositivo Projetado",
            "img": FOTO_DISPOSITIVO,
            "desc": "Estrutura cilíndrica impressa em\n3D para isolamento luminoso e\npadronização da distância focal.",
            "color": "#F0F5FA",
            "outline": "#4C73A6",
            "title_color": "#1B365D"
        },
        {
            "title": "2. Captura de Imagens",
            "img": FOTO_SMARTPHONE,
            "desc": "Aquisição fotográfica da pele\nou pelo no curral utilizando\no dispositivo acoplado ao smartphone.",
            "color": "#F2F9F2",
            "outline": "#5C8A5C",
            "title_color": "#1F4D1F"
        },
        {
            "title": "3. Padrão-Ouro",
            "img": FOTO_COLORIMETRO,
            "desc": "Obtenção das coordenadas\nCIELAB de referência através de\nequipamento colorímetro portátil.",
            "color": "#FFF8EB",
            "outline": "#D9B36C",
            "title_color": "#7A5C29"
        }
    ]

    for i, p in enumerate(panels):
        px = start_x + i * (panel_w + gap)
        
        # Fundo do Painel
        draw.rounded_rectangle([px, y_panel, px+panel_w, y_panel+panel_h], radius=20, fill=p["color"], outline=p["outline"], width=3)
        
        # Cabeçalho do Painel (cor sólida)
        draw.rounded_rectangle([px, y_panel, px+panel_w, y_panel+70], radius=20, fill=p["outline"])
        draw.rectangle([px, y_panel+35, px+panel_w, y_panel+70], fill=p["outline"]) # Arrumar cantos inferiores
        draw.line([px, y_panel+70, px+panel_w, y_panel+70], fill=p["outline"], width=3)
        
        # Texto do Cabeçalho
        draw_text_centered(draw, (px + panel_w//2, y_panel + 35), p["title"], font_header, fill="white")
        
        # Imagem
        img_size = (300, 320)
        img_x = px + (panel_w - img_size[0]) // 2
        img_y = y_panel + 100
        
        add_rounded_image(img, p["img"], (img_x, img_y), img_size, 15)
        
        # Borda da Imagem
        draw.rounded_rectangle([img_x, img_y, img_x+img_size[0], img_y+img_size[1]], radius=15, outline="#888", width=2)
        
        # Descrição
        desc_y = img_y + img_size[1] + 65
        draw_text_multiline_centered(draw, (px + panel_w//2, desc_y), p["desc"], font_desc, fill="#333", line_spacing=10)

        # Setas conectando os painéis
        if i < 2:
            arrow_x = px + panel_w + (gap - 50) // 2
            arrow_y = y_panel + panel_h // 2
            draw_arrow_right(draw, (arrow_x, arrow_y), fill="#A0A0A0", length=50)

    # Salvar
    final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_path)
    img.save(final_path, quality=95)
    print(f"\n[+] Sucesso! O diagrama de aquisição de dados foi gerado em:\n'{final_path}'")

if __name__ == "__main__":
    generate_diagram(NOME_ARQUIVO_SAIDA)
