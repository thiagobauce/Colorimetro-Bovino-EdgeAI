# Documentação Metodológica do Notebook Colorimetro_Clean.ipynb

Este documento apresenta o detalhamento técnico e conceitual de cada etapa do arquivo `Colorimetro_Clean.ipynb`. O objetivo é fornecer uma descrição formal, clara e acessível sobre a lógica de processamento de imagens, engenharia de dados e modelagem preditiva utilizada no projeto.

---

## 1. Visão Geral e Objetivo do Projeto

O objetivo central deste pipeline computacional é estimar com precisão laboratorial os valores de cor da pele e do pelo de bovinos a partir de imagens digitais capturadas por smartphones, utilizando como referência física as medições de um colorímetro profissional de bancada.

O fluxo de trabalho aborda quatro etapas principais:
1. **Ingestão e Padronização:** Unificação e limpeza dos dados de medições físicas e correspondência com as imagens coletadas em diferentes períodos experimentais (Dezembro/2025, Fevereiro/2026 e Julho/2026).
2. **Avaliação da Abordagem Clássica (Baseline):** Segmentação da amostra e aplicação de transformações lineares diretas, demonstrando a necessidade de abordagens estatísticas não lineares.
3. **Engenharia de Atributos Espaciais (Grid 3x3):** Subdivisão da área de interesse em grades espaciais para ampliação amostral e captura de variações texturais e de iluminação.
4. **Modelagem Preditiva com Aprendizado de Máquina:** Treinamento, validação rigorosa com isolamento por animal e comparação de algoritmos supervisionados (*Random Forest*, *Extra Trees* e *XGBoost*).

---

## 2. Fundamentos da Colorimetria (Espaço CIELAB e Métrica Delta E)

As medições do equipamento físico e os alvos preditivos do sistema são definidos no espaço de cor tridimensional **CIELAB** (definido pela Comissão Internacional de Iluminação - CIE):

```
       +L* (Luminosidade máxima: Branco = 100)
         |
         |     +b* (Amarelo)
         |    /
 -a* ----+----+---- +a* (Vermelho)
(Verde) /|
       / |
  (Azul) |
   -b*   |
       -L* (Luminosidade mínima: Preto = 0)
```

* **L\* (Luminosidade):** Escala unidimensional que varia de 0 (preto absoluto) a 100 (branco difuso perfeito).
* **a\* (Eixo Verde-Vermelho):** Coordenada cromática onde valores negativos representam tons verdes e valores positivos representam tons vermelhos.
* **b\* (Eixo Azul-Amarelo):** Coordenada cromática onde valores negativos representam tons azuis e valores positivos representam tons amarelos.
* **Delta E ($\Delta E$ - Distância Euclidiana de Cor):** Métrica padrão que quantifica a diferença perceptível total entre duas cores tridimensionais:

$$\Delta E = \sqrt{(L^*_{\text{previsto}} - L^*_{\text{real}})^2 + (a^*_{\text{previsto}} - a^*_{\text{real}})^2 + (b^*_{\text{previsto}} - b^*_{\text{real}})^2}$$

Interpretação prática da métrica $\Delta E$:
* $\Delta E < 1.0$: Diferença imperceptível ao olho humano.
* $1.0 \le \Delta E \le 3.0$: Diferença perceptível apenas mediante inspeção atenta por especialista.
* $\Delta E > 5.0$: Diferença evidente e facilmente identificável.

---

## 3. Detalhamento Passo a Passo das Células do Notebook

---

### 3.1. Preparação do Ambiente e Dependências (Células 1 a 3)

Neste bloco inicial, são instaladas e carregadas as bibliotecas fundamentais:
* **OpenCV (`cv2`):** Biblioteca para leitura de imagens, conversões entre espaços de cores (BGR, RGB, HSV, LAB) e operações morfológicas.
* **Pandas:** Estruturação, limpeza, manipulação tabular e fusão dos conjuntos de dados.
* **NumPy:** Vetorização e computação científica de matrizes numéricas.
* **Matplotlib e Seaborn:** Geração de diagnósticos visuais, matrizes de correlação e gráficos de dispersão.
* **Scikit-Learn (`sklearn`):** Algoritmos de divisão de dados agrupados, pré-processamento, escalonamento e modelos de árvores de decisão.
* **XGBoost (`xgboost`):** Implementação de *Gradient Boosting* otimizada para regressão de alta performance.

