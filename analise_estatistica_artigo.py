#!/usr/bin/env python3
"""
==============================================================================
Análise Estatística Completa – Artigo Colorímetro 2025–2026
==============================================================================
Autor: Script gerado automaticamente
Data:  2026-09-24

Métricas calculadas:
  1. Pearson (r)
  2. MAE – Erro Absoluto Médio
  3. RMSE – Raiz do Erro Quadrático Médio
  4. Viés Médio
  5. Viés Linear/Proporcional – Regressão Linear
  6. Bland–Altman (com limites de concordância de 95%)
  7. Robustez Ambiental – relação do erro com TMR, CTR, Temp, %RH, ITGU
  8. Modelo Linear Misto – animal como efeito aleatório, período como efeito fixo
==============================================================================
"""

import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

# ─── Configuração visual ────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
})
sns.set_style("whitegrid")

# ─── Diretório de saída ─────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados_estatisticos')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# 1. CARREGAMENTO E LIMPEZA DOS DADOS
# ============================================================================
print("=" * 70)
print("CARREGAMENTO DOS DADOS")
print("=" * 70)

EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'dados artigo colorimetro 2025 - 2026 (1).xlsx')

df_raw = pd.read_excel(EXCEL_PATH, sheet_name='2025 a 2026')

# Remover colunas sem nome (artefatos do Excel)
df = df_raw[[c for c in df_raw.columns if not c.startswith('Unnamed')]].copy()

# Remover linhas sem Animal (linhas em branco no final do Excel)
df = df.dropna(subset=['Animal']).reset_index(drop=True)

# Converter Animal para inteiro
df['Animal'] = df['Animal'].astype(int).astype(str)

# Converter colunas pelo_app para numérico
for col in ['L_pelo_app', 'a_pelo_app', 'b_pelo_app']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Padronizar período
df['período'] = df['período'].str.strip().str.capitalize()

print(f"  Linhas válidas: {len(df)}")
print(f"  Animais únicos: {df['Animal'].nunique()}")
print(f"  Períodos: {df['período'].unique()}")
print(f"  Colunas: {list(df.columns)}")
print()

# ─── Definição de pares (referência vs. app) ────────────────────────────────
# _colo = colorímetro de bancada (referência)
# _app  = aplicativo/câmera (método em avaliação)

PAIRS = {
    'L_pele': ('L_pele_colo', 'L_pele_app'),
    'a_pele': ('a_pele_colo', 'a_pele_app'),
    'b_pele': ('b_pele_colo', 'b_pele_app'),
    'L_pelo': ('L_pelo_colo', 'L_pelo_app'),
    'a_pelo': ('a_pelo_colo', 'a_pelo_app'),
    'b_pelo': ('b_pelo_colo', 'b_pelo_app'),
}

# ============================================================================
# 2. PEARSON (r), MAE, RMSE, VIÉS MÉDIO – Para cada variável
# ============================================================================
print("=" * 70)
print("MÉTRICAS DE CONCORDÂNCIA POR VARIÁVEL")
print("=" * 70)

results_list = []

for name, (ref_col, app_col) in PAIRS.items():
    mask = df[ref_col].notna() & df[app_col].notna()
    ref = df.loc[mask, ref_col].values
    app = df.loc[mask, app_col].values
    n = len(ref)

    # Pearson
    r, p_val = stats.pearsonr(ref, app)

    # MAE
    mae = mean_absolute_error(ref, app)

    # RMSE
    rmse = np.sqrt(mean_squared_error(ref, app))

    # Viés médio (app - ref)
    bias = np.mean(app - ref)
    bias_sd = np.std(app - ref, ddof=1)

    results_list.append({
        'Variável': name,
        'N': n,
        'Pearson_r': r,
        'p_value': p_val,
        'MAE': mae,
        'RMSE': rmse,
        'Viés_médio': bias,
        'Viés_DP': bias_sd,
    })

    print(f"\n  ── {name} (n={n}) ──")
    print(f"     Pearson r = {r:.4f}  (p = {p_val:.2e})")
    print(f"     MAE       = {mae:.4f}")
    print(f"     RMSE      = {rmse:.4f}")
    print(f"     Viés      = {bias:+.4f} ± {bias_sd:.4f}")

