import os
import cv2
import json
import re
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from scipy.stats import pearsonr
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')

caminhos_planilhas = [
    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/colorimetro_dezembro_2025.csv',
    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/colorimetro_fevereiro_2026.csv',
    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/colorimetro_julho_2026.csv'
]

caminhos_fotos = [
    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/fotos colorímetro-dezembro-2025',
    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Fotos colorímetro- fevereiro-2026',
    '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Foto colorimetro-Julho2026'
]

def carregar_planilhas(caminhos):
    dfs = []
    for p in caminhos:
        try:
            temp = pd.read_csv(p, encoding='utf-8')
            if 'dezembro' in p.lower(): temp['Mes'] = 'dezembro'
            elif 'fevereiro' in p.lower(): temp['Mes'] = 'fevereiro'
            elif 'julho' in p.lower(): temp['Mes'] = 'julho'
            else: temp['Mes'] = 'desconhecido'
            dfs.append(temp)
        except Exception as e:
            print(f"Erro ao carregar {p}: {e}")

    if not dfs: return pd.DataFrame()

    df_final = pd.concat(dfs, ignore_index=True)
    df_final = df_final.dropna(subset=['ANIMAL'])
    df_final['ANIMAL'] = df_final['ANIMAL'].astype(float).astype(int).astype(str)

    cols_lab = ['pelo_L', 'pelo_a', 'pelo_b', 'pele_L', 'pele_a', 'pele_b']
    for c in cols_lab: df_final[c] = pd.to_numeric(df_final[c], errors='coerce')

    return df_final

def get_grid_features(crop_bgr, num_partes=9):
    if crop_bgr.size == 0: return []
    
    crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
    crop_hsv = cv2.cvtColor(crop_rgb, cv2.COLOR_RGB2HSV)
    crop_lab_cv2 = cv2.cvtColor(crop_rgb, cv2.COLOR_RGB2LAB)

    grid = int(np.sqrt(num_partes))
    h_c, w_c = crop_rgb.shape[:2]
    step_h, step_w = h_c // grid, w_c // grid

    lista_features = []
    for i in range(grid):
        for j in range(grid):
            y_inicio = i * step_h
            y_fim = (i + 1) * step_h if i < grid - 1 else h_c
            x_inicio = j * step_w
            x_fim = (j + 1) * step_w if j < grid - 1 else w_c

            bloco_rgb = crop_rgb[y_inicio:y_fim, x_inicio:x_fim]
            if bloco_rgb.size == 0: continue

            bloco_hsv = crop_hsv[y_inicio:y_fim, x_inicio:x_fim]
            bloco_lab = crop_lab_cv2[y_inicio:y_fim, x_inicio:x_fim]

            rgb_m = np.mean(bloco_rgb, axis=(0,1))
            hsv_m = np.mean(bloco_hsv, axis=(0,1))
            lab_m = np.mean(bloco_lab, axis=(0,1))

            lista_features.append({
                'R': rgb_m[0], 'G': rgb_m[1], 'B': rgb_m[2],
                'H': hsv_m[0], 'S': hsv_m[1], 'V': hsv_m[2],
                'L_cv2': lab_m[0], 'a_cv2': lab_m[1], 'b_cv2': lab_m[2]
            })
    return lista_features

print("1. Lendo as planilhas do colorímetro...")
df_colorimetro = carregar_planilhas(caminhos_planilhas)

print("2. Carregando json com coordenadas (rl_feedback.json)...")
with open('/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/rl_feedback.json', 'r', encoding='utf-8') as f:
    rl_feedback = json.load(f)

# Group images by (animal_id, mes_atual)
agrupamento = {}
for pasta_atual in caminhos_fotos:
    if not os.path.exists(pasta_atual): continue
    if 'dezembro' in pasta_atual.lower(): mes_atual = 'dezembro'
    elif 'fevereiro' in pasta_atual.lower(): mes_atual = 'fevereiro'
    elif 'julho' in pasta_atual.lower(): mes_atual = 'julho'
    else: mes_atual = 'desconhecido'
    
    for arquivo in os.listdir(pasta_atual):
        if not arquivo.lower().endswith(('.jpg', '.png', '.jpeg')): continue
        match = re.search(r'\d+', arquivo)
        if not match: continue
        animal_id = match.group()
        
        tipo = "pele" if "pele" in arquivo.lower() else "pelo"
        
        chave = (animal_id, mes_atual)
        if chave not in agrupamento:
            agrupamento[chave] = {'pele': None, 'pelo': None, 'pele_arquivo': None}
        
        caminho_completo = os.path.join(pasta_atual, arquivo)
        agrupamento[chave][tipo] = caminho_completo
        if tipo == 'pele':
            agrupamento[chave]['pele_arquivo'] = arquivo

