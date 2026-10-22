import os
from PIL import Image, ImageDraw, ImageFont

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

def draw_db_cylinder(draw, x, y, w, h, fill="#2C4C74", outline="#1F3653"):
    top_h = h * 0.15
    draw.ellipse([x, y + h - top_h, x + w, y + h], fill=fill, outline=outline, width=3)
    draw.rectangle([x, y + top_h/2, x + w, y + h - top_h/2], fill=fill, outline=None)
    draw.line([x, y + top_h/2, x, y + h - top_h/2], fill=outline, width=3)
    draw.line([x+w, y + top_h/2, x+w, y + h - top_h/2], fill=outline, width=3)
    draw.ellipse([x, y, x + w, y + top_h], fill=fill, outline=outline, width=3)
    draw.arc([x, y + h*0.33, x + w, y + h*0.33 + top_h], 0, 180, fill=outline, width=3)
    draw.arc([x, y + h*0.66, x + w, y + h*0.66 + top_h], 0, 180, fill=outline, width=3)

def draw_table_icon(draw, x, y, w, h, fill="#F2F8FF", outline="#2C4C74"):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=5, fill=fill, outline=outline, width=3)
    draw.line([x, y+h*0.25, x+w, y+h*0.25], fill=outline, width=3)
    draw.line([x+w*0.33, y+h*0.25, x+w*0.33, y+h], fill=outline, width=2)
    draw.line([x+w*0.66, y+h*0.25, x+w*0.66, y+h], fill=outline, width=2)
    draw.line([x, y+h*0.5, x+w, y+h*0.5], fill=outline, width=2)
    draw.line([x, y+h*0.75, x+w, y+h*0.75], fill=outline, width=2)

def draw_cow_head(draw, cx, cy, size, color="#D4C4B7", outline="#5A4A3F"):
    s = size
    # Orelhas
    draw.ellipse([cx-s*0.9, cy-s*0.3, cx-s*0.4, cy+s*0.1], fill=color, outline=outline, width=3)
    draw.ellipse([cx+s*0.4, cy-s*0.3, cx+s*0.9, cy+s*0.1], fill=color, outline=outline, width=3)
    # Chifres
    draw.polygon([cx-s*0.6, cy-s*0.3, cx-s*0.8, cy-s*0.8, cx-s*0.3, cy-s*0.5], fill="#EBEBEB", outline=outline)
    draw.polygon([cx+s*0.6, cy-s*0.3, cx+s*0.8, cy-s*0.8, cx+s*0.3, cy-s*0.5], fill="#EBEBEB", outline=outline)
    # Base Cabeça
    draw.ellipse([cx-s*0.6, cy-s*0.6, cx+s*0.6, cy+s*0.6], fill=color, outline=outline, width=3)
    # Focinho
    draw.ellipse([cx-s*0.65, cy+s*0.2, cx+s*0.65, cy+s*0.9], fill="#F4E4D7", outline=outline, width=3)
    # Narinas
    draw.ellipse([cx-s*0.3, cy+s*0.4, cx-s*0.1, cy+s*0.6], fill=outline)
    draw.ellipse([cx+s*0.1, cy+s*0.4, cx+s*0.3, cy+s*0.6], fill=outline)
    # Olhos
    draw.ellipse([cx-s*0.35, cy-s*0.2, cx-s*0.15, cy], fill=outline)
    draw.ellipse([cx+s*0.15, cy-s*0.2, cx+s*0.35, cy], fill=outline)

def draw_cow_silhouette(draw, cx, cy, size, color, outline=None):
    s = size
    for mode in range(2):
        fill_col = color if mode == 1 else outline
        w = 2 if mode == 0 else 0
        if mode == 0 and not outline: continue
        # Corpo
        draw.rounded_rectangle([cx-s*1.2, cy-s*0.4, cx+s*0.6, cy+s*0.5], radius=int(s*0.3), fill=fill_col)
        # Patas
        draw.rectangle([cx-s*1.0, cy+s*0.3, cx-s*0.8, cy+s*1.2], fill=fill_col)
        draw.rectangle([cx-s*0.6, cy+s*0.3, cx-s*0.4, cy+s*1.2], fill=fill_col)
        draw.rectangle([cx+s*0.1, cy+s*0.3, cx+s*0.3, cy+s*1.2], fill=fill_col)
        draw.rectangle([cx+s*0.4, cy+s*0.3, cx+s*0.6, cy+s*1.2], fill=fill_col)
        # Cabeça
        draw.ellipse([cx+s*0.5, cy-s*0.8, cx+s*1.1, cy], fill=fill_col)
        draw.ellipse([cx+s*0.9, cy-s*0.4, cx+s*1.3, cy], fill=fill_col)
        # Orelha
        draw.polygon([cx+s*0.7, cy-s*0.7, cx+s*0.5, cy-s*1.0, cx+s*1.0, cy-s*0.6], fill=fill_col)