df_results = pd.DataFrame(results_list)
df_results.to_csv(os.path.join(OUTPUT_DIR, 'metricas_concordancia.csv'), index=False)
print(f"\n  → Salvo em {os.path.join(OUTPUT_DIR, 'metricas_concordancia.csv')}")

# ============================================================================
# 3. VIÉS LINEAR/PROPORCIONAL – Regressão Linear (app = α + β·ref)
# ============================================================================
print("\n" + "=" * 70)
print("VIÉS LINEAR/PROPORCIONAL – REGRESSÃO LINEAR")
print("=" * 70)

reg_results = []

fig_reg, axes_reg = plt.subplots(2, 3, figsize=(18, 12))
axes_reg = axes_reg.ravel()

for i, (name, (ref_col, app_col)) in enumerate(PAIRS.items()):
    mask = df[ref_col].notna() & df[app_col].notna()
    ref = df.loc[mask, ref_col].values
    app = df.loc[mask, app_col].values

    # Regressão OLS: app = α + β * ref
    slope, intercept, r_value, p_value, std_err = stats.linregress(ref, app)

    # Teste se β ≠ 1 (viés proporcional)
    t_stat_slope = (slope - 1.0) / std_err
    p_slope_diff_1 = 2 * stats.t.sf(abs(t_stat_slope), df=len(ref) - 2)

    # Teste se α ≠ 0 (viés constante)
    # Recalcular o SE do intercept
    X_with_const = sm.add_constant(ref)
    model = sm.OLS(app, X_with_const).fit()
    p_intercept = model.pvalues[0]  # p-value do intercepto

    reg_results.append({
        'Variável': name,
        'Intercepto (α)': intercept,
        'p_α≠0': p_intercept,
        'Inclinação (β)': slope,
        'SE_β': std_err,
        'p_β≠1': p_slope_diff_1,
        'R²': r_value ** 2,
    })

    print(f"\n  ── {name} ──")
    print(f"     app = {intercept:.4f} + {slope:.4f} × ref")
    print(f"     R² = {r_value**2:.4f}")
    print(f"     Intercepto: α = {intercept:.4f} (p_α≠0 = {p_intercept:.4f})")
    print(f"     Inclinação:  β = {slope:.4f} ± {std_err:.4f} (p_β≠1 = {p_slope_diff_1:.4f})")
    if p_slope_diff_1 < 0.05:
        print(f"     ⚠ Viés proporcional significativo (β ≠ 1)")
    else:
        print(f"     ✓ Sem viés proporcional (β ≈ 1)")
    if p_intercept < 0.05:
        print(f"     ⚠ Viés constante significativo (α ≠ 0)")
    else:
        print(f"     ✓ Sem viés constante (α ≈ 0)")

    # Gráfico
    ax = axes_reg[i]
    ax.scatter(ref, app, alpha=0.4, s=20, color='steelblue', edgecolors='none')
    xlim = ax.get_xlim()
    x_line = np.linspace(xlim[0], xlim[1], 100)
    ax.plot(x_line, x_line, 'k--', linewidth=1, label='Identidade (y=x)')
    ax.plot(x_line, intercept + slope * x_line, 'r-', linewidth=1.5,
            label=f'Regressão: y = {intercept:.2f} + {slope:.3f}x')
    ax.set_xlabel(f'{ref_col} (Referência)')
    ax.set_ylabel(f'{app_col} (App)')
    ax.set_title(f'{name}\nR² = {r_value**2:.3f}  β = {slope:.3f}')
    ax.legend(fontsize=8, loc='upper left')

