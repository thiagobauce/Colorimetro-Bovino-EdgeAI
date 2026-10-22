import json

notebook_path = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/VisionReasoner_PromptLearning.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_prompts_code = """    # Prompts iniciais (Seed)
    return {
        "p1": {
            "texto": "Analyze this image of cattle skin inside a circular PVC pipe. Find the precise bounding box of the exposed dark skin patch in the center. Ignore white labels. Return the coordinates as [x1, y1, x2, y2].",
            "recompensas": []
        },
        "p2": {
            "texto": "Identify the central dark spot (hair or skin) within the circular area. Disregard any alphanumeric tags. Output bounding box format: [x1, y1, x2, y2].",
            "recompensas": []
        },
        "p3": {
            "texto": "Find the dark skin lesion or hair sample inside the PVC pipe hole. Provide the bounding box coordinates [x1, y1, x2, y2] strictly for the biological sample, ignoring the white background and text.",
            "recompensas": []
        },
        "p4": {
            "texto": "Detect the central biological specimen (dark skin/hair). Focus only on the circular opening. Do not detect the PVC pipe or the printed text labels. Format: [x1, y1, x2, y2].",
            "recompensas": []
        },
        "p5": {
            "texto": "Locate the dark region of interest in the center of the image. The object is a cattle skin patch. Return its bounding box [x1, y1, x2, y2].",
            "recompensas": []
        }
    }"""

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if any("def carregar_prompts():" in line for line in source):
            # Encontrar onde começa "# Prompts iniciais (Seed)"
            start_idx = -1
            for i, line in enumerate(source):
                if "# Prompts iniciais (Seed)" in line:
                    start_idx = i
                    break
            
            if start_idx != -1:
                # Substituir tudo depois disso
                new_source = source[:start_idx]
                # Separar as linhas de new_prompts_code
                lines = new_prompts_code.split('\n')
                for i in range(len(lines)):
                    lines[i] = lines[i] + ('\n' if i < len(lines)-1 else '')
                
                new_source.extend(lines)
                
                # Mas precisamos preservar o resto da célula se houver outras funções
                # Na célula atual, salvar_prompts() vem depois de return {}
                # Então, o jeito mais seguro é reescrever a célula inteira.

# O código acima era arriscado. Vamos reescrever a célula que contém "def carregar_prompts():" por completo
nova_celula = [
    "# ==========================================\n",
    "# 2. GERENCIAMENTO DO POOL DE PROMPTS (RL)\n",
    "# ==========================================\n",
    "def carregar_prompts():\n",
    "    if os.path.exists(ARQUIVO_PROMPTS):\n",
    "        with open(ARQUIVO_PROMPTS, 'r') as f:\n",
    "            return json.load(f)\n",
    "    \n",
    "    # Prompts iniciais (Seed)\n",
    "    return {\n",
    "        \"p1\": {\n",
    "            \"texto\": \"Analyze this image of cattle skin inside a circular PVC pipe. Find the precise bounding box of the exposed dark skin patch in the center. Ignore white labels. Return the coordinates as [x1, y1, x2, y2].\",\n",
    "            \"recompensas\": []\n",
    "        },\n",
    "        \"p2\": {\n",
    "            \"texto\": \"Identify the central dark spot (hair or skin) within the circular area. Disregard any alphanumeric tags. Output bounding box format: [x1, y1, x2, y2].\",\n",
    "            \"recompensas\": []\n",
    "        },\n",
    "        \"p3\": {\n",
    "            \"texto\": \"Find the dark skin lesion or hair sample inside the PVC pipe hole. Provide the bounding box coordinates [x1, y1, x2, y2] strictly for the biological sample, ignoring the white background and text.\",\n",
    "            \"recompensas\": []\n",
    "        },\n",
    "        \"p4\": {\n",
    "            \"texto\": \"Detect the central biological specimen (dark skin/hair). Focus only on the circular opening. Do not detect the PVC pipe or the printed text labels. Format: [x1, y1, x2, y2].\",\n",
    "            \"recompensas\": []\n",
    "        },\n",
    "        \"p5\": {\n",
    "            \"texto\": \"Locate the dark region of interest in the center of the image. The object is a cattle skin patch. Return its bounding box [x1, y1, x2, y2].\",\n",
    "            \"recompensas\": []\n",
    "        }\n",
    "    }\n",
    "\n",
    "def salvar_prompts(pool):\n",
    "    with open(ARQUIVO_PROMPTS, 'w') as f:\n",
    "        json.dump(pool, f, indent=4)\n",
    "\n",
    "def selecionar_prompt(pool):\n",
    "    \"\"\"\n",
    "    Epsilon-Greedy: 70% de chance de usar o melhor prompt (Exploitation), \n",
    "    30% de chance de explorar outros prompts (Exploration).\n",
    "    \"\"\"\n",
    "    chaves = list(pool.keys())\n",
    "    \n",
    "    # Calcula media de reward de cada prompt\n",
    "    medias = {}\n",
    "    for k, v in pool.items():\n",
    "        if len(v['recompensas']) > 0:\n",
    "            medias[k] = np.mean(v['recompensas'])\n",
    "        else:\n",
    "            medias[k] = 1.0 # Prompts novos começam com prioridade alta\n",
    "            \n",
    "    max_val = max(medias.values())\n",
    "    melhores = [k for k, v in medias.items() if v == max_val]\n",
    "    import random\n",
    "    melhor_prompt = random.choice(melhores)\n",
    "    \n",
    "    if random.random() < 0.7:\n",
    "        return melhor_prompt, pool[melhor_prompt]['texto']\n",
    "    else:\n",
    "        escolha = random.choice(chaves)\n",
    "        return escolha, pool[escolha]['texto']"
]

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if any("def carregar_prompts():" in line for line in source):
            cell['source'] = nova_celula
            break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook cell updated with 5 seed prompts.")
