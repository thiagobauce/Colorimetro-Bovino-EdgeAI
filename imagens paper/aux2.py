import os
from PIL import Image, ImageDraw, ImageFont

def draw_numbered_circle(draw, x, y, number, radius=12):
    """Desenha um círculo branco com um número preto no centro."""
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="white")
    
    # Tenta usar a fonte Arial (padrão Windows), senão usa a fonte padrão da biblioteca
    try:
        font = ImageFont.truetype("arial.ttf", int(radius * 1.2))
    except IOError:
        font = ImageFont.load_default()
        
    try:
        bbox = draw.textbbox((x, y), str(number), font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text((x - w/2, y - h/2 - 2), str(number), fill="black", font=font)
    except AttributeError:
        # Fallback para versões mais antigas do Pillow
        draw.text((x - 4, y - 6), str(number), fill="black", font=font)

def create_panel(img, img_size, grid_size, header_text, theme_color):
    """Cria os painéis de recorte (A, B ou C)."""
    padding = 15
    gap = 20
    header_h = 40
    patch_gap = 5
    
    panel_w = padding * 3 + img_size * 2 + gap
    panel_h = padding * 2 + header_h + img_size
    
    panel = Image.new('RGB', (panel_w, panel_h), 'white')
    draw = ImageDraw.Draw(panel)
    
    # Desenhar o cabeçalho colorido
    draw.rectangle([padding, padding, panel_w - padding, padding + header_h], fill=theme_color)
    try:
        font_header = ImageFont.truetype("arialbd.ttf", 16)
    except IOError:
        font_header = ImageFont.load_default()
    draw.text((padding + 10, padding + 10), header_text, fill="white", font=font_header)
    
    left_x = padding
    left_y = padding + header_h + gap
    right_x = padding * 2 + img_size + gap
    right_y = left_y
    
    # Colar imagem base no lado esquerdo
    panel.paste(img, (left_x, left_y))
    
    # Calcular tamanhos dos recortes
    cell_w = img_size // grid_size
    cell_h = img_size // grid_size
    
    patch_idx = 0
    for row in range(grid_size):
        for col in range(grid_size):
            x0 = col * cell_w
            y0 = row * cell_h
            x1 = x0 + cell_w
            y1 = y0 + cell_h
            
            # Recortar o pedaço (patch) da imagem original
            patch = img.crop((x0, y0, x1, y1))
            
            # Redimensionar patch para caber com o espaçamento na grade da direita
            patch_draw_size = (img_size - (grid_size - 1) * patch_gap) // grid_size
            patch = patch.resize((patch_draw_size, patch_draw_size))
            
            px = right_x + col * (patch_draw_size + patch_gap)
            py = right_y + row * (patch_draw_size + patch_gap)
            
            panel.paste(patch, (px, py))
            
            # Desenhar círculos com números nos recortes (direita)
            draw_numbered_circle(draw, px + 15, py + 15, patch_idx, radius=10)
            
            # Desenhar círculos com números na imagem inteira (esquerda)
            center_left_x = left_x + x0 + cell_w // 2
            center_left_y = left_y + y0 + cell_h // 2
            draw_numbered_circle(draw, center_left_x, center_left_y, patch_idx, radius=12)
            
            patch_idx += 1
            
    # Desenhar as linhas do grid sobre a imagem da esquerda
    for i in range(1, grid_size):
        lx = left_x + i * cell_w
        draw.line([(lx, left_y), (lx, left_y + img_size)], fill=theme_color, width=2)
        ly = left_y + i * cell_h
        draw.line([(left_x, ly), (left_x + img_size, ly)], fill=theme_color, width=2)
        
    return panel

def create_ref_panel(img, img_size):
    """Cria o painel esquerdo inicial 'ROI final (Referência)'."""
    padding = 15
    gap = 20
    header_h = 55 # Mais alto para acomodar texto em duas linhas
    
    panel_w = padding * 2 + img_size
    # Alinhado com a altura dos outros painéis (header_h=40 + gap=20 vs 55 + gap=20)
    panel_h = padding * 2 + 40 + gap + img_size 
    
    panel = Image.new('RGB', (panel_w, panel_h), 'white')
    draw = ImageDraw.Draw(panel)
    
    # Fundo do cabeçalho cinza escuro
    draw.rectangle([padding, padding, panel_w - padding, padding + header_h], fill="#666666")
    try:
        font_header = ImageFont.truetype("arialbd.ttf", 14)
    except:
        font_header = ImageFont.load_default()
        
    draw.text((panel_w//2 - 40, padding + 10), "ROI final\n(Referência)", fill="white", font=font_header, align="center")
    
    # Colar imagem de referência
    left_y = padding + 40 + gap
    panel.paste(img, (padding, left_y)) 
    
    return panel

def generate_pipeline_image(input_image_path, output_path="diagrama_final.jpg"):
    """Função principal: Carrega a foto original e orquestra a geração da imagem completa."""
    if not os.path.exists(input_image_path):
        print(f"ERRO: A imagem '{input_image_path}' não foi encontrada.")
        print("Verifique se o nome está correto e se o arquivo está na mesma pasta do script.")
        return

    print(f"Carregando a imagem '{input_image_path}'...")
    try:
        original_img = Image.open(input_image_path).convert('RGB')
    except Exception as e:
        print(f"Erro ao tentar abrir a imagem: {e}")
        return

    # Definimos um tamanho quadrado fixo para a região de interesse (ROI)
    img_size = 250
    
    # Se a sua imagem original não for quadrada, você pode querer mudar isso
    # para usar .crop() no centro em vez de .resize() para não distorcer.
    base_img = original_img.resize((img_size, img_size))

    print("Gerando painéis...")
    # Gerar cada painel
    panel_ref = create_ref_panel(base_img, img_size)
    panel_a = create_panel(base_img, img_size, 2, "(A) Divisão em 4 partes (2×2) – Grid 4", "#6E9C4E") # Verde
    panel_b = create_panel(base_img, img_size, 3, "(B) Divisão em 9 partes (3×3) – Grid 9", "#EE8A25") # Laranja
    panel_c = create_panel(base_img, img_size, 4, "(C) Divisão em 16 partes (4×4) – Grid 16", "#3A7EB7") # Azul

    # Criar painel da seta preta de fluxo
    arrow_w = 50
    arrow_panel = Image.new('RGB', (arrow_w, panel_a.height), 'white')
    draw_arrow = ImageDraw.Draw(arrow_panel)
    mid_y = panel_a.height // 2 + 30
    draw_arrow.polygon([(5, mid_y-15), (25, mid_y-15), (25, mid_y-25), (45, mid_y), (25, mid_y+25), (25, mid_y+15), (5, mid_y+15)], fill="black")

    print("Montando imagem final...")
    # Juntar todos os elementos na imagem final lado a lado
    total_w = panel_ref.width + arrow_w + panel_a.width + panel_b.width + panel_c.width
    final_img = Image.new('RGB', (total_w, panel_a.height), 'white')

    x_offset = 0
    final_img.paste(panel_ref, (x_offset, 0))
    x_offset += panel_ref.width
    
    final_img.paste(arrow_panel, (x_offset, 0))
    x_offset += arrow_w
    
    final_img.paste(panel_a, (x_offset, 0))
    x_offset += panel_a.width
    
    final_img.paste(panel_b, (x_offset, 0))
    x_offset += panel_b.width
    
    final_img.paste(panel_c, (x_offset, 0))

    # Salvar o resultado
    final_img.save(output_path, quality=95)
    print(f"SUCESSO! O diagrama foi salvo como: '{output_path}'")

# ==============================================================================
# EXECUÇÃO DO SCRIPT
# ==============================================================================
if __name__ == "__main__":
    # ---> COLOQUE O NOME DA SUA IMAGEM AQUI <---
    imagem_de_entrada = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Dataset_RL/pele/pele 2353.3.jpg' 
    
    # Nome do arquivo que será salvo com o diagrama final
    imagem_de_saida = 'pipeline_completo.jpg'
    
    generate_pipeline_image(imagem_de_entrada, imagem_de_saida)