fig_reg.suptitle('Viés Linear/Proporcional – Regressão: App = α + β × Referência',
                 fontsize=15, fontweight='bold', y=1.02)
fig_reg.tight_layout()
fig_reg.savefig(os.path.join(OUTPUT_DIR, 'regressao_linear.png'), bbox_inches='tight')
plt.close(fig_reg)

df_reg = pd.DataFrame(reg_results)
df_reg.to_csv(os.path.join(OUTPUT_DIR, 'regressao_linear.csv'), index=False)
print(f"\n  → Salvo em {os.path.join(OUTPUT_DIR, 'regressao_linear.csv')}")

# ============================================================================
# 4. ANÁLISE DE BLAND–ALTMAN
# ============================================================================
print("\n" + "=" * 70)
print("ANÁLISE DE BLAND–ALTMAN")
print("=" * 70)

fig_ba, axes_ba = plt.subplots(2, 3, figsize=(18, 12))
axes_ba = axes_ba.ravel()

ba_results = []

for i, (name, (ref_col, app_col)) in enumerate(PAIRS.items()):
    mask = df[ref_col].notna() & df[app_col].notna()
    ref = df.loc[mask, ref_col].values
    app = df.loc[mask, app_col].values

    mean_val = (ref + app) / 2.0
    diff = app - ref  # diferença: app - referência

    bias = np.mean(diff)
    sd_diff = np.std(diff, ddof=1)
    loa_upper = bias + 1.96 * sd_diff
    loa_lower = bias - 1.96 * sd_diff

    # Teste t para viés ≠ 0
    t_stat, p_bias = stats.ttest_1samp(diff, 0)

    # Teste de proporcionalidade do erro (correlação entre média e diferença)
    r_prop, p_prop = stats.pearsonr(mean_val, diff)

    ba_results.append({
        'Variável': name,
        'Viés_médio': bias,
        'DP_diferenças': sd_diff,
        'LoA_inferior': loa_lower,
        'LoA_superior': loa_upper,
        'p_viés≠0': p_bias,
        'r_proporcionalidade': r_prop,
        'p_proporcionalidade': p_prop,
    })

    print(f"\n  ── {name} ──")
    print(f"     Viés médio: {bias:+.4f} (p = {p_bias:.4f})")
    print(f"     DP das diferenças: {sd_diff:.4f}")
    print(f"     Limites de concordância (95%):")
    print(f"       Inferior: {loa_lower:.4f}")
    print(f"       Superior: {loa_upper:.4f}")
    print(f"     Proporcionalidade: r = {r_prop:.4f} (p = {p_prop:.4f})")

    # Gráfico
    ax = axes_ba[i]
    ax.scatter(mean_val, diff, alpha=0.4, s=20, color='steelblue', edgecolors='none')
    ax.axhline(bias, color='red', linestyle='-', linewidth=1.5, label=f'Viés = {bias:+.2f}')
    ax.axhline(loa_upper, color='orange', linestyle='--', linewidth=1, label=f'+1.96 DP = {loa_upper:.2f}')
    ax.axhline(loa_lower, color='orange', linestyle='--', linewidth=1, label=f'−1.96 DP = {loa_lower:.2f}')
    ax.axhline(0, color='gray', linestyle=':', linewidth=0.8)

    # Regressão para mostrar tendência proporcional
    if abs(r_prop) > 0.1:
        z = np.polyfit(mean_val, diff, 1)
        p = np.poly1d(z)
        x_sorted = np.sort(mean_val)
        ax.plot(x_sorted, p(x_sorted), 'g-', linewidth=1, alpha=0.7, label='Tendência')

    ax.set_xlabel(f'Média [(Ref + App) / 2]')
    ax.set_ylabel(f'Diferença (App − Ref)')
    ax.set_title(f'Bland–Altman: {name}')
    ax.legend(fontsize=7, loc='best')

