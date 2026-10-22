#!/usr/bin/env python3
"""
Análise estatística complementar (corrige limitações da análise original):

 1. Medidas repetidas: cada animal contribui com até 3 observações (Dez/Fev/Jul),
    portanto Pearson/MAE/RMSE/Bland-Altman "ingênuos" assumem independência
    que não existe. Aqui os ICs 95% são obtidos por BOOTSTRAP POR CLUSTER (animal).
 2. Concordância: CCC de Lin (precisão x acurácia) + LoA de Bland-Altman para
    medidas repetidas (variância total = entre-animais + intra-animal, via LMM).
 3. LMM com resposta adequada:
      (a) erro com sinal (viés) ~ período + (1|animal)  -> distribuição ~simétrica
      (b) log(ΔE)  ~ período + (1|animal)               -> reduz assimetria
    (o LMM sobre |erro| viola normalidade dos resíduos, ver diagnóstico).
 4. Testes omnibus do efeito de período (razão de verossimilhança, ML) + Holm.
 5. ΔE: média, mediana, IQR, P95 e % abaixo de 1, 3 e 5.
Saídas em resultados_estatisticos/.
"""
import os, warnings
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings('ignore')
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'resultados_estatisticos')
os.makedirs(OUT, exist_ok=True)
RNG = np.random.default_rng(42)
B = 5000

df = pd.read_excel(os.path.join(BASE, 'dados artigo colorimetro 2025 - 2026 (1).xlsx'), sheet_name='2025 a 2026')
df = df[[c for c in df.columns if not str(c).startswith('Unnamed')]].dropna(subset=['Animal']).reset_index(drop=True)
df['Animal'] = df['Animal'].astype(int).astype(str)
for c in ['L_pelo_app', 'a_pelo_app', 'b_pelo_app']:
    df[c] = pd.to_numeric(df[c], errors='coerce')
df['período'] = df['período'].str.strip().str.capitalize()

PAIRS = {
    'L_pele': ('L_pele_colo', 'L_pele_app'), 'a_pele': ('a_pele_colo', 'a_pele_app'),
    'b_pele': ('b_pele_colo', 'b_pele_app'), 'L_pelo': ('L_pelo_colo', 'L_pelo_app'),
    'a_pelo': ('a_pelo_colo', 'a_pelo_app'), 'b_pelo': ('b_pelo_colo', 'b_pelo_app'),
}
for t in ['pele', 'pelo']:
    df[f'DeltaE_{t}'] = np.sqrt(sum((df[f'{k}_{t}_app'] - df[f'{k}_{t}_colo']) ** 2 for k in 'Lab'))
    df[f'logDeltaE_{t}'] = np.log(df[f'DeltaE_{t}'])
for n, (r, a) in PAIRS.items():
    df[f'erro_{n}'] = df[a] - df[r]


def ccc(x, y):
    sxy = np.cov(x, y, ddof=0)[0, 1]
    return 2 * sxy / (x.var() + y.var() + (x.mean() - y.mean()) ** 2)


def ba_repeated_loa(sub, ycol):
    """LoA para medidas repetidas: viés ± 1,96·sqrt(σ²_animal + σ²_resíduo) (LMM nulo)."""
    m = smf.mixedlm(f'{ycol} ~ 1', sub, groups=sub['Animal']).fit(reml=True)
    s = np.sqrt(float(m.cov_re.iloc[0, 0]) + m.scale)
    b = float(m.fe_params['Intercept'])
    return b, s, b - 1.96 * s, b + 1.96 * s, float(m.cov_re.iloc[0, 0]), float(m.scale)


# ---------------------------------------------------------------- 1/2. Bootstrap por animal
rows = []
for n, (rc, ac) in PAIRS.items():
    sub = df[['Animal', rc, ac]].dropna().rename(columns={rc: 'ref', ac: 'app'})
    animals = sub['Animal'].unique()
    groups = {a: sub.loc[sub.Animal == a, ['ref', 'app']].values for a in animals}

    def stat(arr):
        x, y = arr[:, 0], arr[:, 1]
        d = y - x
        return (np.corrcoef(x, y)[0, 1], ccc(x, y), np.abs(d).mean(),
                np.sqrt((d ** 2).mean()), d.mean(), d.mean() - 1.96 * d.std(ddof=1),
                d.mean() + 1.96 * d.std(ddof=1), np.polyfit(x, y, 1)[0])

    obs = stat(sub[['ref', 'app']].values)
    boots = []
    for _ in range(B):
        samp = RNG.choice(animals, size=len(animals), replace=True)
        boots.append(stat(np.vstack([groups[a] for a in samp])))
    boots = np.array(boots)
    lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)
    b, s, lo_loa, hi_loa, v_a, v_r = ba_repeated_loa(sub.assign(d=sub.app - sub.ref), 'd')
    row = {'Variável': n, 'N_obs': len(sub), 'N_animais': len(animals)}
    for i, k in enumerate(['Pearson_r', 'CCC_Lin', 'MAE', 'RMSE', 'Viés', 'LoA_inf_ingênuo', 'LoA_sup_ingênuo', 'Inclinação_β']):
        row[k] = obs[i]; row[k + '_IC95_inf'] = lo[i]; row[k + '_IC95_sup'] = hi[i]
    row.update({'LoA_inf_medidas_repetidas': lo_loa, 'LoA_sup_medidas_repetidas': hi_loa,
                'Var_entre_animais_diff': v_a, 'Var_intra_animal_diff': v_r})
    rows.append(row)
    print(f'{n}: r={obs[0]:.3f} [{lo[0]:.3f},{hi[0]:.3f}] CCC={obs[1]:.3f} MAE={obs[2]:.3f} [{lo[2]:.3f},{hi[2]:.3f}]')
