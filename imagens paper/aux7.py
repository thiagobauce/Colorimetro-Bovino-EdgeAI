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

def draw_arrow_down(draw, start_pos, fill="#1B365D", length=40):
    x, y = start_pos
    draw.polygon([(x-10, y), (x+10, y), (x+10, y+length-15), (x+18, y+length-15), 
                  (x, y+length), (x-18, y+length-15), (x-10, y+length-15)], fill=fill)

def draw_arrow_right(draw, start_pos, fill="#4CAF50", length=30):
    x, y = start_pos
    draw.polygon([(x, y-5), (x+length-10, y-5), (x+length-10, y-10), 
                  (x+length, y), (x+length-10, y+10), (x+length-10, y+5), (x, y+5)], fill=fill)

def get_texture_image(input_path, size):
    if os.path.exists(input_path):
        img = Image.open(input_path).convert('RGB')
        # Crop center square
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        img = img.resize((size, size))
        return img
    else:
        # Fallback brown texture
        img = Image.new('RGB', (size, size), color="#8B7355")
        draw = ImageDraw.Draw(img)
        # Add some noise
        import random
        for _ in range(500):
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            c = random.randint(-20, 20)
            draw.point((x, y), fill=(139+c, 115+c, 85+c))
        return img

def draw_grid_img(draw, img, x, y, img_size, grid_n):
    # Draw image border
    draw.rectangle([x, y, x+img_size, y+img_size], outline="#CCC", width=2)
    step = img_size / grid_n
    
    # Draw grid lines
    for i in range(1, grid_n):
        line_x = x + i * step
        draw.line([line_x, y, line_x, y+img_size], fill="#FFF", width=2)
        line_y = y + i * step
        draw.line([x, line_y, x+img_size, line_y], fill="#FFF", width=2)
        
    # Draw circles
    for r in range(grid_n):
        for c in range(grid_n):
            cx = x + c * step + step/2
            cy = y + r * step + step/2
            cr = max(3, min(6, 12 - grid_n)) # Smaller radius for denser grids
            draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], outline="#FFF", width=2)

def draw_tree(draw, x, y, size=40, color="#4CAF50"):
    # Simple binary tree
    s = size
    # Nodes
    root = (x, y)
    l1 = (x-s*0.4, y+s*0.4)
    r1 = (x+s*0.4, y+s*0.4)
    l2 = (x-s*0.6, y+s*0.8)
    r2 = (x-s*0.2, y+s*0.8)
    l3 = (x+s*0.2, y+s*0.8)
    r3 = (x+s*0.6, y+s*0.8)
    
    # Edges
    draw.line([root, l1], fill=color, width=2)
    draw.line([root, r1], fill=color, width=2)
    draw.line([l1, l2], fill=color, width=2)
    draw.line([l1, r2], fill=color, width=2)
    draw.line([r1, l3], fill=color, width=2)
    draw.line([r1, r3], fill=color, width=2)
    
    # Node circles
    nr = 4
    for nx, ny in [root, l1, r1, l2, r2, l3, r3]:
        draw.ellipse([nx-nr, ny-nr, nx+nr, ny+nr], fill="#FFF", outline=color, width=2)

def draw_bagging_arc(draw, x, y, w):
    # Dotted arc over the trees
    draw.arc([x, y, x+w, y+30], 180, 360, fill="#888", width=2)
    draw_text_centered(draw, (x+w/2, y-10), "...", get_font(20, True), fill="#888")

def draw_bar_chart(draw, x, y, w, h):
    # Axes
    draw.line([x, y, x, y+h], fill="#333", width=2)
    draw.line([x, y+h, x+w, y+h], fill="#333", width=2)
    # Bars
    bw = w // 5
    draw.rectangle([x+bw*1, y+h*0.4, x+bw*2-5, y+h], fill="#F4A460")
    draw.rectangle([x+bw*2, y+h*0.2, x+bw*3-5, y+h], fill="#8B4513")
    draw.rectangle([x+bw*3, y+h*0.6, x+bw*4-5, y+h], fill="#A9A9A9")

def draw_scatter_plot(draw, x, y, w, h):
    draw.line([x, y, x, y+h], fill="#333", width=2)
    draw.line([x, y+h, x+w, y+h], fill="#333", width=2)
    # Dashed line
    for i in range(0, int(w), 10):
        draw.line([x+i, y+h - i*(h/w), x+i+5, y+h - (i+5)*(h/w)], fill="#D2691E", width=2)
    # Points
    pts = [(0.2, 0.7), (0.3, 0.6), (0.4, 0.5), (0.5, 0.4), (0.6, 0.3), (0.7, 0.2), 
           (0.3, 0.8), (0.6, 0.4), (0.7, 0.3), (0.8, 0.1)]
    for px, py in pts:
        draw.ellipse([x+w*px-3, y+h*py-3, x+w*px+3, y+h*py+3], fill="#CD853F")