fig_ba.suptitle('Análise de Bland–Altman', fontsize=15, fontweight='bold', y=1.02)
fig_ba.tight_layout()
fig_ba.savefig(os.path.join(OUTPUT_DIR, 'bland_altman.png'), bbox_inches='tight')
plt.close(fig_ba)

df_ba = pd.DataFrame(ba_results)
df_ba.to_csv(os.path.join(OUTPUT_DIR, 'bland_altman.csv'), index=False)
print(f"\n  → Salvo em {os.path.join(OUTPUT_DIR, 'bland_altman.csv')}")

# ============================================================================
# 5. ROBUSTEZ AMBIENTAL – Relação do Erro com TMR, CTR, Temp, %RH, ITGU
# ============================================================================
print("\n" + "=" * 70)
print("ROBUSTEZ AMBIENTAL – CORRELAÇÃO ERRO vs. CONDIÇÕES AMBIENTAIS")
print("=" * 70)

ENV_VARS = {
    'TMR': 'TMR',
    'CTR': 'CTR (W/m²)',
    'Temperatura': 'Temp °C Média',
    'Umidade_Relativa': '%RH',
    'ITGU': 'MÉDIA ITGU',
}

# Calcular erros absolutos para cada variável
for name, (ref_col, app_col) in PAIRS.items():
    df[f'erro_abs_{name}'] = (df[app_col] - df[ref_col]).abs()
    df[f'erro_{name}'] = df[app_col] - df[ref_col]

# Delta E (pele e pelo)
df['DeltaE_pele'] = np.sqrt(
    (df['L_pele_app'] - df['L_pele_colo'])**2 +
    (df['a_pele_app'] - df['a_pele_colo'])**2 +
    (df['b_pele_app'] - df['b_pele_colo'])**2
)
df['DeltaE_pelo'] = np.sqrt(
    (df['L_pelo_app'] - df['L_pelo_colo'])**2 +
    (df['a_pelo_app'] - df['a_pelo_colo'])**2 +
    (df['b_pelo_app'] - df['b_pelo_colo'])**2
)

error_vars = [f'erro_abs_{name}' for name in PAIRS.keys()] + ['DeltaE_pele', 'DeltaE_pelo']

rob_results = []

for env_label, env_col in ENV_VARS.items():
    print(f"\n  ── {env_label} ({env_col}) ──")
    for err_col in error_vars:
        mask = df[env_col].notna() & df[err_col].notna()
        if mask.sum() < 10:
            continue
        env_vals = df.loc[mask, env_col].values
        err_vals = df.loc[mask, err_col].values

        r, p = stats.pearsonr(env_vals, err_vals)
        rho, p_rho = stats.spearmanr(env_vals, err_vals)

        rob_results.append({
            'Var_ambiental': env_label,
            'Var_erro': err_col,
            'N': int(mask.sum()),
            'Pearson_r': r,
            'p_Pearson': p,
            'Spearman_rho': rho,
            'p_Spearman': p_rho,
        })

        sig_mark = '*' if p < 0.05 else ''
        print(f"     {err_col:25s}  r={r:+.4f} (p={p:.4f}){sig_mark}  "
              f"ρ={rho:+.4f} (p={p_rho:.4f})")

df_rob = pd.DataFrame(rob_results)
df_rob.to_csv(os.path.join(OUTPUT_DIR, 'robustez_ambiental.csv'), index=False)

# ─── Gráficos de Robustez (heatmap de correlações) ──────────────────────────
# Montar matriz de correlação
corr_matrix = df_rob.pivot(index='Var_erro', columns='Var_ambiental', values='Pearson_r')
p_matrix = df_rob.pivot(index='Var_erro', columns='Var_ambiental', values='p_Pearson')

fig_heat, ax_heat = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
            vmin=-0.5, vmax=0.5, ax=ax_heat, linewidths=0.5,
            cbar_kws={'label': 'Correlação de Pearson (r)'})

