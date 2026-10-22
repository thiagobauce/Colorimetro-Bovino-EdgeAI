import os
from PIL import Image, ImageDraw, ImageFont

def draw_numbered_circle(draw, x, y, number, radius=12):
    """Desenha um círculo branco com um número preto no centro."""
    # Desenha o círculo
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="white")
    
    # Desenha o número (centralizado)
    # Tenta usar uma fonte padrão, senão usa a fonte básica do Pillow
    try:
        font = ImageFont.truetype("arial.ttf", int(radius * 1.2))
    except IOError:
        font = ImageFont.load_default()
        
    # Pillow moderno usa textbbox para centralizar
    try:
        bbox = draw.textbbox((x, y), str(number), font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text((x - w/2, y - h/2 - 2), str(number), fill="black", font=font)
    except AttributeError:
        # Fallback para versões mais antigas do Pillow
        draw.text((x - 4, y - 6), str(number), fill="black", font=font)

def create_panel(img, grid_size, header_text, theme_color):
    """Cria um painel individual (ex: 2x2, 3x3 ou 4x4) com a imagem base e os recortes."""
    img_size = 300
    img_resized = img.resize((img_size, img_size))
    
    # Configurações de layout do painel
    padding = 20
    gap = 20
    header_h = 40
    patch_gap = 5
    
    # Tamanho total do painel
    panel_w = padding * 3 + img_size * 2 + gap
    panel_h = padding * 2 + header_h + img_size
    
    panel = Image.new('RGB', (panel_w, panel_h), 'white')
    draw = ImageDraw.Draw(panel)
    
    # Desenhar o cabeçalho
    draw.rectangle([padding, padding, panel_w - padding, padding + header_h], fill=theme_color)
    try:
        font_header = ImageFont.truetype("arialbd.ttf", 16)
    except:
        font_header = ImageFont.load_default()
    draw.text((padding + 10, padding + 10), header_text, fill="white", font=font_header)
    
    # Posições de desenho
    left_img_x = padding
    left_img_y = padding + header_h + gap
    right_img_x = padding * 2 + img_size + gap
    right_img_y = left_img_y
    
    # Colar imagem da esquerda (com grid)
    panel.paste(img_resized, (left_img_x, left_img_y))
    
    # Calcular tamanho da célula
    cell_w = img_size // grid_size
    cell_h = img_size // grid_size
    
    # Desenhar linhas do grid na imagem da esquerda e processar os recortes na direita
    patch_idx = 0
    for row in range(grid_size):
        for col in range(grid_size):
            # Coordenadas do bloco atual
            x0 = col * cell_w
            y0 = row * cell_h
            x1 = x0 + cell_w
            y1 = y0 + cell_h
            
            # Recortar o bloco
            patch = img_resized.crop((x0, y0, x1, y1))
            
            # Calcular posição do bloco na grade da direita (com espaçamento)
            # Para caber no mesmo espaço de 300x300, encolhemos levemente os patches
            patch_draw_size = (img_size - (grid_size - 1) * patch_gap) // grid_size
            patch = patch.resize((patch_draw_size, patch_draw_size))
            
            px = right_img_x + col * (patch_draw_size + patch_gap)
            py = right_img_y + row * (patch_draw_size + patch_gap)
            
            # Colar recorte na direita
            panel.paste(patch, (px, py))
            
            # Adicionar numeração no recorte da direita
            draw_numbered_circle(draw, px + 15, py + 15, patch_idx, radius=10)
            
            # Adicionar numeração na imagem da esquerda
            center_left_x = left_img_x + x0 + cell_w // 2
            center_left_y = left_img_y + y0 + cell_h // 2
            draw_numbered_circle(draw, center_left_x, center_left_y, patch_idx, radius=12)
            
            patch_idx += 1
            
    # Desenhar as linhas do grid sobre a imagem da esquerda
    for i in range(1, grid_size):
        # Linhas verticais
        lx = left_img_x + i * cell_w
        draw.line([(lx, left_img_y), (lx, left_img_y + img_size)], fill=theme_color, width=2)
        # Linhas horizontais
        ly = left_img_y + i * cell_h
        draw.line([(left_img_x, ly), (left_img_x + img_size, ly)], fill=theme_color, width=2)
        
    return panel

def generate_grid_comparison_image(input_image_path, output_path="output_grid_comparison.jpg"):
    """Gera a imagem final combinando os painéis A, B e C."""
    try:
        base_img = Image.open(input_image_path).convert('RGB')
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        return

    # Criar os três painéis baseados em grid_2.jpg
    panel_a = create_panel(base_img, 2, "(A) Divisao em 4 partes (2x2) - Grid 4", "#6E9C4E") # Verde
    panel_b = create_panel(base_img, 3, "(B) Divisao em 9 partes (3x3) - Grid 9", "#EE8A25") # Laranja
    panel_c = create_panel(base_img, 4, "(C) Divisao em 16 partes (4x4) - Grid 16", "#3A7EB7") # Azul
        
    # Combinar os painéis lado a lado
    total_width = panel_a.width + panel_b.width + panel_c.width
    max_height = max(panel_a.height, panel_b.height, panel_c.height)
    
    final_image = Image.new('RGB', (total_width, max_height), 'white')
    
    final_image.paste(panel_a, (0, 0))
    final_image.paste(panel_b, (panel_a.width, 0))
    final_image.paste(panel_c, (panel_a.width + panel_b.width, 0))
    
    # Salvar resultado
    final_image.save(output_path, quality=95)
    print(f"Imagem gerada com sucesso em: {output_path}")

# --- Execução ---
# Substitua 'sua_imagem.jpg' pelo caminho da foto do seu colorímetro.
generate_grid_comparison_image('/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Dataset_RL/pele/pele 2353.3.jpg', 
                            output_path='/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/imagens paper/grid_comparison.jpg')