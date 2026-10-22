import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# CONFIGURAÇÃO DAS FOTOS
# ==============================================================================
FOTO_DISPOSITIVO = "/home/workstation_2x_3080/Documents/WhatsApp Image 2026-07-26 at 19.37.01.jpeg"
FOTO_SMARTPHONE = "/home/workstation_2x_3080/Documents/WhatsApp Image 2026-07-26 at 19.36.08.jpeg"
FOTO_COLORIMETRO = "/home/workstation_2x_3080/Documents/WhatsApp Image 2026-07-26 at 19.38.02.jpeg"
FOTO_PELO = "/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Dataset_RL/pelo/pelo 2418.3.jpg"

NOME_ARQUIVO_SAIDA = "diagrama_pipeline_completo.png"

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
    total_h = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] if hasattr(draw, 'textbbox') else 16 for line in lines])
    total_h += line_spacing * (len(lines) - 1)
    
    current_y = y - total_h / 2
    for line in lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
        except:
            w, h = 80, 16
        draw.text((x - w / 2, current_y), line, font=font, fill=fill)
        current_y += h + line_spacing

def add_rounded_image(canvas, img_path, pos, size, radius, crop=True, bg_color="#FFFFFF"):
    try:
        img = Image.open(img_path).convert("RGB")
    except Exception as e:
        img = Image.new("RGB", size, (220, 220, 220))
        d = ImageDraw.Draw(img)
        d.line((0,0) + size, fill=(150,150,150), width=3)
        d.line((0,size[1], size[0],0), fill=(150,150,150), width=3)
        draw_text_centered(d, (size[0]//2, size[1]//2), "Sem Imagem", get_font(18, True), fill="#666")
    
    target_ratio = size[0] / size[1]
    img_ratio = img.width / img.height
    
    if crop:
        if img_ratio > target_ratio:
            new_w = int(img.height * target_ratio)
            offset = (img.width - new_w) // 2
            img = img.crop((offset, 0, offset + new_w, img.height))
        else:
            new_h = int(img.width / target_ratio)
            offset = (img.height - new_h) // 2
            img = img.crop((0, offset, img.width, offset + new_h))
        img = img.resize(size, Image.Resampling.LANCZOS)
    else:
        img.thumbnail(size, Image.Resampling.LANCZOS)
        padded = Image.new("RGB", size, ImageDraw.ImageColor.getrgb(bg_color))
        offset = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)
        padded.paste(img, offset)
        img = padded
        
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    
    canvas.paste(img, pos, mask)

def draw_arrow_right(draw, start_pos, fill="#2C3E50", length=30):
    x, y = start_pos
    draw.polygon([
        (x, y-6), (x+length-12, y-6), (x+length-12, y-15), 
        (x+length, y), 
        (x+length-12, y+15), (x+length-12, y+6), (x, y+6)
    ], fill=fill)

def draw_arrow_down(draw, start_pos, fill="#2C3E50", length=30):
    x, y = start_pos
    draw.polygon([
        (x-6, y), (x+6, y), (x+6, y+length-12), 
        (x+15, y+length-12), (x, y+length), (x-15, y+length-12), (x-6, y+length-12)
    ], fill=fill)

def generate_texture_image(size, color="#BFA58A"):
    img = Image.new('RGB', size, color=ImageDraw.ImageColor.getrgb(color))
    draw = ImageDraw.Draw(img)
    random.seed(42)
    c_r, c_g, c_b = ImageDraw.ImageColor.getrgb(color)
    for _ in range(size[0]*size[1]//15):
        x, y = random.randint(0, size[0]-1), random.randint(0, size[1]-1)
        c = random.randint(-20, 20)
        draw.point((x, y), fill=(max(0, min(255, c_r+c)), max(0, min(255, c_g+c)), max(0, min(255, c_b+c))))
    return img

def draw_histogram(canvas, draw, x, y, w, h):
    # Eixos
    draw.line([x, y, x, y+h], fill="#333", width=2)
    draw.line([x, y+h, x+w+10, y+h], fill="#333", width=2)
    
    # Overlay RGBA para transparência
    overlay = Image.new("RGBA", canvas.size, (255,255,255,0))
    d_overlay = ImageDraw.Draw(overlay)
    
    pts_r, pts_g, pts_b = [(x, y+h)], [(x, y+h)], [(x, y+h)]
    for i in range(w):
        nr = math.exp(-((i - w*0.35)**2) / (2 * (w*0.08)**2))
        ng = math.exp(-((i - w*0.5)**2) / (2 * (w*0.06)**2))
        nb = math.exp(-((i - w*0.65)**2) / (2 * (w*0.09)**2))
        pts_r.append((x + i, y + h - nr * h * 0.8))
        pts_g.append((x + i, y + h - ng * h * 0.95))
        pts_b.append((x + i, y + h - nb * h * 0.75))
    pts_r.append((x+w, y+h)); pts_g.append((x+w, y+h)); pts_b.append((x+w, y+h))
    
    d_overlay.polygon(pts_r, fill=(255, 60, 60, 140))
    d_overlay.polygon(pts_g, fill=(60, 200, 60, 140))
    d_overlay.polygon(pts_b, fill=(60, 100, 255, 140))
    
    canvas.paste(overlay, (0,0), overlay)
    
    # Gradiente na base simulando espectro
    for i in range(w):
        val = i / w
        r = int(255 * (1-val))
        b = int(255 * val)
        g = int(255 * (0.5 - abs(val-0.5)))
        draw.line([x+i, y+h+5, x+i, y+h+15], fill=(r,g,b))

def draw_cielab_sphere(canvas, draw, cx, cy, r):
    sphere = Image.new("RGBA", (int(r*2), int(r*2)), (0,0,0,0))
    for i in range(int(r*2)):
        for j in range(int(r*2)):
            dx = i - r
            dy = j - r
            dist = math.sqrt(dx*dx + dy*dy)
            if dist <= r:
                angle = math.atan2(dy, dx)
                hue = (angle / (2*math.pi)) + 0.5
                sat = dist / r
                rgb = ImageDraw.ImageColor.getrgb(f"hsv({hue*360},{sat*100}%,90%)")
                z = math.sqrt(max(0, r*r - dx*dx - dy*dy))
                light = 0.4 + 0.6 * (z / r)
                hl = max(0, 1 - math.sqrt((dx+r*0.3)**2 + (dy+r*0.3)**2)/(r*0.4))
                light = min(1, light + hl*0.5)
                rgb = (int(rgb[0]*light), int(rgb[1]*light), int(rgb[2]*light), 255)
                sphere.putpixel((i, j), rgb)
    
    canvas.paste(sphere, (int(cx-r), int(cy-r)), sphere)
    font = get_font(16, True)
    draw.line([cx-r-30, cy, cx+r+30, cy], fill="#333", width=2)
    draw.line([cx, cy-r-30, cx, cy+r+30], fill="#333", width=2)
    
    draw_text_centered(draw, (cx+r+45, cy), "+a*", font, fill="#333")
    draw_text_centered(draw, (cx-r-45, cy), "-a*", font, fill="#333")
    draw_text_centered(draw, (cx, cy-r-45), "L*", font, fill="#333")
    draw_text_centered(draw, (cx, cy+r+45), "-b*", font, fill="#333")

def draw_network(draw, cx, cy, w, h):
    nodes = []
    random.seed(123)
    for _ in range(35):
        angle = random.uniform(0, 2*math.pi)
        r = math.sqrt(random.uniform(0, 1))
        nx = cx + r * w/2 * math.cos(angle)
        ny = cy + r * h/2 * math.sin(angle)
        nodes.append((nx, ny))
    
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if math.dist(nodes[i], nodes[j]) < 45:
                draw.line([nodes[i], nodes[j]], fill="#4C73A6", width=2)
                
    for nx, ny in nodes:
        draw.ellipse([nx-7, ny-7, nx+7, ny+7], fill="#1B365D")

def draw_sun(draw, cx, cy, r, color="#FFC107"):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    for i in range(8):
        angle = i * math.pi / 4
        x1, y1 = cx + r*1.3 * math.cos(angle), cy + r*1.3 * math.sin(angle)
        x2, y2 = cx + r*2.0 * math.cos(angle), cy + r*2.0 * math.sin(angle)
        draw.line([x1, y1, x2, y2], fill=color, width=3)

def generate_diagram(output_path="diagrama_pipeline_completo.png"):
    canvas_w = 2200
    canvas_h = 1200
    bg_color = (255, 255, 255)
    img = Image.new('RGB', (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(img)

    font_title = get_font(38, bold=True)
    font_sub_title = get_font(26, bold=False)
    font_header = get_font(20, bold=True)
    font_desc = get_font(18)
    font_small = get_font(16)

    # Header Principal
    draw_text_centered(draw, (canvas_w//2, 70), "PIPELINE COMPUTACIONAL PARA ESTIMATIVA DAS COORDENADAS CIELAB", font_title, fill="#1B365D")
    draw_text_centered(draw, (canvas_w//2, 120), "Da imagem capturada à predição da cor", font_sub_title, fill="#555")

    # Configuração dos 5 painéis
    panel_w = 380
    panel_h = 950
    gap = 40
    start_x = (canvas_w - (5 * panel_w + 4 * gap)) // 2
    y_panel = 180
    
    panels = [
        {"title": "1. IMAGEM ADQUIRIDA\nEM CAMPO", "color": "#F2F6FA", "outline": "#6D90BB"},
        {"title": "2. PADRONIZAÇÃO\nDA IMAGEM", "color": "#F4F8F3", "outline": "#84AC7D"},
        {"title": "3. DELIMITAÇÃO DA\nREGIÃO DE INTERESSE", "color": "#F7F4F9", "outline": "#A58DBA"},
        {"title": "4. EXTRAÇÃO DE\nATRIBUTOS CROMÁTICOS", "color": "#FDF9F0", "outline": "#E2B86E"},
        {"title": "5. MODELAGEM POR\nINTELIGÊNCIA ARTIFICIAL", "color": "#F2F4F8", "outline": "#6070A6"}
    ]

    for i, p in enumerate(panels):
        px = start_x + i * (panel_w + gap)
        
        # Caixa Principal
        draw.rounded_rectangle([px, y_panel, px+panel_w, y_panel+panel_h], radius=15, fill=p["color"], outline=p["outline"], width=3)
        
        # Cabeçalho da Caixa
        draw.rounded_rectangle([px, y_panel, px+panel_w, y_panel+90], radius=15, fill=p["outline"])
        draw.rectangle([px, y_panel+45, px+panel_w, y_panel+90], fill=p["outline"]) 
        draw.line([px, y_panel+90, px+panel_w, y_panel+90], fill=p["outline"], width=3)
        
        draw_text_multiline_centered(draw, (px + panel_w//2, y_panel + 45), p["title"], font_header, fill="white", line_spacing=5)
        
        # Desenhar Setas de conexão (exceto para o último)
        if i < 4:
            arrow_x = px + panel_w + (gap - 40) // 2
            arrow_y = y_panel + panel_h // 2
            draw_arrow_right(draw, (arrow_x, arrow_y), fill="#2C3E50", length=40)

        # ---------------------------------------------------------
        # CONTEÚDO ESPECÍFICO DE CADA PAINEL
        # ---------------------------------------------------------
        cx = px + panel_w//2

        if i == 0:
            # 1. IMAGEM ADQUIRIDA (3 fotos em cascata, redimensionadas sem cortar)
            img_size = (340, 200)
            
            y_base = y_panel + 120
            
            # Foto 1: Dispositivo
            add_rounded_image(img, FOTO_DISPOSITIVO, (cx - img_size[0]//2, y_base), img_size, 15, crop=False, bg_color=p["color"])
            draw.rounded_rectangle([cx - img_size[0]//2, y_base, cx + img_size[0]//2, y_base + img_size[1]], radius=15, outline="#888", width=2)
            draw_text_centered(draw, (cx, y_base + img_size[1] + 15), "Dispositivo de isolamento luminoso", font_small, fill="#333")
            
            draw_arrow_down(draw, (cx, y_base + img_size[1] + 30), fill="#7F8C8D", length=30)
            
            # Foto 2: Smartphone
            y_base += 265
            add_rounded_image(img, FOTO_SMARTPHONE, (cx - img_size[0]//2, y_base), img_size, 15, crop=False, bg_color=p["color"])
            draw.rounded_rectangle([cx - img_size[0]//2, y_base, cx + img_size[0]//2, y_base + img_size[1]], radius=15, outline="#888", width=2)
            draw_text_centered(draw, (cx, y_base + img_size[1] + 15), "Captura com smartphone (em campo)", font_small, fill="#333")

            draw_arrow_down(draw, (cx, y_base + img_size[1] + 30), fill="#7F8C8D", length=30)
            
            # Foto 3: Colorímetro
            y_base += 265
            add_rounded_image(img, FOTO_COLORIMETRO, (cx - img_size[0]//2, y_base), img_size, 15, crop=False, bg_color=p["color"])
            draw.rounded_rectangle([cx - img_size[0]//2, y_base, cx + img_size[0]//2, y_base + img_size[1]], radius=15, outline="#888", width=2)
            draw_text_centered(draw, (cx, y_base + img_size[1] + 15), "Colorímetro (Dispositivo de referência)", font_small, fill="#333")

        elif i == 1:
            # 2. PADRONIZAÇÃO
            draw_text_multiline_centered(draw, (cx, y_panel + 160), "Correção de iluminação\ne balanço de branco", font_desc, fill="#333")
            
            # Ícones Sol -> Lua
            draw_sun(draw, cx - 80, y_panel + 240, 15, "#F39C12")
            draw_arrow_right(draw, (cx - 30, y_panel + 240), fill="#7F8C8D", length=60)
            draw_sun(draw, cx + 80, y_panel + 240, 15, "#BDC3C7")
            
            # Patches reais da imagem da pele
            from PIL import ImageEnhance
            try:
                base_pelo = Image.open(FOTO_PELO).convert("RGB")
                w, h = base_pelo.size
                min_d = min(w, h)
                base_pelo = base_pelo.crop(((w-min_d)//2, (h-min_d)//2, (w+min_d)//2, (h+min_d)//2)).resize((140, 140))
            except Exception as e:
                base_pelo = generate_texture_image((140, 140), "#8B7355")
                
            tex_dark = ImageEnhance.Brightness(base_pelo).enhance(0.6)
            tex_light = ImageEnhance.Brightness(base_pelo).enhance(1.3)
            
            img.paste(tex_dark, (cx - 145, y_panel + 300))
            draw.rectangle([cx-145, y_panel+300, cx-5, y_panel+440], outline="#CCC", width=2)
            
            img.paste(tex_light, (cx + 5, y_panel + 300))
            draw.rectangle([cx+5, y_panel+300, cx+145, y_panel+440], outline="#CCC", width=2)
            
            draw.line([cx, y_panel + 290, cx, y_panel + 450], fill="#888", width=3)
            
            draw_text_centered(draw, (cx, y_panel + 550), "Normalização cromática", font_desc, fill="#333")
            draw_histogram(img, draw, cx - 120, y_panel + 620, 240, 180)

        elif i == 2:
            # 3. DELIMITAÇÃO DA ROI
            draw_text_multiline_centered(draw, (cx, y_panel + 160), "Segmentação automática\nda área de interesse", font_desc, fill="#333")
            
            try:
                base_pelo = Image.open(FOTO_PELO).convert("RGB")
                w, h = base_pelo.size
                base_pelo = base_pelo.crop(((w-280)//2, (h-220)//2, (w+280)//2, (h+220)//2))
            except:
                base_pelo = generate_texture_image((280, 220), "#CDBA96")
                
            img.paste(base_pelo, (cx - 140, y_panel + 220))
            draw.rectangle([cx-140, y_panel+220, cx+140, y_panel+440], outline="#CCC", width=2)
            
            # Caixa vermelha
            draw.rectangle([cx-70, y_panel + 250, cx+70, y_panel + 410], outline="#E74C3C", width=4)
            draw.line([cx-10, y_panel + 330, cx+10, y_panel + 330], fill="#E74C3C", width=3)
            draw.line([cx, y_panel + 320, cx, y_panel + 340], fill="#E74C3C", width=3)
            
            draw_arrow_down(draw, (cx, y_panel + 500), fill="#8E44AD", length=50)
            
            draw_text_centered(draw, (cx, y_panel + 610), "ROI final utilizada", font_desc, fill="#333")
            img.paste(base_pelo, (cx - 140, y_panel + 650))
            draw.rectangle([cx-140, y_panel+650, cx+140, y_panel+870], outline="#CCC", width=2)
            
            # Caixa verde
            draw.rectangle([cx-70, y_panel + 680, cx+70, y_panel + 840], outline="#2ECC71", width=4)

        elif i == 3:
            # 4. EXTRAÇÃO DE ATRIBUTOS
            draw_text_centered(draw, (cx, y_panel + 160), "Divisão da ROI em grid", font_desc, fill="#333")
            
            try:
                base_pelo = Image.open(FOTO_PELO).convert("RGB")
                w, h = base_pelo.size
                base_pelo = base_pelo.crop(((w-280)//2, (h-220)//2, (w+280)//2, (h+220)//2))
            except:
                base_pelo = generate_texture_image((280, 220), "#CDBA96")
                
            img.paste(base_pelo, (cx - 140, y_panel + 200))
            draw.rectangle([cx-140, y_panel+200, cx+140, y_panel+420], outline="#CCC", width=2)
            
            # Desenhar grid 4x4
            step_x = 280 / 4
            step_y = 220 / 4
            for j in range(1, 4):
                draw.line([cx - 140 + j*step_x, y_panel + 200, cx - 140 + j*step_x, y_panel + 420], fill="#FFF", width=2)
                draw.line([cx - 140, y_panel + 200 + j*step_y, cx + 140, y_panel + 200 + j*step_y], fill="#FFF", width=2)
            
            draw_text_centered(draw, (cx, y_panel + 470), "...", font_title, fill="#777")
            
            draw_text_multiline_centered(draw, (cx, y_panel + 550), "Cálculo dos descritores\ncromáticos", font_desc, fill="#333")
            
            # Botões RGB, HSV, CIELAB
            draw.rounded_rectangle([cx - 160, y_panel + 620, cx - 60, y_panel + 670], radius=10, fill="#FADBD8", outline="#E6B0AA", width=2)
            draw_text_centered(draw, (cx - 110, y_panel + 645), "RGB", font_small, fill="#333")
            
            draw.rounded_rectangle([cx - 45, y_panel + 620, cx + 45, y_panel + 670], radius=10, fill="#D5F5E3", outline="#A9DFBF", width=2)
            draw_text_centered(draw, (cx, y_panel + 645), "HSV", font_small, fill="#333")
            
            draw.rounded_rectangle([cx + 60, y_panel + 620, cx + 160, y_panel + 670], radius=10, fill="#D4E6F1", outline="#A9CCE3", width=2)
            draw_text_centered(draw, (cx + 110, y_panel + 645), "CIELAB", font_small, fill="#333")
            
            draw_text_centered(draw, (cx, y_panel + 730), "...", font_title, fill="#777")
            draw_text_centered(draw, (cx, y_panel + 800), "Vetor de atributos", font_desc, fill="#333")
            
            # Bloquinhos do vetor
            colors = ["#C39BD3", "#C39BD3", "#7FB3D5", "#7FB3D5", "#76D7C4", "#76D7C4", "#F7DC6F", "#F7DC6F"]
            bw = 30
            gap_b = 6
            start_b = cx - (len(colors)*(bw+gap_b)) // 2
            for j, c in enumerate(colors):
                draw.rounded_rectangle([start_b + j*(bw+gap_b), y_panel + 840, start_b + j*(bw+gap_b) + bw, y_panel + 880], radius=4, fill=c)
            draw_text_centered(draw, (start_b + len(colors)*(bw+gap_b) + 15, y_panel + 860), "...", font_desc, fill="#777")

        elif i == 4:
            # 5. MODELAGEM
            draw_text_multiline_centered(draw, (cx, y_panel + 160), "Modelos de IA\n(regressão)", font_desc, fill="#333")
            
            draw_network(draw, cx, y_panel + 330, 240, 180)
            
            draw_arrow_down(draw, (cx, y_panel + 490), fill="#34495E", length=50)
            
            draw_text_multiline_centered(draw, (cx, y_panel + 610), "Predição das coordenadas\nno espaço CIELAB", font_desc, fill="#333")
            
            draw_cielab_sphere(img, draw, cx, y_panel + 780, 110)

    final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_path)
    img.save(final_path, quality=95)
    print(f"\n[+] Diagrama pipeline completo gerado em:\n'{final_path}'")

if __name__ == "__main__":
    generate_diagram(NOME_ARQUIVO_SAIDA)