# Marcar significância
for y_idx, err_var in enumerate(corr_matrix.index):
    for x_idx, env_var in enumerate(corr_matrix.columns):
        p_val = p_matrix.loc[err_var, env_var]
        if pd.notna(p_val) and p_val < 0.05:
            ax_heat.text(x_idx + 0.5, y_idx + 0.85, '★', ha='center', va='center',
                        fontsize=8, color='black')

ax_heat.set_title('Robustez Ambiental: Correlação entre Erro e Condições Ambientais\n'
                  '(★ = p < 0.05)', fontsize=13, fontweight='bold')
ax_heat.set_ylabel('Variável de Erro')
ax_heat.set_xlabel('Variável Ambiental')
fig_heat.tight_layout()
fig_heat.savefig(os.path.join(OUTPUT_DIR, 'robustez_heatmap.png'), bbox_inches='tight')
plt.close(fig_heat)

# ─── Gráficos de dispersão Erro vs. Ambiente ────────────────────────────────
fig_env, axes_env = plt.subplots(5, 2, figsize=(14, 25))

for row_idx, (env_label, env_col) in enumerate(ENV_VARS.items()):
    for col_idx, de_col in enumerate(['DeltaE_pele', 'DeltaE_pelo']):
        ax = axes_env[row_idx, col_idx]
        mask = df[env_col].notna() & df[de_col].notna()
        if mask.sum() < 10:
            ax.set_visible(False)
            continue
        x = df.loc[mask, env_col].values
        y = df.loc[mask, de_col].values
        r, p = stats.pearsonr(x, y)

        ax.scatter(x, y, alpha=0.4, s=25, color='steelblue', edgecolors='none')
        # Linha de tendência
        z = np.polyfit(x, y, 1)
        poly = np.poly1d(z)
        x_sorted = np.sort(x)
        ax.plot(x_sorted, poly(x_sorted), 'r-', linewidth=1.5)

        ax.set_xlabel(env_label)
        ax.set_ylabel(de_col)
        ax.set_title(f'{de_col} vs. {env_label}\nr = {r:.3f} (p = {p:.4f})')

fig_env.suptitle('Robustez Ambiental: ΔE vs. Condições Ambientais',
                 fontsize=15, fontweight='bold', y=1.01)
fig_env.tight_layout()
fig_env.savefig(os.path.join(OUTPUT_DIR, 'robustez_dispersao.png'), bbox_inches='tight')
plt.close(fig_env)

print(f"\n  → Salvos em {OUTPUT_DIR}")

# ============================================================================
# 6. MODELO LINEAR MISTO – Animal como efeito aleatório, Período como fixo
# ============================================================================
print("\n" + "=" * 70)
print("MODELO LINEAR MISTO")
print("  Efeito fixo: período")
print("  Efeito aleatório: Animal (intercepto aleatório)")
print("=" * 70)

# Preparar dataframe para modelos mistos
df_lmm = df.copy()
df_lmm['período_cat'] = pd.Categorical(df_lmm['período'])

# Adicionar variáveis ambientais ao modelo de robustez
lmm_results_summary = []
fixed_effects_all = []
lmm_diag = []

# Para cada variável de erro e DeltaE
response_vars = {
    'erro_abs_L_pele': 'Erro absoluto L* pele',
    'erro_abs_a_pele': 'Erro absoluto a* pele',
    'erro_abs_b_pele': 'Erro absoluto b* pele',
    'erro_abs_L_pelo': 'Erro absoluto L* pelo',
    'erro_abs_a_pelo': 'Erro absoluto a* pelo',
    'erro_abs_b_pelo': 'Erro absoluto b* pelo',
    'DeltaE_pele': 'ΔE pele',
    'DeltaE_pelo': 'ΔE pelo',
}