---

### 3.2. Configuração de Caminhos e Estrutura de Pastas (Célula 4)

Define as variáveis estruturais do projeto:
* `caminhos_planilhas`: Lista com os caminhos absolutos das planilhas CSV correspondentes às três épocas de coleta.
* `caminhos_fotos`: Lista com os diretórios que armazenam as fotografias brutas capturadas no respectivo período.

---

### 3.3. Ingestão, Padronização e Limpeza das Planilhas (Célula 5)
* **Função:** `carregar_planilhas(caminhos)`

Esta função executa a higienização dos registros tabulares:
1. Itera sobre cada arquivo CSV de coleta.
2. Identifica e corrige variações de formatação entre versões de planilhas (por exemplo, cabeçalhos legados com coluna de índice sequencial versus o formato padronizado de 7 colunas).
3. Uniformiza os nomes das colunas: `ANIMAL`, `L_pelo`, `a_pelo`, `b_pelo`, `L_pele`, `a_pele`, `b_pele`.
4. Garante a integridade tipológica: converte o identificador do animal (`ANIMAL`) para representação textual pura e converte as medições cromáticas para tipos numéricos de ponto flutuante, descartando registros com valores nulos.
5. Retorna o DataFrame consolidado `df_final`.

---

### 3.4. Segmentação Clássica por Visão Computacional (Célula 6)
* **Função:** `extrair_cor_pura_multicanal(caminho_img)`

Executa o isolamento geométrico da área de interesse biológico contida no cone de contenção de PVC:
1. **Detecção da Abertura do PVC:** A imagem em tons de cinza recebe um filtro Gaussiano ($61 \times 61$) para eliminação de ruídos de alta frequência. Uma limiarização binária seguida de abertura morfológica ($45 \times 45$) delimita o contorno da abertura circular.
2. **Mascaramento do Fundo:** A região externa ao contorno detectado é preenchida com o valor 255 (fundo branco), eliminando interferências do exterior do cano.
3. **Segmentação da Mancha Biológica:** Aplica-se um segundo filtro Gaussiano ($151 \times 151$) com limiarização dinâmica:
   * Para amostras de **pele**: limiar de intensidade definido em 80 (detecção da região raspada mais escura).
   * Para amostras de **pelo**: limiar definido em 165.
4. **Extração dos Perfis de Cor:**
   * Recorta a caixa delimitadora (*Bounding Box*) da mancha com uma margem de segurança (*padding*) de 5%.
   * Converte a região recortada para os espaços RGB, HSV e Lab do OpenCV.
   * Calcula a **Mediana** e o **Desvio Padrão** de cada canal para mitigar o impacto de artefatos pontuais (poeira ou brilhos especulares).

---

### 3.5. Avaliação da Conversão Direta sem Machine Learning (Célula 7)

Esta etapa estabelece o *baseline* empírico (abordagem ingênua):
1. Faz o pareamento entre o identificador numérico extraído do nome do arquivo da foto e o registro correspondente na planilha.
2. Aplica a função `extrair_cor_pura_multicanal`.
3. Executa a conversão linear direta do espaço Lab do OpenCV (faixa de 0 a 255) para a escala CIELAB padrão:
   * $L_{\text{convertido}} = L_{\text{câmera}} \times \frac{100}{255}$
   * $a_{\text{convertido}} = a_{\text{câmera}} - 128$
   * $b_{\text{convertido}} = b_{\text{câmera}} - 128$
4. Calcula o erro absoluto para cada coordenada e o $\Delta E$ médio, gravando os resultados em `resultados.csv`.

**Conclusão desta etapa:** A resposta espectral dos sensores de câmeras de celular e as variações na iluminação ambiente geram discrepâncias não lineares significativas em relação aos sensores do colorímetro. Isso fundamenta a necessidade de modelagem avançada com Aprendizado de Máquina.

