import json

notebook_path = 'VisionReasoner_PromptLearning.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The install cell is at index 1
source = nb['cells'][1]['source']
for i, line in enumerate(source):
    if line.startswith("!") and "pip install" in line:
        source[i] = "!{sys.executable} -m pip install transformers sam2 openai ultralytics"

nb['cells'][1]['source'] = source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook pip dependencies updated.")