print(f"Encontrados {len(agrupamento)} pares (ou parciais) de imagens.")

dataset_final = []
erro_coords = 0
erro_img = 0

for (animal_id, mes_atual), imgs in agrupamento.items():
    if not imgs['pele']:
        continue # Não tem a pele para pegar a coordenada
        
    arquivo_pele = imgs['pele_arquivo']
    if arquivo_pele not in rl_feedback:
        erro_coords += 1
        continue
        
    entry = rl_feedback[arquivo_pele]
    coords = entry.get('gt_coords', entry.get('auto_coords'))
    if not coords or len(coords) != 4:
        erro_coords += 1
        continue
        
    x1, y1, x2, y2 = [int(v) for v in coords]
    
    linha = df_colorimetro[(df_colorimetro['ANIMAL'] == animal_id) & (df_colorimetro['Mes'] == mes_atual)]
    if linha.empty: continue
    
    # Processar Pele
    l_pele, a_pele, b_pele = linha[['pele_L', 'pele_a', 'pele_b']].iloc[0]
    if not pd.isna(l_pele):
        img_bgr = cv2.imread(imgs['pele'])
        if img_bgr is not None:
            # Garante que os limites estão dentro da imagem
            h_img, w_img = img_bgr.shape[:2]
            c_y1, c_y2 = max(0, y1), min(h_img, y2)
            c_x1, c_x2 = max(0, x1), min(w_img, x2)
            if c_y2 > c_y1 and c_x2 > c_x1:
                crop = img_bgr[c_y1:c_y2, c_x1:c_x2]
                features_lista = get_grid_features(crop)
                for f in features_lista:
                    f.update({
                        'ANIMAL': animal_id, 'L': l_pele, 'a': a_pele, 'b': b_pele, 'Tipo_Pele': 1
                    })
                    dataset_final.append(f)
            else: erro_img += 1
        else: erro_img += 1

    # Processar Pelo (usando a mesma coordenada!)
    if imgs['pelo']:
        l_pelo, a_pelo, b_pelo = linha[['pelo_L', 'pelo_a', 'pelo_b']].iloc[0]
        if not pd.isna(l_pelo):
            img_bgr = cv2.imread(imgs['pelo'])
            if img_bgr is not None:
                h_img, w_img = img_bgr.shape[:2]
                c_y1, c_y2 = max(0, y1), min(h_img, y2)
                c_x1, c_x2 = max(0, x1), min(w_img, x2)
                if c_y2 > c_y1 and c_x2 > c_x1:
                    crop = img_bgr[c_y1:c_y2, c_x1:c_x2]
                    features_lista = get_grid_features(crop)
                    for f in features_lista:
                        f.update({
                            'ANIMAL': animal_id, 'L': l_pelo, 'a': a_pelo, 'b': b_pelo, 'Tipo_Pele': 0
                        })
                        dataset_final.append(f)
                else: erro_img += 1
            else: erro_img += 1

df_ml = pd.DataFrame(dataset_final)
print(f"Dataset montado com {len(df_ml)} amostras (blocos do grid).")

print("\\n=======================================================")
print("             ESTATÍSTICA DESCRITIVA                     ")
print("=======================================================")
desc_cols = ['L', 'a', 'b']
print("--- PELE ---")
print(df_ml[df_ml['Tipo_Pele']==1][desc_cols].describe().loc[['mean', 'std', 'min', 'max']].T)
print("\\n--- PELO ---")
print(df_ml[df_ml['Tipo_Pele']==0][desc_cols].describe().loc[['mean', 'std', 'min', 'max']].T)

