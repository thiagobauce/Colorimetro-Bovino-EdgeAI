#!/usr/bin/env python3
"""
Script gerador da Metodologia Científica Completa do Colorímetro
Revista Alvo: Smart Agricultural Technology (Elsevier)
Gera: Metodologia_Colorimetro_Smart_Agricultural_Technology.md e .docx
"""

import os
import subprocess
import pandas as pd
import numpy as np

RD = "/media/workstation_2x_3080/ext_ssd1/Colorímetro/resultados_estatisticos/"
BASE_DIR = "/media/workstation_2x_3080/ext_ssd1/Colorímetro"

def _f(x, d=2):
    return "--" if pd.isna(x) else f"{x:.{d}f}"

def _p(x):
    if pd.isna(x): return "--"
    if x < 0.001: return "< 0.001"
    return f"{x:.3f}"

# Carregar tabelas estatísticas
df_ab = pd.read_csv(os.path.join(BASE_DIR, "tabela_de_ablacao.csv")) if os.path.exists(os.path.join(BASE_DIR, "tabela_de_ablacao.csv")) else None
df_conc = pd.read_csv(os.path.join(RD, "concordancia_bootstrap_cluster.csv"))
df_de = pd.read_csv(os.path.join(RD, "deltaE_descritivo.csv"))
df_anim = pd.read_csv(os.path.join(RD, "estabilidade_fatores_animais.csv"))
df_env = pd.read_csv(os.path.join(RD, "robustez_ambiental.csv"))
df_lrt = pd.read_csv(os.path.join(RD, "lmm_efeito_periodo_LRT.csv"))
df_fx = pd.read_csv(os.path.join(RD, "lmm_viés_logDeltaE_efeitos_fixos.csv"))

print("Todas as tabelas foram carregadas com sucesso!")