def draw_brain(draw, cx, cy, size, color="#A67B5B"):
    s = size
    draw.ellipse([cx-s, cy-s*0.8, cx+s, cy+s*0.8], outline=color, width=3)
    draw.ellipse([cx-s*0.8, cy-s*0.9, cx+s*0.2, cy+s*0.2], outline=color, width=3)
    draw.ellipse([cx-s*0.2, cy-s*0.2, cx+s*0.8, cy+s*0.9], outline=color, width=3)
    nodes = [(cx-s*0.6, cy-s*0.3), (cx-s*0.2, cy-s*0.6), (cx+s*0.4, cy-s*0.4),
             (cx-s*0.4, cy+s*0.3), (cx+s*0.2, cy+s*0.5), (cx+s*0.6, cy+s*0.1), (cx, cy)]
    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2:
                draw.line([n1, n2], fill=color, width=2)
    for nx, ny in nodes:
        draw.ellipse([nx-5, ny-5, nx+5, ny+5], fill=color)

def draw_regression(draw, x, y, w, h, color="#1B365D"):
    draw.line([x, y, x, y+h], fill=color, width=3)
    draw.line([x, y+h, x+w, y+h], fill=color, width=3)
    draw.line([x+w*0.1, y+h*0.8, x+w*0.9, y+h*0.2], fill=color, width=3)
    pts = [(0.2, 0.6), (0.3, 0.7), (0.4, 0.4), (0.5, 0.5), (0.6, 0.3), (0.7, 0.4), (0.8, 0.2)]
    for px, py in pts:
        draw.ellipse([x+w*px-4, y+h*py-4, x+w*px+4, y+h*py+4], fill=color)

def draw_target(draw, cx, cy, size, color="#A67B5B"):
    s = size
    draw.ellipse([cx-s, cy-s, cx+s, cy+s], outline=color, width=4)
    draw.ellipse([cx-s*0.6, cy-s*0.6, cx+s*0.6, cy+s*0.6], outline=color, width=4)
    draw.ellipse([cx-s*0.2, cy-s*0.2, cx+s*0.2, cy+s*0.2], outline=color, width=4)
    draw.line([cx-s*1.2, cy, cx-s*0.3, cy], fill=color, width=4)
    draw.line([cx+s*0.3, cy, cx+s*1.2, cy], fill=color, width=4)
    draw.line([cx, cy-s*1.2, cx, cy-s*0.3], fill=color, width=4)
    draw.line([cx, cy+s*0.3, cx, cy+s*1.2], fill=color, width=4)

def draw_arrow_down(draw, start_pos, fill="#1B365D", length=40):
    x, y = start_pos
    draw.polygon([(x-10, y), (x+10, y), (x+10, y+length-15), (x+18, y+length-15), 
                  (x, y+length), (x-18, y+length-15), (x-10, y+length-15)], fill=fill)

