#!/usr/bin/env python3
"""
Exporta as 3 planilhas do arquivo 'Dados colorímetro aparelho 2026.xlsx'
para 3 arquivos CSV individuais no mesmo diretório.

Saída:
  - colorimetro_dezembro_2025.csv
  - colorimetro_fevereiro_2026.csv
  - colorimetro_julho_2026.csv

Colunas: animal_id, pelo_L, pelo_a, pelo_b, pele_L, pele_a, pele_b
"""

import os
import csv
import openpyxl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(BASE_DIR, 'Dados colorímetro aparelho 2026.xlsx')

# Mapeamento: nome da sheet → nome do CSV de saída
SHEET_MAP = {
    'Colorímetro dezembro':  'colorimetro_dezembro_2025.csv',
    'Colorímetro fevereiro': 'colorimetro_fevereiro_2026.csv',
    'colorímetro julho':     'colorimetro_julho_2026.csv',
}

COLUNAS = ['ANIMAL', 'pelo_L', 'pelo_a', 'pelo_b', 'pele_L', 'pele_a', 'pele_b']
# Estrutura da planilha:
# Col A = Nº Animal | B,C,D = Pelo L,a,b | E,F,G = Pele L,a,b
# Dados começam na linha 6 (linhas 1-5 são cabeçalho/títulos)
DATA_START_ROW = 6
COL_INDICES    = [0, 1, 2, 3, 4, 5, 6]  # A..G (0-indexed)


def exportar_sheet_para_csv(ws, csv_path: str) -> int:
    """Lê os dados da sheet e salva em CSV. Retorna o número de linhas gravadas."""
    rows_written = 0
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(COLUNAS)
        for row in ws.iter_rows(min_row=DATA_START_ROW, values_only=True):
            animal_id = row[0]
            if animal_id is None:
                continue  # pula linhas vazias/rodapé
            valores = [row[i] for i in COL_INDICES]
            writer.writerow(valores)
            rows_written += 1
    return rows_written


def main():
    if not os.path.exists(XLSX_PATH):
        print(f'[ERRO] Arquivo não encontrado: {XLSX_PATH}')
        return

    wb = openpyxl.load_workbook(XLSX_PATH)

    print(f'Exportando: {os.path.basename(XLSX_PATH)}')
    print('-' * 60)

    for sheet_name, csv_name in SHEET_MAP.items():
        if sheet_name not in wb.sheetnames:
            print(f'[AVISO] Sheet não encontrada: {sheet_name!r}')
            continue

        ws = wb[sheet_name]
        csv_path = os.path.join(BASE_DIR, csv_name)
        n = exportar_sheet_para_csv(ws, csv_path)
        print(f'  ✓  {sheet_name!r:30s} → {csv_name}  ({n} animais)')

    wb.close()
    print('-' * 60)
    print('Exportação concluída.')


if __name__ == '__main__':
    main()