for var, label in response_vars.items():
    print(f"\n  ────────────────────────────────────────────")
    print(f"  Variável resposta: {label} ({var})")
    print(f"  ────────────────────────────────────────────")

    # Modelo básico: efeito fixo de período + aleatório de animal
    df_model = df_lmm[['Animal', 'período', var]].dropna()

    if df_model.empty or df_model['Animal'].nunique() < 3:
        print(f"     Dados insuficientes para {var}. Pulando...")
        continue

    fixed_effects_all_local = []

    def _extract(mdf, nome_modelo, n_grupos):
        """Extrai efeitos fixos (estimativa, EP, z, p, IC95%) e componentes de variância."""
        ci = mdf.conf_int()
        k_fe = len(mdf.fe_params)
        var_animal = float(mdf.cov_re.iloc[0, 0])
        var_res = float(mdf.scale)
        icc = var_animal / (var_animal + var_res) if (var_animal + var_res) > 0 else np.nan
        for eff in mdf.fe_params.index:
            fixed_effects_all.append({
                'Variável': label, 'Modelo': nome_modelo, 'Efeito': eff,
                'Estimativa': mdf.fe_params[eff], 'Erro_Padrão': mdf.bse_fe[eff],
                'z': mdf.tvalues[eff], 'p_valor': mdf.pvalues[eff],
                'IC95_inf': ci.loc[eff, 0], 'IC95_sup': ci.loc[eff, 1],
                'N_obs': int(mdf.nobs), 'N_grupos': n_grupos,
                'Var_Animal': var_animal, 'Var_Resíduo': var_res, 'ICC': icc,
            })
        lmm_results_summary.append({
            'Variável': label, 'Modelo': nome_modelo,
            'N_obs': int(mdf.nobs), 'N_grupos': n_grupos,
            'Log-Lik (REML)': mdf.llf, 'Var_Animal (σ²)': var_animal,
            'Var_Resíduo (σ²)': var_res, 'ICC': icc,
            'Convergiu': bool(getattr(mdf, 'converged', True)),
        })
        # Resíduos para diagnóstico (Shapiro-Wilk)
        try:
            sw_w, sw_p = stats.shapiro(mdf.resid)
        except Exception:
            sw_w, sw_p = np.nan, np.nan
        lmm_diag.append({'Variável': label, 'Modelo': nome_modelo,
                         'Shapiro_W': sw_w, 'Shapiro_p': sw_p,
                         'Assimetria_resíduos': stats.skew(mdf.resid),
                         'Curtose_resíduos': stats.kurtosis(mdf.resid)})

    try:
        formula_basic = f"{var} ~ C(período)"
        md_basic = smf.mixedlm(formula_basic, df_model,
                                groups=df_model['Animal'],
                                re_formula="1")
        mdf_basic = md_basic.fit(reml=True)
        print(f"\n  ── Modelo Básico: {var} ~ C(período) + (1|Animal) ──")
        print(mdf_basic.summary())
        _extract(mdf_basic, 'Básico (período)', df_model['Animal'].nunique())
    except Exception as e:
        print(f"     Erro no modelo básico para {var}: {e}")

    # Modelo com robustez: período + variáveis ambientais + (1|Animal)
    env_cols_available = []
    for env_label_key, env_col in ENV_VARS.items():
        if env_col in df_lmm.columns and df_lmm[env_col].notna().sum() > 20:
            safe_name = env_label_key
            df_lmm[safe_name] = df_lmm[env_col]
            env_cols_available.append(safe_name)

    if env_cols_available:
        df_model_env = df_lmm[['Animal', 'período', var] + env_cols_available].dropna()

        if len(df_model_env) >= 20 and df_model_env['Animal'].nunique() >= 3:
            try:
                # Covariáveis ambientais padronizadas (z-score) para comparabilidade
                # dos coeficientes e para reduzir colinearidade numérica.
                for c in env_cols_available:
                    df_model_env[c] = (df_model_env[c] - df_model_env[c].mean()) / df_model_env[c].std(ddof=1)
                env_formula = " + ".join(env_cols_available)
                formula_env = f"{var} ~ C(período) + {env_formula}"
                md_env = smf.mixedlm(formula_env, df_model_env,
                                      groups=df_model_env['Animal'],
                                      re_formula="1")
                mdf_env = md_env.fit(reml=True)
                print(f"\n  ── Modelo Robustez: {var} ~ C(período) + TMR + CTR + Temp + RH + ITGU + (1|Animal) ──")
                print(mdf_env.summary())
                _extract(mdf_env, 'Robustez (período + ambiente)', df_model_env['Animal'].nunique())
            except Exception as e:
                print(f"     Erro no modelo de robustez para {var}: {e}")

