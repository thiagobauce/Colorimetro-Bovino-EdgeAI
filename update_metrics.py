import json
import re

notebook_path = '/media/workstation_2x_3080/HD 1TB/Famez_yolo/Colorímetro/Colorimetro_Clean.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

metrics_code_str = """
    prev_L = previsoes[:,0]
    prev_a = previsoes[:,1]
    prev_b = previsoes[:,2]

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

    from scipy.stats import pearsonr
    pearson_L, _ = pearsonr(y_L, prev_L)
    pearson_a, _ = pearsonr(y_a, prev_a)
    pearson_b, _ = pearsonr(y_b, prev_b)

    delta_e = np.sqrt((y_L - prev_L)**2 + (y_a - prev_a)**2 + (y_b - prev_b)**2)
    delta_e_mean = np.mean(delta_e)

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
    print("\\n[Erro] Não há dados suficientes para treinar a IA.")
"""

# Format into a list of lines keeping the newlines for json source format
metrics_code = [line + '\n' for line in metrics_code_str.split('\n')]
# Remove the very first empty line if present
if metrics_code[0] == '\n':
    metrics_code = metrics_code[1:]

for cell in nb.get('cells', []):
    if cell['cell_type'] == 'code':
        source_str = "".join(cell['source'])
        if "previsoes = modelo.predict(X_test)" in source_str and "erro_l = mean_absolute_error" in source_str:
            # Find the index of "previsoes = modelo.predict(X_test)"
            idx = -1
            for i, line in enumerate(cell['source']):
                if "previsoes = modelo.predict(X_test)" in line:
                    idx = i
                    break
            
            if idx != -1:
                # Keep lines up to and including previsoes = modelo.predict(X_test)
                new_source = cell['source'][:idx+1]
                # Append the new metrics code
                new_source.extend(metrics_code)
                cell['source'] = new_source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Métricas adicionadas a todos os modelos com sucesso!")
