import json

notebook_path = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/VisionReasoner_PromptLearning.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if any("def selecionar_prompt(pool):" in line for line in source):
            # Encontrar onde começa def selecionar_prompt
            start_idx = -1
            for i, line in enumerate(source):
                if "def selecionar_prompt(pool):" in line:
                    start_idx = i
                    break
            
            if start_idx != -1:
                # Manter apenas até antes de selecionar_prompt
                cell['source'] = source[:start_idx]
            break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook cell 2 cleaned up.")