df_lmm_results = pd.DataFrame(lmm_results_summary)
df_lmm_results.to_csv(os.path.join(OUTPUT_DIR, 'modelo_linear_misto.csv'), index=False)
print(f"\n  → Salvo em {os.path.join(OUTPUT_DIR, 'modelo_linear_misto.csv')}")

# Efeitos fixos detalhados + correção para múltiplos testes (Holm e BH-FDR)
from statsmodels.stats.multitest import multipletests
df_fixed = pd.DataFrame(fixed_effects_all)
df_fixed['p_Holm'] = np.nan
df_fixed['p_FDR_BH'] = np.nan
for modelo, idx in df_fixed[df_fixed['Efeito'] != 'Intercept'].groupby('Modelo').groups.items():
    pv = df_fixed.loc[idx, 'p_valor'].values
    df_fixed.loc[idx, 'p_Holm'] = multipletests(pv, method='holm')[1]
    df_fixed.loc[idx, 'p_FDR_BH'] = multipletests(pv, method='fdr_bh')[1]
df_fixed.to_csv(os.path.join(OUTPUT_DIR, 'modelo_linear_misto_efeitos_fixos.csv'), index=False)
pd.DataFrame(lmm_diag).to_csv(os.path.join(OUTPUT_DIR, 'modelo_linear_misto_diagnostico.csv'), index=False)
print(f"  → Salvo em modelo_linear_misto_efeitos_fixos.csv e modelo_linear_misto_diagnostico.csv")

# ============================================================================
# 7. TABELA RESUMO GERAL
# ============================================================================
print("\n" + "=" * 70)
print("TABELA RESUMO GERAL")
print("=" * 70)

# Merge de todas as métricas básicas
summary = df_results.merge(
    df_reg[['Variável', 'Intercepto (α)', 'Inclinação (β)', 'p_α≠0', 'p_β≠1']],
    on='Variável'
).merge(
    df_ba[['Variável', 'LoA_inferior', 'LoA_superior', 'p_viés≠0', 'r_proporcionalidade', 'p_proporcionalidade']],
    on='Variável'
)

# DeltaE
for tecido in ['pele', 'pelo']:
    de_col = f'DeltaE_{tecido}'
    mask = df[de_col].notna()
    de_vals = df.loc[mask, de_col].values
    print(f"\n  ΔE {tecido}:")
    print(f"     Média ± DP = {np.mean(de_vals):.3f} ± {np.std(de_vals, ddof=1):.3f}")
    print(f"     Mediana    = {np.median(de_vals):.3f}")
    print(f"     Min – Max  = {np.min(de_vals):.3f} – {np.max(de_vals):.3f}")
    print(f"     % ΔE < 3.0 = {100 * np.mean(de_vals < 3.0):.1f}%")
    print(f"     % ΔE < 5.0 = {100 * np.mean(de_vals < 5.0):.1f}%")

summary.to_csv(os.path.join(OUTPUT_DIR, 'resumo_geral.csv'), index=False)
print(f"\n  → Salvo em {os.path.join(OUTPUT_DIR, 'resumo_geral.csv')}")

# Imprimir tabela formatada
print("\n" + summary.to_string(index=False))

