#!/usr/bin/env python3
"""
Script gerador e validador da Metodologia Científica Completa do Colorímetro
Revista Alvo: Smart Agricultural Technology (Elsevier)
Gera: Metodologia_Colorimetro_Smart_Agricultural_Technology.docx a partir de .md via pandoc
"""

import os
import subprocess
import pandas as pd
import numpy as np

BASE_DIR = "/media/workstation_2x_3080/ext_ssd1/Colorímetro"
MD_PATH = os.path.join(BASE_DIR, "Metodologia_Colorimetro_Smart_Agricultural_Technology.md")
DOCX_PATH = os.path.join(BASE_DIR, "Metodologia_Colorimetro_Smart_Agricultural_Technology.docx")
RD = os.path.join(BASE_DIR, "resultados_estatisticos")

def compile_docx():
    print(f"Compilando DOCX a partir de:\n  {MD_PATH}")
    if not os.path.exists(MD_PATH):
        raise FileNotFoundError(f"Arquivo Markdown não encontrado: {MD_PATH}")
    
    cmd = ["pandoc", MD_PATH, "-o", DOCX_PATH]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Erro na execução do pandoc:\n{res.stderr}")
        raise RuntimeError("Falha ao gerar DOCX")
    
    size_kb = os.path.getsize(DOCX_PATH) / 1024
    print(f"SUCESSO! Documento gerado com sucesso:\n  {DOCX_PATH} ({size_kb:.1f} KB)")

def validate_integrity():
    with open(MD_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    
    words = len(text.split())
    lines = len(text.splitlines())
    print("\n--- Relatório de Integridade da Metodologia ---")
    print(f"Total de Linhas no Markdown: {lines}")
    print(f"Total de Palavras no Markdown: {words:,}")
    
    # Verificar termos técnicos essenciais de software
    terms = [
        "android.hardware.camera2", "CONTROL_AE_MODE_OFF", "CONTROL_AF_MODE_OFF",
        "CONTROL_AWB_MODE_OFF", "SENSOR_EXPOSURE_TIME", "SENSOR_SENSITIVITY",
        "ImageFormat.YUV_420_888", "OpenCV", "ONNX Runtime", "Gray World",
        "Hough", "Otsu", "GroupShuffleSplit", "Random Forest", "skl2onnx",
        "Room", "SQLite", "$3 \\times 3$"
    ]
    print("\nVerificando presença de módulos técnicos de software e visão computacional:")
    for term in terms:
        status = "OK" if term in text else "FALTANDO"
        print(f"  - [{status}] {term}")

if __name__ == "__main__":
    compile_docx()
    validate_integrity()