def generate_diagram(output_path="diagrama_pipeline.png"):
    canvas_w = 800
    canvas_h = 1350
    bg_color = (255, 255, 255)
    img = Image.new('RGB', (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26, bold=True)
    font_bold = get_font(20, bold=True)
    font_normal = get_font(18)
    font_small = get_font(14)

    box_w = 640
    box_x = (canvas_w - box_w) // 2

    # 1. Banco de dados
    y = 50
    h1 = 180
    draw.rounded_rectangle([box_x, y, box_x+box_w, y+h1], radius=15, fill="#F0F5FA", outline="#A4C2DF", width=3)
    draw.rectangle([box_x, y, box_x+box_w, y+45], fill="#E6F0FA")
    draw.line([box_x, y+45, box_x+box_w, y+45], fill="#A4C2DF", width=3)
    draw_text_centered(draw, (canvas_w//2, y+22), "Banco de dados", font_title, fill="#1B365D")
    
    draw_db_cylinder(draw, box_x + 40, y + 60, 80, 100)
    draw_table_icon(draw, box_x + box_w - 120, y + 60, 80, 100)
    
    img_start_x = box_x + 160
    img_y = y + 60
    img_size = 90
    colors = ["#C8B19D", "#B39883", "#5C3A21", "#4A321F", "#D4C2B3", "#D9C9BE"]
    for i in range(2):
        for j in range(3):
            idx = i*3 + j
            draw.rectangle([img_start_x + j*(img_size+10), img_y + i*(img_size//2+10), 
                            img_start_x + j*(img_size+10) + img_size, img_y + i*(img_size//2+10) + img_size//2], 
                            fill=colors[idx], outline="#888", width=1)

    draw_arrow_down(draw, (canvas_w//2, y+h1+5), length=40)

    # 2. Animal ID
    y += h1 + 50
    h2 = 180
    draw.rounded_rectangle([box_x, y, box_x+box_w, y+h2], radius=15, fill="#F2F9F2", outline="#A3D4A3", width=3)
    draw.rectangle([box_x, y, box_x+box_w, y+45], fill="#E6F2E6")
    draw.line([box_x, y+45, box_x+box_w, y+45], fill="#A3D4A3", width=3)
    draw_text_centered(draw, (canvas_w//2, y+22), "Animal ID", font_title, fill="#1F4D1F")
    
    cow_x_start = box_x + 90
    gap = 115
    ids = ["ID: 01", "ID: 02", "ID: 03", "...", "ID: N"]
    colors_cow = ["#D4C4B7", "#DCDCDC", "#555555", None, "#D4C4B7"]
    for i, c_id in enumerate(ids):
        cx = cow_x_start + i*gap
        if i != 3:
            draw_cow_head(draw, cx, y+90, 25, color=colors_cow[i])
            draw.rounded_rectangle([cx-35, y+135, cx+35, y+165], radius=5, fill="white", outline="#CCC", width=2)
            draw_text_centered(draw, (cx, y+150), c_id, font_small, fill="black")
        else:
            draw_text_centered(draw, (cx, y+110), "...", font_title, fill="#666")

    draw_arrow_down(draw, (canvas_w//2, y+h2+5), length=40)

    # 3. GroupShuffleSplit
    y += h2 + 50
    h3 = 150
    draw.rounded_rectangle([box_x, y, box_x+box_w, y+h3], radius=15, fill="#F7F2FA", outline="#C2B2D6", width=3)
    draw.rectangle([box_x, y, box_x+box_w, y+45], fill="#EFE6F5")
    draw.line([box_x, y+45, box_x+box_w, y+45], fill="#C2B2D6", width=3)
    draw_text_centered(draw, (canvas_w//2, y+22), "GroupShuffleSplit", font_title, fill="#3D2B56")

    sq_size = 25
    sq_gap = 5
    for i in range(2):
        for j in range(3):
            draw.rounded_rectangle([box_x + 150 + j*(sq_size+sq_gap), y + 60 + i*(sq_size+sq_gap),
                                   box_x + 150 + j*(sq_size+sq_gap) + sq_size, y + 60 + i*(sq_size+sq_gap) + sq_size], 
                                   radius=3, fill="#A388C4")
            
    ax = canvas_w // 2
    ay = y + 105
    draw.line([ax-35, ay-15, ax+35, ay+15], fill="#1B365D", width=3)
    draw.polygon([(ax+35, ay+15), (ax+25, ay+15), (ax+35, ay+5)], fill="#1B365D")
    draw.line([ax-35, ay+15, ax+35, ay-15], fill="#1B365D", width=3)
    draw.polygon([(ax+35, ay-15), (ax+25, ay-15), (ax+35, ay-5)], fill="#1B365D")
    
    for i in range(2):
        for j in range(3):
            draw.rounded_rectangle([box_x + 390 + j*(sq_size+sq_gap), y + 60 + i*(sq_size+sq_gap),
                                   box_x + 390 + j*(sq_size+sq_gap) + sq_size, y + 60 + i*(sq_size+sq_gap) + sq_size], 
                                   radius=3, fill="#6CA0DC")

    y += h3 + 5
    draw.line([canvas_w//2, y, canvas_w//2, y+20], fill="#1B365D", width=4)
    draw.line([canvas_w//2 - 160, y+20, canvas_w//2 + 160, y+20], fill="#1B365D", width=4)
    draw_arrow_down(draw, (canvas_w//2 - 160, y+20), length=30)
    draw_arrow_down(draw, (canvas_w//2 + 160, y+20), length=30)

    # 4. Treino e Teste
    y += 50
    h4 = 220
    w_half = 300
    
    # Treino
    draw.rounded_rectangle([box_x, y, box_x+w_half, y+h4], radius=15, fill="#F2F9F2", outline="#5C8A5C", width=3)
    draw.rectangle([box_x, y, box_x+w_half, y+70], fill="#E6F2E6")
    draw.line([box_x, y+70, box_x+w_half, y+70], fill="#5C8A5C", width=3)
    draw_text_centered(draw, (box_x+w_half//2, y+25), "Treino", font_title, fill="#1F4D1F")
    draw_text_centered(draw, (box_x+w_half//2, y+55), "37 animais", font_normal, fill="#1F4D1F")
    
    draw_cow_silhouette(draw, box_x+w_half//2, y+120, 30, color="#4D804D")
    for i in range(4):
        if i == 2:
            draw_text_centered(draw, (box_x + 60 + i*60, y+185), "...", font_title, fill="#4D804D")
        else:
            draw_cow_silhouette(draw, box_x + 60 + i*60, y+185, 12, color="#4D804D", outline="#4D804D")

    # Teste
    tx = canvas_w//2 + 20
    draw.rounded_rectangle([tx, y, tx+w_half, y+h4], radius=15, fill="#F0F5FA", outline="#4C73A6", width=3)
    draw.rectangle([tx, y, tx+w_half, y+70], fill="#E6F0FA")
    draw.line([tx, y+70, tx+w_half, y+70], fill="#4C73A6", width=3)
    draw_text_centered(draw, (tx+w_half//2, y+25), "Teste", font_title, fill="#1B365D")
    draw_text_centered(draw, (tx+w_half//2, y+55), "10 animais", font_normal, fill="#1B365D")

    draw_cow_silhouette(draw, tx+w_half//2, y+120, 30, color="#336699")
    for i in range(4):
        if i == 2:
            draw_text_centered(draw, (tx + 60 + i*60, y+185), "...", font_title, fill="#336699")
        else:
            draw_cow_silhouette(draw, tx + 60 + i*60, y+185, 12, color="#336699", outline="#336699")

    # Merge
    y += h4 + 5
    draw.line([canvas_w//2 - 160, y, canvas_w//2 - 160, y+30], fill="#1B365D", width=4)
    draw.line([canvas_w//2 + 160, y, canvas_w//2 + 160, y+30], fill="#1B365D", width=4)
    draw.line([canvas_w//2 - 160, y+30, canvas_w//2 + 160, y+30], fill="#1B365D", width=4)
    draw_arrow_down(draw, (canvas_w//2, y+30), length=30)

    # 5. Modelagem
    y += 60
    h5 = 160
    box_w_mod = 540
    box_x_mod = (canvas_w - box_w_mod) // 2
    draw.rounded_rectangle([box_x_mod, y, box_x_mod+box_w_mod, y+h5], radius=15, fill="#FFF8EB", outline="#D9B36C", width=3)
    draw.rectangle([box_x_mod, y, box_x_mod+box_w_mod, y+45], fill="#FFF0D1")
    draw.line([box_x_mod, y+45, box_x_mod+box_w_mod, y+45], fill="#D9B36C", width=3)
    draw_text_centered(draw, (canvas_w//2, y+22), "Modelagem", font_title, fill="#7A5C29")

    draw_brain(draw, box_x_mod + 110, y+100, 35, color="#A67B5B")
    draw_regression(draw, box_x_mod + 220, y+65, 100, 70, color="#1B365D")
    draw_target(draw, box_x_mod + 430, y+100, 35, color="#A67B5B")

    final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_path)
    img.save(final_path, quality=95)
    print(f"Diagrama gerado com sucesso em: '{final_path}'")

if __name__ == "__main__":
    generate_diagram("diagrama_pipeline_treino.png")