def draw_radar_chart(draw, cx, cy, radius):
    import math
    # Hexagons
    for r in [radius, radius*0.6, radius*0.3]:
        pts = []
        for i in range(6):
            angle = math.pi/2 + i * math.pi/3
            pts.append((cx + r*math.cos(angle), cy - r*math.sin(angle)))
        pts.append(pts[0])
        draw.line(pts, fill="#AAA", width=1)
    
    # Axes
    for i in range(6):
        angle = math.pi/2 + i * math.pi/3
        draw.line([cx, cy, cx + radius*math.cos(angle), cy - radius*math.sin(angle)], fill="#AAA", width=1)
        
    # Data polygon
    d_pts = []
    vals = [0.8, 0.6, 0.9, 0.4, 0.7, 0.5]
    for i in range(6):
        angle = math.pi/2 + i * math.pi/3
        r = radius * vals[i]
        d_pts.append((cx + r*math.cos(angle), cy - r*math.sin(angle)))
    d_pts.append(d_pts[0])
    draw.line(d_pts, fill="#DAA520", width=2)
    for px, py in d_pts[:-1]:
        draw.ellipse([px-2, py-2, px+2, py+2], fill="#DAA520")

def draw_trophy(draw, cx, cy, size):
    s = size
    color = "#DAA520"
    # Base
    draw.polygon([cx-s*0.4, cy+s*0.8, cx+s*0.4, cy+s*0.8, cx+s*0.3, cy+s*0.5, cx-s*0.3, cy+s*0.5], fill=color)
    draw.rectangle([cx-s*0.5, cy+s*0.8, cx+s*0.5, cy+s*1.0], fill=color)
    # Stem
    draw.rectangle([cx-s*0.1, cy+s*0.2, cx+s*0.1, cy+s*0.5], fill=color)
    # Cup
    draw.polygon([cx-s*0.5, cy-s*0.5, cx+s*0.5, cy-s*0.5, cx+s*0.3, cy+s*0.2, cx-s*0.3, cy+s*0.2], fill=color)
    draw.ellipse([cx-s*0.5, cy-s*0.6, cx+s*0.5, cy-s*0.4], fill="#F0E68C")
    # Handles
    draw.arc([cx-s*0.7, cy-s*0.5, cx-s*0.3, cy], 90, 270, fill=color, width=4)
    draw.arc([cx+s*0.3, cy-s*0.5, cx+s*0.7, cy], -90, 90, fill=color, width=4)

