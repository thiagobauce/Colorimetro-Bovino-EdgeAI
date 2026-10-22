#!/bin/bash
#set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DEBUG_ARG=""
[[ "${1:-}" == "--debug" ]] && DEBUG_ARG="--out_debug \"$BASE_DIR/debug_pipeline\""

echo "=== Exportando planilhas Excel para CSV ==="
python "$BASE_DIR/exportar_csv.py"

echo ""
echo "=== Iniciando Processamento de Imagens (Isolamento PVC e Detecção de Mancha) ==="
# Executa o pré-processamento nas três pastas principais do colorímetro
python "$BASE_DIR/pvc_preprocessor.py" \
    --pastas "Fotos colorímetro- fevereiro-2026" "fotos colorímetro-dezembro-2025" "Foto colorimetro-Julho2026" \
    $DEBUG_ARG

echo ""
echo "=== Pipeline concluído! ==="