---

### 3.6. Extração Espacial Multicanal em Grade 3x3 (Célula 8)
* **Função:** `extrair_grid_multicanal(caminho_img, num_partes=9)`

Para capturar a variabilidade textural e enriquecer a densidade amostral:
1. Replica a rotina de isolamento do PVC e localização da mancha biológica.
2. Subdivide a imagem recortada em uma matriz geométrica regular de **$3 \times 3$ (9 células independentes)**.
3. Para cada uma das 9 células, calcula a média dos canais:
   * **RGB:** Canais Vermelho ($R$), Verde ($G$) e Azul ($B$).
   * **HSV:** Matiz ($H$), Saturação ($S$) e Valor de Luminância ($V$).
   * **Lab (OpenCV):** $L$, $a$ e $b$ nativos do OpenCV.
4. Gera 9 vetores de características para cada imagem processada.

---

### 3.7. Estruturação da Base de Dados para Aprendizado de Máquina (Célula 9)

Constrói a base de dados tabular `df_ml`:
1. Agrupa os pares de imagens (pele e pelo) de cada animal.
2. Executa a extração em grade para as imagens de **pele**, atribuindo o identificador binário `Tipo_Pele = 1`.
3. Executa a extração em grade para as imagens de **pelo**, atribuindo `Tipo_Pele = 0`.
4. Associa a cada vetor os valores reais $L^*, a^*, b^*$ medidos pelo colorímetro.
5. Estrutura o DataFrame `df_ml`, contendo centenas de registros representativos para o treinamento.

---

### 3.8. Análise Estatística de Correlação e Dispersão (Células 10 e 11)

Nestas células são produzidos diagnósticos exploratórios:
* **Matriz de Correlação de Pearson (Heatmap):** Avalia a força e o sentido das correlações lineares entre os canais da câmera e as leituras de referência do aparelho.
* **Gráficos de Dispersão com Regressão Linear (`pairplot` e `regplot`):** Permitem verificar visualmente a dispersão dos pontos cromáticos e o comportamento de monotonicidade entre as variáveis.

---

### 3.9. Treinamento e Comparação de Modelos Preditivos (Células 12 a 15)

---

#### Protocolo de Validação: Separação por Grupos (`GroupShuffleSplit`)
Para garantir validade metodológica e prevenir o vazamento de dados (*data leakage*):
* A divisão entre conjunto de treinamento (80%) e teste (20%) é parametrizada com base no identificador único do animal (`groups=df_ml['Animal']`).
* Nenhuma célula da grade de um mesmo animal participa simultaneamente de treino e teste. O modelo é avaliado exclusivamente sobre indivíduos inéditos.

---

#### Modelo 1: Clusterização K-Means associada a Extra Trees (Célula 12)
* **Arquitetura:** Aplica o algoritmo não supervisionado `KMeans(n_clusters=9)` sobre o espaço de cores para segmentar as amostras em 9 perfis fotométricos ("famílias" de iluminação).
* Em seguida, treina um `ExtraTreesRegressor(n_estimators=300, max_depth=20)` utilizando as variáveis cromáticas e a classe do cluster para prever simultaneamente $L^*, a^*, b^*$.

---

#### Modelo 2: Random Forest com Engenharia de Features e Modelagem Especializada (Célula 13)
* **Engenharia de Atributos:** Cria variáveis matemáticas baseadas em relações de reflectância:
  * Razões cromáticas: $\text{Razao\_RG} = \frac{R}{G}$, $\text{Razao\_RB} = \frac{R}{B}$, $\text{Razao\_GB} = \frac{G}{B}$.
  * Energia total: $\text{Soma\_RGB} = R + G + B$.
  * Diferencial de luminância: $\text{Dif\_L\_V} = L_{\text{cv2}} - V$.
* **Abordagem Especialista:** Treina dois regressores independentes (`rf_pele` e `rf_pelo`), permitindo que as superfícies de decisão se ajustem separadamente à opacidade da pele e à dispersão de luz no pelame.

---

