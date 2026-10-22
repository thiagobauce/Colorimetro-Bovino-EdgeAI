import json

notebook_path = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/VisionReasoner_PromptLearning.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        for i, line in enumerate(source):
            if "from vision_reasoner.models.vision_reasoner_model import VisionReasoner\n" == line or "from vision_reasoner.models.vision_reasoner_model import VisionReasoner" == line:
                source[i] = line.replace("VisionReasoner", "VisionReasonerModel")
            elif "model = VisionReasoner.from_pretrained" in line:
                source[i] = line.replace("model = VisionReasoner.from_pretrained(", "model = VisionReasonerModel(reasoning_model_path=")

        cell['source'] = source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully.")