# ============================================================================
# 8. GRÁFICOS COMPLEMENTARES
# ============================================================================

# ─── 8a. Boxplot do erro por período ─────────────────────────────────────────
fig_box, axes_box = plt.subplots(2, 4, figsize=(20, 10))

error_cols = [f'erro_{name}' for name in PAIRS.keys()] + ['DeltaE_pele', 'DeltaE_pelo']
error_labels = list(PAIRS.keys()) + ['ΔE pele', 'ΔE pelo']

for i, (ecol, elabel) in enumerate(zip(error_cols, error_labels)):
    ax = axes_box.ravel()[i]
    data_to_plot = []
    labels_to_plot = []
    for per in df['período'].unique():
        vals = df.loc[df['período'] == per, ecol].dropna().values
        if len(vals) > 0:
            data_to_plot.append(vals)
            labels_to_plot.append(per)

    bp = ax.boxplot(data_to_plot, labels=labels_to_plot, patch_artist=True)
    colors = ['#4C72B0', '#DD8452', '#55A868']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax.set_title(elabel)
    ax.set_ylabel('Erro')
    if ecol.startswith('erro_') and not ecol.startswith('erro_abs'):
        ax.axhline(0, color='red', linestyle='--', linewidth=0.8)

fig_box.suptitle('Distribuição do Erro por Período', fontsize=15, fontweight='bold')
fig_box.tight_layout()
fig_box.savefig(os.path.join(OUTPUT_DIR, 'boxplot_erro_periodo.png'), bbox_inches='tight')
plt.close(fig_box)

# ─── 8b. Gráficos de correlação App vs. Ref com identidade ──────────────────
fig_corr, axes_corr = plt.subplots(2, 3, figsize=(18, 12))
axes_corr = axes_corr.ravel()

for i, (name, (ref_col, app_col)) in enumerate(PAIRS.items()):
    ax = axes_corr[i]
    mask = df[ref_col].notna() & df[app_col].notna()

    # Colorir por período
    periodo_colors = {'Dezembro': '#4C72B0', 'Fevereiro': '#DD8452', 'Julho': '#55A868'}

    for per, color in periodo_colors.items():
        per_mask = mask & (df['período'] == per)
        if per_mask.sum() > 0:
            ax.scatter(df.loc[per_mask, ref_col], df.loc[per_mask, app_col],
                      alpha=0.5, s=25, color=color, label=per, edgecolors='none')

    # Linha de identidade
    lims = [min(ax.get_xlim()[0], ax.get_ylim()[0]),
            max(ax.get_xlim()[1], ax.get_ylim()[1])]
    ax.plot(lims, lims, 'k--', linewidth=1, alpha=0.7, label='y = x')
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_xlabel(f'{ref_col} (Referência)', fontsize=10)
    ax.set_ylabel(f'{app_col} (App)', fontsize=10)

    r_val = df_results.loc[df_results['Variável'] == name, 'Pearson_r'].values[0]
    ax.set_title(f'{name}  (r = {r_val:.3f})', fontsize=12, fontweight='bold')
    ax.legend(fontsize=8)

fig_corr.suptitle('Concordância: Colorímetro (Referência) vs. App',
                  fontsize=15, fontweight='bold', y=1.02)
fig_corr.tight_layout()
fig_corr.savefig(os.path.join(OUTPUT_DIR, 'concordancia_scatter.png'), bbox_inches='tight')
plt.close(fig_corr)

# ============================================================================
# FINALIZAÇÃO
# ============================================================================
print("\n" + "=" * 70)
print("ANÁLISE CONCLUÍDA COM SUCESSO!")
print("=" * 70)
print(f"\nTodos os resultados foram salvos em: {OUTPUT_DIR}")
print("\nArquivos gerados:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    fpath = os.path.join(OUTPUT_DIR, f)
    size = os.path.getsize(fpath)
    print(f"  📄 {f} ({size/1024:.1f} KB)")
