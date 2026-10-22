# Bovine Colorimetry Edge-AI: In-Field Skin and Hair Coat Color Estimation via Computer Vision and Machine Learning

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.7%2B-green.svg)](https://opencv.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-1.16%2B-blueviolet.svg)](https://onnxruntime.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Target Journal](https://img.shields.io/badge/Target_Journal-Smart_Agricultural_Technology-red.svg)](https://www.sciencedirect.com/journal/smart-agricultural-technology)

> **Official Repository for the Manuscript:**  
> *"Development and Validation of a Smartphone-Based Computer Vision and Machine Learning System for In-Field Bovine Skin and Hair Coat Colorimetry"*  
> **Affiliations:** Faculty of Veterinary Medicine and Animal Science, Federal University of Mato Grosso do Sul (UFMS) & Embrapa Beef Cattle (*Embrapa Gado de Corte*), Campo Grande, MS, Brazil.  
> **Animal Ethics Approval:** CEUA Embrapa Gado de Corte (Certificate Protocol No. 002/2022 / CONCEA).

---

## 📌 Table of Contents
- [1. Overview & Research Scope](#1-overview--research-scope)
- [2. Research Objectives](#2-research-objectives)
- [3. System Architecture & Methodology](#3-system-architecture--methodology)
  - [3.1. Optical Isolation Chamber Hardware](#31-optical-isolation-chamber-hardware)
  - [3.2. Computer Vision Pipeline (Gray World & 3x3 Grid)](#32-computer-vision-pipeline-gray-world--3x3-grid)
  - [3.3. Multichannel Feature Engineering (14 Descriptors)](#33-multichannel-feature-engineering-14-descriptors)
  - [3.4. Dual-Specialist Machine Learning (Skin vs. Coat)](#34-dual-specialist-machine-learning-skin-vs-coat)
  - [3.5. Standalone Android Edge-AI Application](#35-standalone-android-edge-ai-application)
- [4. Experimental Cohort & Validation Design](#4-experimental-cohort--validation-design)
- [5. Metrological Results & Statistical Benchmarking](#5-metrological-results--statistical-benchmarking)
  - [5.1. Architectural Ablation Study](#51-architectural-ablation-study)
  - [5.2. Agreement with Cluster Bootstrap 95% CIs](#52-agreement-with-cluster-bootstrap-95-cis)
  - [5.3. Global Color Difference ($\Delta E^*_{ab}$) by Season](#53-global-color-difference-delta-e_ab-by-season)
  - [5.4. Stability Across Animal Biometrics and Weather Conditions](#54-stability-across-animal-biometrics-and-weather-conditions)
  - [5.5. Longitudinal Linear Mixed-Effects Models (LMM)](#55-longitudinal-linear-mixed-effects-models-lmm)
- [6. Repository File Structure](#6-repository-file-structure)
- [7. Quickstart & Reproducibility Guide](#7-quickstart--reproducibility-guide)
- [8. Citation & Acknowledgments](#8-citation--acknowledgments)

---

## 1. Overview & Research Scope
Accurate measurement of skin and hair coat color in cattle is crucial for precision livestock farming, thermoregulation assessment, tropical adaptation phenotyping, and genetic selection. Standard commercial benchtop tristimulus colorimeters (e.g., Konica Minolta CR-400) cost thousands of dollars, require delicate laboratory handling, and are cumbersome in field handling chutes (*troncos de contenção*).

This project delivers a **cost-effective, edge-computing smartphone system** that replaces physical benchtop colorimeters with metrological equivalence:
- **Zero Cloud Dependency:** Runs 100% offline directly on smartphone hardware (< 140 ms inference time);
- **Physical Glare Shielding:** Custom 3D/PVC optical chamber eliminating ambient sun flare;
- **Dual Bio-Optical Specialists:** Independent Random Forest ensembles accounting for dermal volume scattering vs. keratin fiber reflection;
- **Strict Subject Isolation:** Validated with group-level holdout (`GroupShuffleSplit`) to prevent animal identity memorization (*data leakage*).

---

## 2. Research Objectives

### 🎯 General Objective
To develop and validate an artificial intelligence-driven computational methodology to accurately estimate the skin and hair coat color of Nellore cattle (*Bos indicus*) under operational tropical field conditions.

### 🎯 Specific Objectives
1. **Instrumental Benchmarking:** Compare computational smartphone computer vision estimates directly against ground-truth instrumental tristimulus colorimetry (CIE $L^*, a^*, b^*$);
2. **Longitudinal Stability:** Evaluate the temporal stability and metrological agreement between methods across distinct seasonal campaigns in relation to dynamic environmental microclimate conditions (TMR, CTR, Temp, RH, ITGU/BGHI) and biological animal growth factors (chronological age, body weight, and average daily gain);
3. **Edge-AI Commercial Deployment:** Develop, optimize, and validate a standalone native mobile application (Edge-AI) for in-field commercial utilization, providing instantaneous chute-side colorimetry without compromising metrological precision.

---

## 3. System Architecture & Methodology

```
+---------------------------------------------------------------------------------------------------+
|                                  IN-FIELD DATA ACQUISITION & EDGE-AI PIPELINE                     |
+---------------------------------------------------------------------------------------------------+
|  [ Bovine Flank Patch ]  -->  [ Custom PVC Chamber ]  -->  [ Smartphone Pro Camera + Flash ]      |
|                                (20 cm, Matte Black,         (Fixed ISO 100, 1/125 s, 5500 K)      |
|                                 Neoprene Seal Ring)                                               |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                COMPUTER VISION NORMALIZATION & EXTRACTION                         |
+---------------------------------------------------------------------------------------------------+
|  [ Gray World White Balance ]  -->  [ Morphological ROI ]  -->  [ 3x3 Spatial Grid Discretization ]|
|  (Illuminant color correction)      (Gaussian filter + Otsu)     (9 sub-cells: core vs. periphery)|
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                  14 PHOTOMETRIC DESCRIPTORS PER CELL                              |
+---------------------------------------------------------------------------------------------------+
|  - 9 Direct Channels: R, G, B, H, S, V, L_cv2, a_cv2, b_cv2                                       |
|  - 5 Bio-Optical Ratios: Razao_RG, Razao_RB, Razao_GB, Dif_L_V (anti-glare), Soma_RGB (energy)    |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                             DUAL-SPECIALIST RANDOM FOREST ENSEMBLE                                |
+---------------------------------------------------------------------------------------------------+
|         [ Skin Specialist Regressor ]              [ Hair Coat Specialist Regressor ]             |
|          (Trained on shaved epidermis)               (Trained on intact keratin coat)             |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                    COMMERCIAL DEPLOYMENT (ONNX)                                   |
+---------------------------------------------------------------------------------------------------+
|  Outputs: Calibrated CIE L*, a*, b* Coordinates + Perceptual Delta E + Instantaneous Chute Display |
+---------------------------------------------------------------------------------------------------+
```

### 3.1. Optical Isolation Chamber Hardware
- Rigid PVC cylinder with an axial length of $20\text{ cm}$ and internal diameter of $10\text{ cm}$;
- Interior coated with optical ultra-matte black paint (specular reflectance $< 1.5\%$ across $380--750\text{ nm}$);
- Distal end equipped with a flexible closed-cell neoprene rubber seal that contours to the animal's flank, preventing outdoor sunlight leakage ($> 100,000\text{ lux}$ to $0\text{ lux}$ interior);
- High-precision smartphone adapter keeping the camera lens and flash centered over the longitudinal axis.

### 3.2. Computer Vision Pipeline (Gray World & 3x3 Grid)
1. **Gray World White Balance:** Normalizes cold spectral peaks from the smartphone LED flash by balancing channel gains against scene gray expectation ($\mu_{\text{gray}} / \bar{C}$);
2. **Otsu Circular Segmentation:** Isolates the active circular biological tissue aperture;
3. **$3 \times 3$ Spatial Grid:** Decomposes illumination into 1 central core block (direct incident flash) and 8 peripheral blocks (diffuse volumetric backscattering), preserving spatial gradients.

### 3.3. Multichannel Feature Engineering (14 Descriptors)
1. $R, G, B$: Mean raw intensities in sRGB;
2. $H, S, V$: Cylindrical chromatic coordinates (Hue, Saturation, Value);
3. $L_{\text{cv2}}, a_{\text{cv2}}, b_{\text{cv2}}$: Scaled OpenCV CIELAB coordinates;
4. $\text{Razao}_{\text{RG}} = R / (G + \epsilon)$: Cutaneous erythema and vascularization index;
5. $\text{Razao}_{\text{RB}} = R / (B + \epsilon)$: Melanin pigmentation ratio (eumelanin vs. pheomelanin);
6. $\text{Razao}_{\text{GB}} = G / (B + \epsilon)$: Keratin fiber structural scattering ratio;
7. $\text{Dif}_{LV} = L_{\text{cv2}} - V$: Decoupling metric between perceived lightness and photonic brightness (suppresses specular hotspots);
8. $\text{Soma}_{\text{RGB}} = R + G + B$: Total integrated backscattered photon flux proxy.

### 3.4. Dual-Specialist Machine Learning (Skin vs. Coat)
Because shaved bovine skin (dermal volume scattering) and intact coat (keratin cylindrical fibers with anisotropic reflection) possess distinct BRDFs, unifying them causes conflicting decision boundaries. Two dedicated Random Forest models ($B = 200$ trees, $\text{max\_depth} = 15$) are trained independently: $\mathcal{M}_{\text{skin}}$ and $\mathcal{M}_{\text{coat}}$.

### 3.5. Standalone Android Edge-AI Application
- Built natively with **Kotlin**, **C++ (OpenCV Native SDK)**, and **ONNX Runtime (v1.16)**;
- Quantized ONNX weights ($< 8.5\text{ MB}$ package payload);
- Zero internet or cellular connection required;
- Total camera-to-result latency $< 140\text{ ms}$.

---

## 4. Experimental Cohort & Validation Design
- **Location:** Embrapa Beef Cattle (*Embrapa Gado de Corte*), Campo Grande, MS, Brazil ($20^\circ 26' 41.5''\text{ S}$, $54^\circ 43' 21.3''\text{ W}$);
- **Cohort:** Longitudinal follow-up of $N = 47$ intact young male Nellore cattle (*Bos indicus*) on *Urochloa brizantha* cv. Marandu pastures;
- **Longitudinal Campaigns:**
  - **December 2025:** Rainy summer, high irradiance ($n = 47$; Age: $14.3 \pm 1.3\text{ mo}$; Weight: $293.5 \pm 31.2\text{ kg}$; BGHI: $75.7 \pm 3.2$);
  - **February/March 2026:** Late-rainy summer, peak thermal stress ($n = 46$; Age: $17.3 \pm 1.3\text{ mo}$; Weight: $345.4 \pm 35.8\text{ kg}$; BGHI: $77.3 \pm 3.1$);
  - **July 2026:** Dry winter season, dense winter coat ($n = 40$; Age: $21.4 \pm 1.4\text{ mo}$; Weight: $454.1 \pm 47.0\text{ kg}$; BGHI: $72.1 \pm 5.2$);
- **Reference Standard:** Konica Minolta Chroma Meter CR-400 (d/$0^\circ$, SCI, Illuminant $\text{D}_{65}$, observer $2^\circ$, daily calibrated against white ceramic tile);
- **Validation Partition:** `GroupShuffleSplit` on Animal ID ($80\%$ train = 37 animals / $20\%$ holdout test = 10 unseen animals).

---

## 5. Metrological Results & Statistical Benchmarking

### 5.1. Architectural Ablation Study
Evaluation of spatial grid resolutions ($1 \times 1$, $2 \times 2$, $3 \times 3$, $4 \times 4$) across machine learning algorithms on the independent holdout set:

| Algorithm | Grid Resolution | Train / Test Samples | MAE $L^*$ | MAE $a^*$ | MAE $b^*$ | $\Delta E^*_{ab}$ | $R^2$ |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Random Forest (Selected)** | **$3 \times 3$ (9 cells)** | **1,872 / 504** | **2.472** | **0.625** | **0.907** | **2.923** | **0.791** |
| Random Forest | $1 \times 1$ (Global) | 208 / 56 | 2.369 | 0.558 | 0.816 | 2.778 | 0.838 |
| Random Forest | $4 \times 4$ (16 cells) | 3,328 / 896 | 2.485 | 0.626 | 0.908 | 2.944 | 0.800 |
| Extra Trees | $3 \times 3$ (9 cells) | 1,872 / 504 | 2.539 | 0.632 | 0.903 | 3.002 | 0.782 |
| Gradient Boosting | $3 \times 3$ (9 cells) | 1,872 / 504 | 3.111 | 0.726 | 1.139 | 3.742 | 0.695 |

*Note: While $1 \times 1$ appears competitive on summary metrics, it fails to capture spatial lighting gradients, collapsing under off-center hair orientations. The $3 \times 3$ grid was selected as optimal for production robustness.*

### 5.2. Agreement with Cluster Bootstrap 95% CIs
Evaluated on the full longitudinal dataset (132 skin and 131 coat readings, $N = 46$ cattle). Confidence intervals derived via **5,000 animal-level cluster bootstrap resamples**:

| Tissue & Channel | $n$ | Pearson $r$ [95% CI] | Lin CCC [95% CI] | MAE [95% CI] | RMSE [95% CI] | Mean Bias [95% CI] | LoA 95% (Repeated Measures) | OLS Slope $\beta$ [95% CI] |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$L^*$ (skin)** | 132 | 0.652 [0.473, 0.768] | 0.588 [0.413, 0.711] | 1.307 [1.130, 1.496] | 1.684 [1.448, 1.932] | +0.039 [-0.321, +0.388] | [-3.34, +3.35] | 0.410 [0.278, 0.538] |
| **$a^*$ (skin)** | 132 | 0.839 [0.758, 0.902] | 0.793 [0.689, 0.868] | 0.842 [0.672, 1.038] | 1.237 [0.922, 1.582] | -0.016 [-0.198, +0.163] | [-2.45, +2.42] | 0.598 [0.487, 0.703] |
| **$b^*$ (skin)** | 132 | 0.892 [0.754, 0.946] | 0.849 [0.708, 0.901] | 0.603 [0.513, 0.705] | 0.809 [0.661, 0.958] | -0.008 [-0.182, +0.163] | [-1.61, +1.58] | 0.649 [0.527, 0.709] |
| **$L^*$ (coat)** | 131 | 0.582 [0.428, 0.716] | 0.548 [0.403, 0.663] | 2.882 [2.413, 3.377] | 4.054 [3.289, 4.785] | -0.041 [-0.868, +0.784] | [-8.00, +7.99] | 0.410 [0.312, 0.522] |
| **$a^*$ (coat)** | 131 | 0.875 [0.828, 0.916] | 0.862 [0.810, 0.907] | 0.820 [0.680, 0.971] | 1.133 [0.927, 1.336] | +0.018 [-0.164, +0.199] | [-2.21, +2.25] | 0.738 [0.662, 0.817] |
| **$b^*$ (coat)** | 131 | 0.818 [0.757, 0.865] | 0.785 [0.721, 0.834] | 1.013 [0.875, 1.169] | 1.320 [1.125, 1.528] | +0.030 [-0.213, +0.276] | [-2.57, +2.63] | 0.613 [0.543, 0.686] |

### 5.3. Global Color Difference ($\Delta E^*_{ab}$) by Season

| Tissue Target | Seasonal Period | $n$ | Mean $\pm$ SD | Median [Q1--Q3] | 95th Percentile | $\% < 1.0$ (Imperceptible) | $\% < 3.0$ (Lab Equivalent) | $\% < 5.0$ (Industry Match) |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Skin** | **All Campaigns** | **132** | **1.87 $\pm$ 1.23** | **1.57 [1.10--2.34]** | **4.12** | **22.7%** | **85.6%** | **97.0%** |
| Skin | December (Summer) | 46 | 1.73 $\pm$ 1.13 | 1.45 [0.88--2.47] | 3.63 | 32.6% | 87.0% | 100.0% |
| Skin | February (Late-Summer) | 46 | 1.99 $\pm$ 1.44 | 1.57 [1.17--2.45] | 5.00 | 21.7% | 80.4% | 93.5% |
| Skin | July (Winter) | 40 | 1.91 $\pm$ 1.08 | 1.67 [1.38--2.16] | 3.63 | 12.5% | 90.0% | 97.5% |
| **Hair Coat** | **All Campaigns** | **131** | **3.47 $\pm$ 2.74** | **2.76 [1.85--4.29]** | **9.54** | **9.9%** | **59.5%** | **83.2%** |
| Hair Coat | December (Summer) | 46 | 2.86 $\pm$ 1.75 | 2.36 [1.60--3.92] | 6.36 | 15.2% | 69.6% | 84.8% |
| Hair Coat | February (Late-Summer) | 45 | 3.28 $\pm$ 2.53 | 2.78 [2.02--3.75] | 6.62 | 4.4% | 62.2% | 88.9% |
| Hair Coat | July (Winter) | 40 | 4.39 $\pm$ 3.59 | 3.47 [2.22--5.15] | 11.95 | 10.0% | 45.0% | 75.0% |

### 5.4. Stability Across Animal Biometrics and Weather Conditions
- **Animal Growth Factors:** Prediction error in skin color is completely invariant to animal chronological age ($r = -0.030, p = 0.73$) and live body weight ($r = -0.080, p = 0.36$), confirming high physiological stability. In hair coat, a weak correlation with age ($r = 0.188, p = 0.031$) and body weight ($r = 0.231, p = 0.008$) is observed, driven exclusively by $L^*$ during winter as cattle develop denser, thicker hair coats;
- **Environmental Robustness:** Optical isolation inside the closed PVC chamber successfully uncouples measurements from ambient solar radiation ($r < 0.15$ with CTR and TMR, $p > 0.05$ after multiplicity control).

### 5.5. Longitudinal Linear Mixed-Effects Models (LMM)
- **Likelihood Ratio Tests (Omnibus Period Effect):** No significant seasonal degradation detected for global color differences ($\log \Delta E^*_{ab}$ skin: $\chi^2 = 2.88, p_{\text{Holm}} = 0.338$; $\log \Delta E^*_{ab}$ coat: $\chi^2 = 4.20, p_{\text{Holm}} = 0.338$);
- **Residual Diagnostics:** Shapiro--Wilk tests confirmed Gaussian behavior on signed errors and $\log \Delta E^*_{ab}$ ($p > 0.05$ or minimal skewness $< 0.40$).

---

## 6. Repository File Structure

```
├── Consolidado_Metricas_Estatisticas_Colorimetro.xlsx  # 16-sheet master spreadsheet of all metrics
├── Metodologia_Colorimetro_Smart_Agricultural_Technology.docx # Submission-ready DOCX methodology
├── Metodologia_Colorimetro_Smart_Agricultural_Technology.md   # Markdown version of methodology
├── analise_estatistica_artigo.py                      # Primary statistical pipeline & baseline LMMs
├── analise_estatistica_complementar.py                # Bootstrap CIs, Lin CCC, descriptive & Gaussian LMMs
├── consolidar_planilha_metricas.py                    # Consolidator generating the master Excel workbook
├── generate_docx_methodology.py                       # Generates paper methodology and compiles DOCX
├── run_statistics.py                                  # Computer vision feature extraction & ML runner
├── pvc_preprocessor.py                                # ROI detection & optical chamber preprocessor
├── tabela_de_ablacao.csv                              # Full architectural ablation benchmark table
├── dados artigo colorimetro 2025 - 2026 (1).xlsx      # Longitudinal field experimental dataset
├── colorimetro_dezembro_2025.csv                      # Instrumental readings (Dec 2025)
├── colorimetro_fevereiro_2026.csv                     # Instrumental readings (Feb 2026)
├── colorimetro_julho_2026.csv                         # Instrumental readings (Jul 2026)
├── colorimeter_regressor_test.onnx                    # Exported edge-deployable ONNX model
├── resultados_estatisticos/                           # Generated analytical CSVs and publication figures
│   ├── concordancia_bootstrap_cluster.csv
│   ├── deltaE_descritivo.csv
│   ├── estabilidade_fatores_animais.csv
│   ├── robustez_ambiental.csv
│   ├── lmm_efeito_periodo_LRT.csv
│   ├── lmm_viés_logDeltaE_efeitos_fixos.csv
│   ├── lmm_viés_logDeltaE_diagnostico.csv
│   ├── metricas_concordancia.csv
│   ├── regressao_linear.csv
│   ├── bland_altman.csv
│   ├── resumo_geral.csv
│   ├── modelo_linear_misto.csv
│   ├── modelo_linear_misto_efeitos_fixos.csv
│   ├── modelo_linear_misto_diagnostico.csv
│   ├── bland_altman.png
│   ├── concordancia_scatter.png
│   ├── regressao_linear.png
│   ├── boxplot_erro_periodo.png
│   ├── robustez_heatmap.png
│   └── robustez_dispersao.png
├── requirements.txt                                   # Python dependencies
├── .gitignore                                         # Git ignore rules
├── LICENSE                                            # MIT License
└── README.md                                          # This repository documentation
```

---

## 7. Quickstart & Reproducibility Guide

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/thiagobauce/Colorimetro-Bovino-EdgeAI.git
cd Colorimetro-Bovino-EdgeAI

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Reproduce Primary Statistical Metrics
```bash
python3 analise_estatistica_artigo.py
```
*Outputs generated in `resultados_estatisticos/` (classical metrics, regression plots, Bland-Altman diagrams).*

### Step 3: Reproduce Cluster Bootstrap & Mixed-Effects Models
```bash
python3 analise_estatistica_complementar.py
```
*Outputs generated in `resultados_estatisticos/` (5,000 cluster bootstrap iterations, Lin's CCC, LRT seasonal tests).*

### Step 4: Re-generate the Master Consolidated Excel Workbook
```bash
python3 consolidar_planilha_metricas.py
```
*Compiles all 15 analytical CSV tables into `Consolidado_Metricas_Estatisticas_Colorimetro.xlsx` with an indexed traceability sheet.*

### Step 5: Re-generate Submission-Ready Manuscript & DOCX
```bash
python3 generate_docx_methodology.py
```
*Compiles the complete methodology document into `Metodologia_Colorimetro_Smart_Agricultural_Technology.docx`.*

---

## 8. Citation & Acknowledgments
If you use this codebase, methodology, or dataset in your academic research, please cite:

```bibtex
@article{Godoy2026BovineColorimetry,
  title={Development and Validation of a Smartphone-Based Computer Vision and Machine Learning System for In-Field Bovine Skin and Hair Coat Colorimetry},
  author={de Godoy, Camila and Melo, Max and et al.},
  journal={Smart Agricultural Technology},
  year={2026},
  publisher={Elsevier}
}
```

**Institutional Acknowledgments:**  
- **UFMS:** Faculty of Veterinary Medicine and Animal Science, Federal University of Mato Grosso do Sul;
- **Embrapa Beef Cattle:** Brazilian Agricultural Research Corporation (*Embrapa Gado de Corte*), Campo Grande, MS, Brazil.