def generate_diagram(input_img_path, output_path="diagrama_estudo_ablacao.png"):
    canvas_w = 1000
    canvas_h = 1350
    bg_color = (255, 255, 255)
    img = Image.new('RGB', (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(img)

    font_title = get_font(24, bold=True)
    font_bold = get_font(20, bold=True)
    font_normal = get_font(18)
    font_small = get_font(14)
    font_math = get_font(28, bold=True)

    box_w = 940
    box_x = (canvas_w - box_w) // 2

    # ---- 1. Resoluções de Grid ----
    y = 50
    h1 = 300
    draw.rounded_rectangle([box_x, y, box_x+box_w, y+h1], radius=15, fill="#F0F5FA", outline="#A4C2DF", width=3)
    draw.rectangle([box_x, y, box_x+box_w, y+45], fill="#E6F0FA")
    draw.line([box_x, y+45, box_x+box_w, y+45], fill="#A4C2DF", width=3)
    draw_text_centered(draw, (canvas_w//2, y+22), "1. Resoluções de Grid (extração de atributos)", font_title, fill="#1B365D")
    
    img_size = 140
    gap = 50
    start_x = box_x + (box_w - (img_size*4 + gap*3)) // 2
    
    base_tex = get_texture_image(input_img_path, img_size)
    
    grids = [(1, "1 célula"), (2, "4 células"), (3, "9 células"), (4, "16 células")]
    grid_centers_x = []
    
    for i, (n, txt) in enumerate(grids):
        gx = start_x + i*(img_size+gap)
        grid_centers_x.append(int(gx + img_size/2))
        # Title
        draw_text_centered(draw, (gx + img_size//2, y+75), f"{n} × {n}", font_bold, fill="#1B365D")
        
        # Draw grid box
        box_padding = 10
        draw.rounded_rectangle([gx-box_padding, y+95, gx+img_size+box_padding, y+275], radius=5, fill="white", outline="#CCC", width=2)
        
        # Paste image and draw grid
        img.paste(base_tex, (gx, y+105))
        draw_grid_img(draw, img, gx, y+105, img_size, n)
        
        # Text bottom
        draw_text_centered(draw, (gx + img_size//2, y+260), txt, font_normal, fill="#333")

    draw_arrow_down(draw, (canvas_w//2, y+h1+10), length=40)

    # ---- 2. Algoritmos de Machine Learning ----
    y += h1 + 60
    h2 = 250
    draw.rounded_rectangle([box_x, y, box_x+box_w, y+h2], radius=15, fill="#F2F9F2", outline="#A3D4A3", width=3)
    draw.rectangle([box_x, y, box_x+box_w, y+45], fill="#E6F2E6")
    draw.line([box_x, y+45, box_x+box_w, y+45], fill="#A3D4A3", width=3)
    draw_text_centered(draw, (canvas_w//2, y+22), "2. Algoritmos de Aprendizado de Máquina (Regressores)", font_title, fill="#1F4D1F")
    
    alg_w = 230
    alg_gap = 40
    start_alg = box_x + (box_w - (alg_w*3 + alg_gap*2)) // 2
    
    algs = [
        ("RF", "(Random Forest)", "Bagging de árvores\nde decisão"),
        ("ET", "(Extra Trees)", "Árvores extremamente\nrandomizadas"),
        ("GBR", "(Gradient Boosting)", "Boosting sequencial\nde árvores")
    ]
    alg_centers_y = [] # Para a seção 3
    
    for i, (title, sub, desc) in enumerate(algs):
        ax = start_alg + i*(alg_w+alg_gap)
        draw.rounded_rectangle([ax, y+60, ax+alg_w, y+h2-15], radius=10, fill="white", outline="#A3D4A3", width=2)
        draw_text_centered(draw, (ax+alg_w//2, y+80), title, font_bold, fill="#2E8B57")
        draw_text_centered(draw, (ax+alg_w//2, y+100), sub, font_normal, fill="#2E8B57")
        
        if i < 2:
            # Bagging (RF, ET)
            tx1, tx2, tx3 = ax+40, ax+alg_w//2, ax+alg_w-40
            ty = y+130
            draw_tree(draw, tx1, ty, 30, "#2E8B57")
            draw_tree(draw, tx2, ty, 30, "#2E8B57")
            draw_tree(draw, tx3, ty, 30, "#2E8B57")
            draw_bagging_arc(draw, tx1-10, ty-15, (tx3-tx1)+20)
        else:
            # Boosting (GBR)
            tx1, tx2, tx3 = ax+35, ax+alg_w//2, ax+alg_w-35
            ty = y+130
            draw_tree(draw, tx1, ty, 25, "#2E8B57")
            draw_arrow_right(draw, (tx1+20, ty+10), fill="#2E8B57", length=20)
            draw_tree(draw, tx2, ty, 25, "#2E8B57")
            draw_arrow_right(draw, (tx2+20, ty+10), fill="#2E8B57", length=20)
            draw_tree(draw, tx3, ty, 25, "#2E8B57")
            draw_text_centered(draw, (tx3+25, ty+10), "...", font_bold, fill="#2E8B57")

        draw_text_centered(draw, (ax+alg_w//2, y+205), desc, font_small, fill="#333")

    draw_arrow_down(draw, (canvas_w//2, y+h2+10), length=40)

    # ---- 3. Combinações Ablação ----
    y += h2 + 60
    h3 = 280
    draw.rounded_rectangle([box_x, y, box_x+box_w, y+h3], radius=15, fill="#F7F2FA", outline="#C2B2D6", width=3)
    draw.rectangle([box_x, y, box_x+box_w, y+45], fill="#EFE6F5")
    draw.line([box_x, y+45, box_x+box_w, y+45], fill="#C2B2D6", width=3)
    draw_text_centered(draw, (canvas_w//2, y+22), "3. Combinações do Estudo de Ablação", font_title, fill="#3D2B56")
    
    grid_y_start = y + 100
    grid_y_step = 60
    alg_labels = ["RF", "ET", "GBR"]
    
    # Draw dashed lines horizontal
    for i in range(3):
        gy = grid_y_start + i*grid_y_step
        alg_centers_y.append(gy)
        # Label on left
        draw.rounded_rectangle([box_x+30, gy-15, box_x+90, gy+15], radius=8, fill="#D8BFD8", outline="#C2B2D6")
        draw_text_centered(draw, (box_x+60, gy), alg_labels[i], font_bold, fill="#3D2B56")
        
        # Dashed line
        for lx in range(box_x+95, int(grid_centers_x[-1])+40, 15):
            draw.line([lx, gy, lx+8, gy], fill="#C2B2D6", width=2)
            
    # Draw dashed lines vertical & top labels
    for i, gx in enumerate(grid_centers_x):
        # Label on top
        draw.rounded_rectangle([gx-30, grid_y_start-45, gx+30, grid_y_start-15], radius=8, fill="#D8BFD8", outline="#C2B2D6")
        draw_text_centered(draw, (gx, grid_y_start-30), f"{i+1}×{i+1}", font_bold, fill="#3D2B56")
        
        # Dashed line
        for ly in range(grid_y_start-10, int(alg_centers_y[-1])+20, 15):
            draw.line([gx, ly, gx, ly+8], fill="#C2B2D6", width=2)
            
    # Draw intersection dots
    for gx in grid_centers_x:
        for gy in alg_centers_y:
            draw.ellipse([gx-8, gy-8, gx+8, gy+8], fill="#9370DB", outline="#4B0082", width=1)
            
    # Bracket on right
    br_x = grid_centers_x[-1] + 60
    br_y1 = alg_centers_y[0] - 10
    br_y2 = alg_centers_y[-1] + 10
    br_ym = (br_y1 + br_y2) / 2
    
    draw.line([br_x, br_y1, br_x+10, br_y1], fill="#3D2B56", width=3)
    draw.line([br_x, br_y2, br_x+10, br_y2], fill="#3D2B56", width=3)
    draw.line([br_x+10, br_y1, br_x+10, br_ym-10], fill="#3D2B56", width=3)
    draw.line([br_x+10, br_ym+10, br_x+10, br_y2], fill="#3D2B56", width=3)
    draw.arc([br_x+10, br_ym-20, br_x+30, br_ym], 90, 180, fill="#3D2B56", width=3)
    draw.arc([br_x+10, br_ym, br_x+30, br_ym+20], 180, 270, fill="#3D2B56", width=3)
    
    draw_text_centered(draw, (br_x+90, br_ym-15), "12", font_math, fill="#3D2B56")
    draw_text_centered(draw, (br_x+90, br_ym+15), "modelos", font_bold, fill="#3D2B56")
    draw_text_centered(draw, (br_x+90, br_ym+35), "(4 × 3)", font_bold, fill="#3D2B56")

    draw_arrow_down(draw, (canvas_w//2, y+h3+10), length=40)

    # ---- 4. Comparação e Seleção ----
    y += h3 + 60
    h4 = 200
    draw.rounded_rectangle([box_x, y, box_x+box_w, y+h4], radius=15, fill="#FFF8EB", outline="#D9B36C", width=3)
    draw.rectangle([box_x, y, box_x+box_w, y+45], fill="#FFF0D1")
    draw.line([box_x, y+45, box_x+box_w, y+45], fill="#D9B36C", width=3)
    draw_text_centered(draw, (canvas_w//2, y+22), "4. Comparação e Seleção do Melhor Modelo", font_title, fill="#D2691E")
    
    icon_w = 120
    icon_gap = 60
    start_icon = box_x + (box_w - (icon_w*4 + icon_gap*3)) // 2
    
    # 1. Bar chart
    ix = start_icon
    draw_bar_chart(draw, ix+20, y+70, 80, 60)
    draw_text_centered(draw, (ix+icon_w//2, y+160), "Métricas de\nDesempenho", font_normal, fill="#333")
    
    # 2. Scatter plot
    ix += icon_w + icon_gap
    draw_scatter_plot(draw, ix+20, y+70, 80, 60)
    draw_text_centered(draw, (ix+icon_w//2, y+160), "Validação\nno Conjunto de Teste", font_normal, fill="#333")
    
    # 3. Radar chart
    ix += icon_w + icon_gap
    draw_radar_chart(draw, ix+icon_w//2, y+100, 35)
    draw_text_centered(draw, (ix+icon_w//2, y+160), "Análise\nComparativa", font_normal, fill="#333")
    
    # 4. Trophy
    ix += icon_w + icon_gap
    draw_trophy(draw, ix+icon_w//2, y+90, 25)
    draw_text_centered(draw, (ix+icon_w//2, y+160), "Seleção do\nMelhor Modelo", font_normal, fill="#333")


    final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_path)
    img.save(final_path, quality=95)
    print(f"Diagrama gerado com sucesso em: '{final_path}'")

if __name__ == "__main__":
    # Same base image as aux5/aux2
    imagem_de_entrada = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Dataset_RL/pelo/pelo 2418.3.jpg'
    generate_diagram(imagem_de_entrada, "diagrama_ablacao.png")
