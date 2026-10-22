import json

notebook_path = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/VisionReasoner_PromptLearning.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if any("def selecionar_prompt(pool):" in line for line in source):
            new_source = []
            skip = False
            for line in source:
                if "melhor_prompt = max(medias, key=medias.get)" in line:
                    new_source.append("    max_val = max(medias.values())\n")
                    new_source.append("    melhores = [k for k, v in medias.items() if v == max_val]\n")
                    new_source.append("    melhor_prompt = random.choice(melhores)\n")
                else:
                    new_source.append(line)
            cell['source'] = new_source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully with random selection for tied prompts.")
