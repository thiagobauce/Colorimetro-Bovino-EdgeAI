import json

notebook_path = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/VisionReasoner_PromptLearning.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if any("caminhos_fotos = [" in line for line in source):
            new_source = []
            for i, line in enumerate(source):
                if line.strip() == "caminhos_fotos = [":
                    new_source.append(line)
                    new_source.append("    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Foto colorimetro-Julho2026',\n")
                    new_source.append("    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Fotos colorímetro- fevereiro-2026',\n")
                    new_source.append("    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/fotos colorímetro-dezembro-2025'\n")
                elif "'/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Foto colorimetro-Julho2026'" in line:
                    pass # We already added it above
                else:
                    new_source.append(line)
            cell['source'] = new_source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully with all 3 folders.")