#### Modelo 3: Extra Trees Unificado (Célula 14)
* **Arquitetura:** Treina um regressor `ExtraTreesRegressor` com 300 estimadores utilizando a matriz de atributos padrão acompanhada da variável indicadora `Tipo_Pele`.

---

#### Modelo 4: XGBoost Especialista por Canal de Cor (Célula 15) — Modelo de Maior Desempenho
* **Arquitetura:** Utiliza *Extreme Gradient Boosting* (`XGBRegressor`) com normalização prévia por `StandardScaler` em um pipeline estruturado.
* **Modelagem Unidimensional Especializada:** São instanciados e calibrados 3 modelos separados:
  1. `modelo_L`: Especialista exclusivo na previsão de Luminosidade ($L^*$).
  2. `modelo_a`: Especialista exclusivo na coordenada Verde-Vermelho ($a^*$).
  3. `modelo_b`: Especialista exclusivo na coordenada Azul-Amarelo ($b^*$).
* **Hiperparâmetros configurados:** `n_estimators=600`, `learning_rate=0.05`, `max_depth=20`, `tree_method='hist'`.
* **Resultado:** Esta configuração obtém a maior taxa de concordância estatística e a menor dispersão de erro global no conjunto de teste.

---

## 4. Interpretação das Métricas de Validação Estatística

Para cada experimento, o notebook gera um relatório quantitativo no conjunto de teste independente:

| Métrica | Definição Matemática | Interpretação Científica |
| :--- | :--- | :--- |
| **MAE (Erro Médio Absoluto)** | $\frac{1}{n} \sum \|y_i - \hat{y}_i\|$ | Distância linear média entre o valor predito e o real. Quanto menor, melhor. |
| **$R^2$ (Coeficiente de Determinação)** | $1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$ | Proporção da variância dos dados reais explicada pelo modelo. Valores próximos a 1.0 indicam alta precisão explicativa. |
| **RMSE (Raiz do Erro Quadrático Médio)** | $\sqrt{\frac{1}{n} \sum (y_i - \hat{y}_i)^2}$ | Penaliza desvios de grande magnitude. Valores próximos ao MAE confirmam consistência e ausência de *outliers* preditivos. |
| **$r$ de Pearson** | Coeficiente de correlação bivariada | Avalia o alinhamento da direção linear. Deve se aproximar de +1.0. |
| **Delta E Médio ($\Delta E$)** | Média das distâncias euclidianas CIELAB | Métrica sintética global de cor. Valores inferiores a 2.0 a 3.0 atestam equivalência prática ao equipamento. |
| **Análise de Bland-Altman** | Viés médio e Limites de Concordância de 95% ($\text{Viés} \pm 1.96 \cdot \text{DP}$) | Metodologia padrão da literatura biomédica para avaliar a substituibilidade de instrumentos. Viés próximo de zero e limites estreitos comprovam concordância entre métodos. |

---

## 5. Dicionário de Variáveis e Estruturas de Dados

Para facilitar o acompanhamento e modificações no código:

* `df_colorimetro`: Tabela com as leituras oficiais consolidadas do colorímetro físico.
* `df_comparacao`: Tabela contendo a validação preliminar direta (foto bruta convertida linearmente versus aparelho).
* `df_ml`: Base tabular consolidada para Aprendizado de Máquina, contendo as características do Grid 3x3, a marcação de pele/pelo e os valores reais.
* `X_train` / `y_train`: Conjunto de atributos e alvos dos animais selecionados para a fase de ajuste dos modelos.
* `X_test` / `y_test`: Conjunto de validação composto exclusivamente por animais não observados no treinamento.
* `modelo_L`, `modelo_a`, `modelo_b`: Instâncias dos pipelines de regressão do XGBoost ajustadas individualmente para cada canal de cor.

---

## 6. Síntese Metodológica

O notebook `Colorimetro_Clean.ipynb` constitui a estrutura analítica principal do projeto: ele realiza a ingestão estruturada das imagens e planilhas, executa a extração em grade para aumento da resolução espacial de cor, assegura a integridade experimental por meio de validação agrupada por animal e calibra modelos baseados em gradiente (*XGBoost*) capazes de reproduzir com rigor científico as leituras de um colorímetro laboratorial.
