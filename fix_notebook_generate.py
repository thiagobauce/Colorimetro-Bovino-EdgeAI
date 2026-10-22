import json

notebook_path = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/VisionReasoner_PromptLearning.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if any("def pedir_bbox_vlm" in line for line in source):
            new_source = []
            for line in source:
                if "def pedir_bbox_vlm(image_path, prompt_text):" in line:
                    new_source.append(line)
                    new_source.append("    from PIL import Image\n")
                    new_source.append("    image = Image.open(image_path).convert('RGB')\n")
                    new_source.append("    result = model.detect_objects(image, prompt_text)\n")
                    new_source.append("    if result and 'bboxes' in result and len(result['bboxes']) > 0:\n")
                    new_source.append("        return tuple(result['bboxes'][0])\n")
                    new_source.append("    \n")
                    new_source.append("    # Fallback:\n")
                    new_source.append("    resposta_texto = result.get('full_response', '')\n")
                elif "resposta_texto = model.generate(image_path, prompt_text)" in line:
                    pass # We already added the replacement
                else:
                    new_source.append(line)
            cell['source'] = new_source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully.")