pd.DataFrame(rows).to_csv(os.path.join(OUT, 'concordancia_bootstrap_cluster.csv'), index=False)

# ---------------------------------------------------------------- 5. ΔE descritivo
rows = []
for t in ['pele', 'pelo']:
    for per in ['Todos', 'Dezembro', 'Fevereiro', 'Julho']:
        v = df[f'DeltaE_{t}'] if per == 'Todos' else df.loc[df['período'] == per, f'DeltaE_{t}']
        v = v.dropna().values
        rows.append({'Tecido': t, 'Período': per, 'N': len(v), 'Média': v.mean(), 'DP': v.std(ddof=1),
                     'Mediana': np.median(v), 'Q1': np.percentile(v, 25), 'Q3': np.percentile(v, 75),
                     'P95': np.percentile(v, 95), 'Máx': v.max(),
                     '%<1': 100 * (v < 1).mean(), '%<3': 100 * (v < 3).mean(), '%<5': 100 * (v < 5).mean()})
pd.DataFrame(rows).to_csv(os.path.join(OUT, 'deltaE_descritivo.csv'), index=False)

# ---------------------------------------------------------------- 3/4. LMM adequados
ENV = {'TMR': 'TMR', 'CTR': 'CTR (W/m²)', 'Temp': 'Temp °C Média', 'RH': '%RH', 'ITGU': 'MÉDIA ITGU'}
resp = {**{f'erro_{k}': f'Viés (erro com sinal) {k}' for k in PAIRS},
        'logDeltaE_pele': 'log ΔE pele', 'logDeltaE_pelo': 'log ΔE pelo'}
fx_rows, om_rows, dg_rows = [], [], []
for var, label in resp.items():
    d = df[['Animal', 'período', var]].dropna()
    m_full = smf.mixedlm(f'{var} ~ C(período, Treatment("Dezembro"))', d, groups=d['Animal']).fit(reml=False)
    m_null = smf.mixedlm(f'{var} ~ 1', d, groups=d['Animal']).fit(reml=False)
    lr = 2 * (m_full.llf - m_null.llf)
    om_rows.append({'Resposta': label, 'N_obs': len(d), 'N_animais': d.Animal.nunique(),
                    'LRT_qui2': lr, 'gl': 2, 'p_LRT': stats.chi2.sf(lr, 2)})
    m = smf.mixedlm(f'{var} ~ C(período, Treatment("Dezembro"))', d, groups=d['Animal']).fit(reml=True)
    ci = m.conf_int()
    va, vr = float(m.cov_re.iloc[0, 0]), float(m.scale)
    for e in m.fe_params.index:
        fx_rows.append({'Resposta': label, 'Efeito': e.replace('C(período, Treatment("Dezembro"))', 'Período'),
                        'Estimativa': m.fe_params[e], 'EP': m.bse_fe[e], 'z': m.tvalues[e], 'p': m.pvalues[e],
                        'IC95_inf': ci.loc[e, 0], 'IC95_sup': ci.loc[e, 1], 'N_obs': len(d),
                        'N_animais': d.Animal.nunique(), 'σ²_animal': va, 'σ²_resíduo': vr, 'ICC': va / (va + vr)})
    w, p = stats.shapiro(m.resid)
    dg_rows.append({'Resposta': label, 'Shapiro_W': w, 'Shapiro_p': p, 'Assimetria': stats.skew(m.resid),
                    'Curtose_exc': stats.kurtosis(m.resid)})
om = pd.DataFrame(om_rows)
om['p_Holm'] = multipletests(om['p_LRT'], method='holm')[1]
om.to_csv(os.path.join(OUT, 'lmm_efeito_periodo_LRT.csv'), index=False)
fx = pd.DataFrame(fx_rows)
fx['p_Holm_contrastes'] = np.nan
mask = fx['Efeito'] != 'Intercept'
fx.loc[mask, 'p_Holm_contrastes'] = multipletests(fx.loc[mask, 'p'], method='holm')[1]
fx.to_csv(os.path.join(OUT, 'lmm_viés_logDeltaE_efeitos_fixos.csv'), index=False)
pd.DataFrame(dg_rows).to_csv(os.path.join(OUT, 'lmm_viés_logDeltaE_diagnostico.csv'), index=False)

# ---------------------------------------------------------------- ΔE por período (Dezembro como referência)
print('\nLRT efeito de período:\n', om.round(4).to_string(index=False))
print('\nDiagnóstico:\n', pd.DataFrame(dg_rows).round(3).to_string(index=False))
print('\nOK')