if len(df_ml) > 0:
    colunas_x = ['R', 'G', 'B', 'H', 'S', 'V', 'L_cv2', 'a_cv2', 'b_cv2', 'Tipo_Pele']
    X = df_ml[colunas_x]
    y = df_ml[['L', 'a', 'b']]
    grupos = df_ml['ANIMAL']

    separador = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    indice_treino, indice_teste = next(separador.split(X, y, groups=grupos))

    X_train, X_test = X.iloc[indice_treino], X.iloc[indice_teste]
    y_train, y_test = y.iloc[indice_treino], y.iloc[indice_teste]

    config_xgb = {
        'n_estimators': 600,
        'learning_rate': 0.05,
        'max_depth': 20,
        'random_state': 42,
        'tree_method': 'hist',
        'device': 'cuda'
    }

    modelo_L = Pipeline([('scaler', StandardScaler()), ('xgb', XGBRegressor(**config_xgb))])
    modelo_a = Pipeline([('scaler', StandardScaler()), ('xgb', XGBRegressor(**config_xgb))])
    modelo_b = Pipeline([('scaler', StandardScaler()), ('xgb', XGBRegressor(**config_xgb))])

    print("\\nTreinando modelos (XGBoost)...")
    modelo_L.fit(X_train, y_train['L'])
    modelo_a.fit(X_train, y_train['a'])
    modelo_b.fit(X_train, y_train['b'])

    prev_L = modelo_L.predict(X_test)
    prev_a = modelo_a.predict(X_test)
    prev_b = modelo_b.predict(X_test)

    # Calculando as métricas
    y_L = y_test['L'].values
    y_a = y_test['a'].values
    y_b = y_test['b'].values

    mae_L = mean_absolute_error(y_L, prev_L)
    mae_a = mean_absolute_error(y_a, prev_a)
    mae_b = mean_absolute_error(y_b, prev_b)

    r2_L = r2_score(y_L, prev_L)
    r2_a = r2_score(y_a, prev_a)
    r2_b = r2_score(y_b, prev_b)

    rmse_L = np.sqrt(mean_squared_error(y_L, prev_L))
    rmse_a = np.sqrt(mean_squared_error(y_a, prev_a))
    rmse_b = np.sqrt(mean_squared_error(y_b, prev_b))

    pearson_L, _ = pearsonr(y_L, prev_L)
    pearson_a, _ = pearsonr(y_a, prev_a)
    pearson_b, _ = pearsonr(y_b, prev_b)

    # Delta E
    delta_e = np.sqrt((y_L - prev_L)**2 + (y_a - prev_a)**2 + (y_b - prev_b)**2)
    delta_e_mean = np.mean(delta_e)

    # Bland-Altman
    bias_L = np.mean(prev_L - y_L)
    sd_L = np.std(prev_L - y_L)
    loa_L = (bias_L - 1.96*sd_L, bias_L + 1.96*sd_L)

    bias_a = np.mean(prev_a - y_a)
    sd_a = np.std(prev_a - y_a)
    loa_a = (bias_a - 1.96*sd_a, bias_a + 1.96*sd_a)

    bias_b = np.mean(prev_b - y_b)
    sd_b = np.std(prev_b - y_b)
    loa_b = (bias_b - 1.96*sd_b, bias_b + 1.96*sd_b)

    print("\\n=======================================================")
    print("             MÉTRICAS DE AVALIAÇÃO (CONJUNTO DE TESTE) ")
    print("=======================================================")
    print(f"Erro Médio Absoluto (MAE): L*={mae_L:.3f} | a*={mae_a:.3f} | b*={mae_b:.3f}")
    print(f"Coeficiente de Determinação (R2): L*={r2_L:.3f} | a*={r2_a:.3f} | b*={r2_b:.3f}")
    print(f"Raiz do Erro Quadrático Médio (RMSE): L*={rmse_L:.3f} | a*={rmse_a:.3f} | b*={rmse_b:.3f}")
    print(f"Coeficiente de Correlação (r): L*={pearson_L:.3f} | a*={pearson_a:.3f} | b*={pearson_b:.3f}")
    print(f"Diferença de Cor (Delta E) Médio: {delta_e_mean:.3f}")
    print("\\n--- ANÁLISE DE BLAND-ALTMAN ---")
    print(f"L* -> Viés: {bias_L:.3f} | Limites de Concordância 95%: ({loa_L[0]:.3f}, {loa_L[1]:.3f})")
    print(f"a* -> Viés: {bias_a:.3f} | Limites de Concordância 95%: ({loa_a[0]:.3f}, {loa_a[1]:.3f})")
    print(f"b* -> Viés: {bias_b:.3f} | Limites de Concordância 95%: ({loa_b[0]:.3f}, {loa_b[1]:.3f})")
    print("=======================================================")
else:
    print("Nenhum dado encontrado para treino.")
