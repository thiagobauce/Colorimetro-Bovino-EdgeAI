# Development and Validation of a Smartphone-Based Computer Vision and Machine Learning System for In-Field Bovine Skin and Hair Coat Colorimetry: Comprehensive Methodology

**Target Journal:** *Smart Agricultural Technology* (Elsevier)  
**Authors / Affiliation:** Faculty of Veterinary Medicine and Animal Science, Federal University of Mato Grosso do Sul (UFMS) & Brazilian Agricultural Research Corporation (Embrapa Beef Cattle -- *Embrapa Gado de Corte*), Campo Grande, MS, Brazil.

---

### Research Objectives
- **General Objective:** To develop and validate an artificial intelligence-driven computational methodology to accurately estimate the skin and hair coat color of Nellore cattle under operational tropical field conditions.
- **Specific Objectives:**
  1. To compare computational smartphone computer vision estimates directly against ground-truth instrumental tristimulus colorimetry;
  2. To evaluate the temporal stability and metrological agreement between methods across distinct seasonal campaigns in relation to dynamic environmental microclimate conditions and biological animal growth factors (chronological age and body weight);
  3. To develop, optimize, and validate a standalone mobile application (Edge-AI) for in-field commercial utilization, providing instantaneous, offline colorimetric diagnostics capable of replacing costly benchtop instruments without compromising metrological precision.

---

# PART I: ENGLISH VERSION (SUBMISSION-READY)

## 1. Material and Methods

### 1.1. Experimental Site, Bioethics, and Longitudinal Cattle Cohort
The experimental research was carried out at the Beef Cattle Experimental Station of the Brazilian Agricultural Research Corporation (Embrapa Beef Cattle -- *Embrapa Gado de Corte*), situated in Campo Grande, Mato Grosso do Sul, Central-Western Brazil ($20^\circ 26' 41.5''\text{ S}$, $54^\circ 43' 21.3''\text{ W}$, altitude $530\text{ m}$ above sea level). The regional landscape belongs to the Brazilian Cerrado biome (Neotropical Savanna), characterized by a tropical wet-and-dry climate classified as *Aw* according to the Köppen-Geiger system. The local climate exhibits two well-defined seasons: a hot, convective rainy season between October and April, and a pronounced dry winter season between May and September.

All animal handling protocols, sampling interventions, trichotomy procedures, and optical measurements strictly complied with the ethical guidelines for animal experimentation established by the National Council for Animal Experimentation Control (CONCEA, Brazil). The research protocol was formally submitted, evaluated, and approved by the Ethics Committee on Animal Use (CEUA -- *Comitê de Ética no Uso de Animais*) of Embrapa Beef Cattle under Certificate Protocol No. 002/2022.

The experimental cohort initially enrolled $N = 47$ intact young male Nellore cattle (*Bos indicus*) managed under extensive rotational grazing on tropical pastures (*Urochloa brizantha* cv. Marandu) with *ad libitum* access to fresh water and mineral supplementation. Standard veterinary sanitary procedures (vaccination against clostridiosis, foot-and-mouth disease, and brucellosis, along with targeted ecto- and endoparasiticide applications) were uniformly maintained. Longitudinal experimental campaigns were executed across three contrasting meteorological periods:
1. **December 2025 (1--5 December; $n = 47$ animals evaluated):** Mid-rainy summer season with high solar irradiance and temperature ($27.0 \pm 3.0\,^\circ\text{C}$, relative humidity $56.2 \pm 12.5\%$, Black Globe Humidity Index [BGHI/ITGU] $75.7 \pm 3.2$). Mean animal age was $14.30 \pm 1.27\text{ months}$ and mean live body weight was $293.5 \pm 31.2\text{ kg}$;
2. **February/March 2026 (28 February--6 March; $n = 46$ animals evaluated):** Late-rainy summer season exhibiting maximum cumulative thermal load ($26.6 \pm 1.8\,^\circ\text{C}$, $72.5 \pm 9.3\%$, BGHI $77.3 \pm 3.1$). Mean animal age was $17.27 \pm 1.27\text{ months}$ and body weight reached $345.4 \pm 35.8\text{ kg}$;
3. **July 2026 (30 June--3 July; $n = 40$ animals evaluated):** Dry winter season characterized by milder thermal conditions ($23.7 \pm 4.0\,^\circ\text{C}$, $77.1 \pm 8.3\%$, BGHI $72.1 \pm 5.2$) and dense, thicker hair coats. Mean animal age was $21.37 \pm 1.35\text{ months}$ and body weight was $454.1 \pm 47.0\text{ kg}$.

On each sampling day, data collection was conducted exclusively between 09:00 and 12:00 h to standardize diurnal circadian rhythms. Six animals (IDs 2372, 2384, 2393, 2404, 2420, and 2421) were not available during the July campaign due to routine herd management culling, and animal ID 2382 was measured only in December. Consequently, the longitudinal agreement dataset comprises 46 animals followed across repeated seasons (132 paired observations for skin and 131 for hair coat, with one coat image corrupted in February).

### 1.2. Ground-Truth Reference Instrumentation: Tristimulus Colorimetry
Physical ground-truth colorimetric measurements were recorded using a benchtop-grade commercial tristimulus spectrophotometer/colorimeter (Chroma Meter CR-400, Konica Minolta Inc., Tokyo, Japan). The optical measuring head features a diffuse illumination / $0^\circ$ viewing angle optical geometry (d/$0^\circ$, specular component included -- SCI), adhering to standard recommendations of the Commission Internationale de l’Éclairage (CIE). Illumination is generated by an ultra-stable pulsed xenon arc lamp, and the spectral flux reflected from the biological specimen is detected by an integrated array of six high-sensitivity silicon photocells configured in a dual-beam monitoring system to cancel source fluctuations.

The optical head incorporates an $8\text{ mm}$ circular measurement aperture and an $11\text{ mm}$ illumination field. The instrument features a short-term repeatability precision of $\Delta E^*_{ab} \le 0.07$ (standard deviation based on 30 measurements on standard white tile) and an inter-instrument agreement within $\Delta E^*_{ab} \le 0.60$. Readings were collected in the three-dimensional CIELAB uniform color space (CIE 1976), configured with CIE Standard Illuminant $\text{D}_{65}$ (correlated color temperature $\approx 6504\text{ K}$) and the CIE $1931$ standard $2^\circ$ colorimetric observer:
- $L^*$ (Psychometric Lightness): Scaled from 0 (ideal black) to 100 (diffuse perfect white diffuser);
- $a^*$ (Green--Red Chromatic Opponency): Negative coordinates represent green and positive denote red;
- $b^*$ (Blue--Yellow Chromatic Opponency): Negative coordinates represent blue and positive denote yellow.

Daily calibration was executed prior to each chute operation against the manufacturer standard white ceramic calibration plate ($Y = 92.4$, $x = 0.3160$, $y = 0.3323$). For each individual animal and tissue target (shaved epidermal skin and intact hair coat), a single, highly stabilized instrumental reading was recorded at the exact center of the designated anatomical patch, providing the target reference vector:

$$\mathbf{y}_{\text{ref}} = [L^*_{\text{ref}}, a^*_{\text{ref}}, b^*_{\text{ref}}]^\top$$

### 1.3. Animal Restraint, Trichotomy, and Biosanitary Patch Preparation
To eliminate motion artifacts, cattle were moved calmly through the holding chute into a heavy-duty hydraulic squeeze crush (*tronco de contenção mecânico/hidráulico*). The operational sampling area was established on the left dorsal flank, approximately $20\text{ cm}$ ventral to the vertebral spine, equidistant between the caudal edge of the scapula and the iliac crest:
1. **Intact Coat Preparation:** A square anatomical region of $10 \times 10\text{ cm}$ ($100\text{ cm}^2$) was selected. Hair fibers were cleaned using a soft anti-static grooming brush to remove superficial dust, pasture dirt, and dander without disturbing natural fiber orientation or damaging the keratin cuticles.
2. **Epidermal Exposure via Trichotomy:** Contiguous to the coat patch, an anatomical window of approximately $5\text{ cm}^2$ was designated for skin assessment. Complete trichotomy was performed using sterile disposable surgical scalpel blades (Carbon Steel No. 22). Shaving was conducted parallel to hair growth to slice fibers flush with follicular ostia. The area was monitored to ensure absolute absence of lacerations, micro-abrasions, or cutaneous hyperemia, which would otherwise introduce confounding hemoglobin absorption bands ($\approx 542\text{ nm}$ and $577\text{ nm}$) into the baseline melanin spectrum.
3. **Traceability:** High-contrast ear-tag registration numbers were verified against laboratory datasheets, ensuring bidirectional cross-referencing between digital imagery, environmental logs, and colorimetric records.

### 1.4. In-Field Optical Isolation Chamber and Synchronized Edge Image Acquisition
Ambient outdoor lighting under tropical field conditions exhibits severe stochastic fluctuations (direct sunlight $> 100,000\text{ lux}$, passing cloud occlusions, tree canopy shadows, and varying correlated color temperatures from $4,000\text{ K}$ to $> 15,000\text{ K}$). To establish controlled optical conditions, a custom-engineered portable light-tight isolation chamber was fabricated:
- **Cylindrical Structural Barrel:** Fabricated from rigid polyvinyl chloride (PVC) with an axial length of $20\text{ cm}$ and an internal diameter of $10\text{ cm}$. The length was optically engineered to maintain the camera lens at its optimal focal distance while preventing optical flare;
- **Anti-Reflective Internal Coating:** The inner circumferential barrel walls were coated with ultra-matte, non-reflective optical black paint (specular reflectance $< 1.5\%$ across $380--750\text{ nm}$), eliminating internal cross-reflections;
- **Anatomical Conformable Rubber Seal:** The distal end was fitted with a flexible closed-cell neoprene gasket that adapts to the convex curvature of the bovine flank, establishing complete optical sealing against ambient daylight infiltration;
- **Precision Smartphone Mount:** The proximal end incorporated a high-density thermoplastic adapter that rigidly centers the smartphone camera aperture and the onboard LED flash over the cylinder axis.

Digital image capture was executed using a smartphone with manual hardware API control. Camera settings were locked in manual mode: ISO 100, exposure time $1/125\text{ s}$, fixed manual focal distance, and raw white balance override. Illumination was provided exclusively by the synchronized onboard LED flash unit firing inside the sealed optical chamber.

### 1.5. Computer Vision Pipeline and Spatial Preprocessing
The acquired digital frames were ingested into an automated computer vision pipeline:
1. **Chromatic Correction via Gray World Algorithm:** Despite chamber isolation, the white LED flash exhibits non-uniform spectral power distribution with high correlated color temperature (CCT $\approx 5,500--6,500\text{ K}$) and a pronounced blue emission peak ($\approx 450\text{ nm}$). To normalize color casts, the Gray World color constancy algorithm was implemented under the physical postulate that the average surface reflectance across a complex biological scene is achromatic (neutral gray):

$$\bar{R} = \frac{1}{N_p} \sum_{p=1}^{N_p} R(p), \quad \bar{G} = \frac{1}{N_p} \sum_{p=1}^{N_p} G(p), \quad \bar{B} = \frac{1}{N_p} \sum_{p=1}^{N_p} B(p)$$

$$\mu_{\text{gray}} = \frac{\bar{R} + \bar{G} + \bar{B}}{3}$$

$$\alpha_R = \frac{\mu_{\text{gray}}}{\bar{R}}, \quad \alpha_G = \frac{\mu_{\text{gray}}}{\bar{G}}, \quad \alpha_B = \frac{\mu_{\text{gray}}}{\bar{B}}$$

Each pixel was rescaled as $I_{\text{balanced}}(p) = [\alpha_R R(p), \alpha_G G(p), \alpha_B B(p)]^\top$, normalizing lighting chromaticity.
2. **Morphological ROI Extraction:** The circular interior opening of the PVC chamber was segmented by applying a Gaussian spatial filter ($61 \times 61$, $\sigma = 10$) followed by Otsu adaptive thresholding and morphological opening (structuring element $B = 45 \times 45$) to isolate the biological tissue target;
3. **Spatial Grid Discretization ($3 \times 3$ Matrix):** Flash illumination within a cylindrical chamber generates a radial luminance gradient (perpendicular incident light at the center, progressive angular attenuation toward peripheral margins). A single global average would collapse this spatial gradient and dilute local bio-optical information. Therefore, the segmented bounding region was partitioned into a regular $3 \times 3$ matrix (9 distinct spatial sub-blocks: 1 central core region receiving direct specular flash and 8 peripheral blocks capturing diffuse backscattering).

### 1.6. Multichannel Photometric Feature Engineering (14 Descriptors)
From each of the 9 spatial grid blocks, a 14-dimensional photometric feature vector was extracted, combining primary color spaces with non-linear bio-optical ratios:
- **Direct Multi-Space Channels (9 features):**
  - RGB channels: Mean Red ($R$), Green ($G$), and Blue ($B$) intensities ($0--255$);
  - HSV channels: Mean Hue ($H$, angular chromatic tone), Saturation ($S$, purity of pigmentation), and Value ($V$, perceived optical brightness);
  - OpenCV CIELAB channels: Scaled lightness ($L_{\text{cv2}}$), green--red ($a_{\text{cv2}}$), and blue--yellow ($b_{\text{cv2}}$);
- **Non-Linear Bio-Optical Ratios and Invariant Descriptors (5 features):**
  - $\text{Razao}_{\text{RG}} = \frac{R}{G + \epsilon}$: Erythema and micro-vascularization index, sensitive to dermal perfusion;
  - $\text{Razao}_{\text{RB}} = \frac{R}{B + \epsilon}$: Cutaneous pigmentation index, sensitive to eumelanin vs. pheomelanin ratios;
  - $\text{Razao}_{\text{GB}} = \frac{G}{B + \epsilon}$: Structural keratin scattering ratio, sensitive to hair cuticle fiber density;
  - $\text{Dif}_{LV} = L_{\text{cv2}} - V$: Decoupling metric between perceptual psychometric lightness and achromatic photonic intensity, neutralizing residual flash glare;
  - $\text{Soma}_{\text{RGB}} = R + G + B$: Total photometric energy proxy, measuring gross integrated backscattered photon flux.

### 1.7. Machine Learning Modeling, Dual-Specialist Architecture, and Ablation Study
Bovine skin (epidermis/dermis with high micro-vascularity, melanin granule clusters, and subsurface volume scattering) and intact hair coat (keratinized cuticular cylinders, air-filled medullary cavities, and anisotropic surface reflection) exhibit fundamentally distinct Bidirectional Reflectance Distribution Functions (BRDF). Unifying both tissues into a single regressor creates conflicting mathematical decision boundaries.

To address this bio-optical disparity, a **dual specialized architecture** was established:
1. **Skin-Specialist Regressor ($\mathcal{M}_{\text{skin}}$):** Trained exclusively on trichotomized epidermal patches;
2. **Coat-Specialist Regressor ($\mathcal{M}_{\text{coat}}$):** Trained exclusively on intact hair coat specimens.

To identify the optimal spatial discretization and regression algorithm, a systematic **architectural ablation experiment** was conducted evaluating four grid resolutions ($1 \times 1$, $2 \times 2$, $3 \times 3$, and $4 \times 4$, generating 1, 4, 9, and 16 spatial instances per image) across three machine learning algorithms:
- **Random Forest Regressor:** Ensemble of $B = 200$ randomized decision trees with bootstrap aggregation (bagging) and maximum tree depth constrained to $\text{max\_depth} = 15$;
- **Extra Trees Regressor:** Ensemble of $B = 200$ extremely randomized trees where cut-points are drawn completely at random;
- **Gradient Boosting Regressor:** Ensembled under a `MultiOutputRegressor` wrapper with $B = 200$ boosting stages, learning rate $\eta = 0.05$, and tree depth 15.

The complete ablation results across 12 architecture--grid configurations (Table S1) demonstrated that the **Random Forest with a $3 \times 3$ grid (9 cells)** achieved the superior balance between precision and generalization ($\Delta E^*_{ab} = 2.923$, $R^2 = 0.791$, $\text{MAE}_{L^*} = 2.472$, $\text{MAE}_{a^*} = 0.625$, $\text{MAE}_{b^*} = 0.907$), significantly outperforming single global crops and Gradient Boosting models (which exhibited overfitting to localized flash specularities).

### 1.8. Validation Protocol: Group-Level Subject Isolation (`GroupShuffleSplit`)
To ensure genuine generalization and prevent data leakage and pseudoreplication, simple random splitting (`train_test_split`) was prohibited. Because individual cattle share unique phenotypic coat textures, skin topography, and melanin distributions, distributing sub-grid blocks or repeated photographs of the same animal across both training and test partitions would cause models to memorize individual animal signatures rather than learning universal bio-optical color mappings.

Validation was enforced using `GroupShuffleSplit` structured strictly on unique biological subject identifiers ($\text{Group} = \text{Animal ID}$):
- **Training Partition (80% of subjects):** 37 unique animals (1,872 spatial sub-grid instances for grid 9);
- **Independent Test Partition (20% of subjects):** 10 completely unseen animals (504 spatial sub-grid instances for grid 9).

No image, sub-block, or measurement from any training animal ever entered the test set, guaranteeing that reported performance benchmarks reflect deployment on novel animals in field operations.

### 1.9. Commercial Edge-AI Android Mobile Application Architecture
To provide an immediate, accessible tool for commercial beef cattle breeding, precision livestock management, and thermal comfort research, the complete computational vision and Random Forest dual-specialist pipeline was compiled into a native Android mobile application:
- **Core Technology Stack:** Developed in Kotlin and native C++ using the OpenCV Android SDK (v4.8.0) and the ONNX Runtime execution engine (v1.16);
- **Model Quantization and Serialization:** The trained scikit-learn Random Forest models were exported to the Open Neural Network Exchange (ONNX) format with dynamic 8-bit float quantization (`float32` weights serialized to compact binary payloads $< 8.5\text{ MB}$);
- **Autonomous Edge Execution:** The mobile app executes entirely offline without requiring internet, cellular reception, or cloud computing infrastructure. Hardware camera APIs programmatically control camera ISO, shutter speed, and flash triggering;
- **Real-Time Inference Latency:** Image capture, Gray World normalization, circular segmentation, 14-feature multi-grid extraction, and ONNX model inference execute in $< 140\text{ ms}$ on mid-range and high-end smartphone hardware;
- **User Interface:** The mobile GUI displays real-time calibrated $L^*, a^*, b^*$ values, perceptual difference classifications, and historical animal tagging logs directly at chute side.

### 1.10. Comprehensive Statistical and Metrological Evaluation Framework
To rigorously evaluate the system's viability as a commercial replacement for physical colorimeters, a multi-faceted statistical framework was executed using Python (SciPy, statsmodels):

#### 1.10.1. Comparative Instrumental Agreement Metrics
Model predictions ($y_{\text{app}}$) were benchmarked against benchtop colorimeter readings ($y_{\text{ref}}$) on the longitudinal field dataset (132 skin and 131 coat observations across $N = 46$ cattle):
- **Mean Absolute Error (MAE):** $\text{MAE}_k = \frac{1}{N} \sum_{i=1}^N |y_{\text{app},i,k} - y_{\text{ref},i,k}|$, for $k \in \{L^*, a^*, b^*\}$;
- **Root Mean Squared Error (RMSE):** $\text{RMSE}_k = \sqrt{\frac{1}{N} \sum_{i=1}^N (y_{\text{app},i,k} - y_{\text{ref},i,k})^2}$;
- **Pearson Product-Moment Correlation Coefficient ($r$):** Standard linear association metric;
- **Lin Concordance Correlation Coefficient (CCC, $\rho_c$):** Combines precision (Pearson $r$) and accuracy ($C_b$, bias correction factor):
  $$\rho_c = \frac{2 s_{xy}}{s_x^2 + s_y^2 + (\bar{x} - \bar{y})^2} = r \cdot C_b$$
  where $s_{xy}$ is the sample covariance, $s_x^2$ and $s_y^2$ are sample variances, and $\bar{x}, \bar{y}$ are sample means.
- **Animal-Level (Cluster) Percentile Bootstrap:** Because individual animals contributed repeated measurements across three seasons, standard parametric confidence intervals that assume independent and identically distributed (i.i.d.) observations would underestimate standard errors. Therefore, 95% confidence intervals for $r$, CCC, MAE, RMSE, mean bias, and OLS regression slopes were derived using an **animal-level cluster bootstrap** ($B = 5,000$ resamples of animals with replacement; seed = 42).

#### 1.10.2. Global Perceptual Color Difference (CIE 1976 $\Delta E^*_{ab}$)
Overall color deviation was computed via the Euclidean distance in CIELAB space:

$$\Delta E^*_{ab} = \sqrt{(L^*_{\text{app}} - L^*_{\text{ref}})^2 + (a^*_{\text{app}} - a^*_{\text{ref}})^2 + (b^*_{\text{app}} - b^*_{\text{ref}})^2}$$

Perceptual and metrological equivalence thresholds were categorized according to CIE standards:
- $\Delta E^*_{ab} < 1.0$: Imperceptible to the human eye;
- $1.0 \le \Delta E^*_{ab} \le 3.0$: Perceptible only by trained observers; standard threshold for instrumental laboratory equivalence;
- $3.0 < \Delta E^*_{ab} \le 5.0$: Acceptable industrial color matching tolerance;
- $\Delta E^*_{ab} > 5.0$: Pronounced color disparity.

#### 1.10.3. Repeated-Measures Bland--Altman Agreement and Proportional Bias Analysis
To assess method interchangeability under repeated sampling, a repeated-measures Bland--Altman analysis was conducted. For each pair $(i, j)$ (animal $i$, campaign $j$), the difference $d_{ij} = y_{\text{app},ij} - y_{\text{ref},ij}$ and mean $m_{ij} = (y_{\text{app},ij} + y_{\text{ref},ij})/2$ were computed.

The total variance of differences was partitioned into between-animal variance ($\sigma^2_u$) and within-animal (residual) variance ($\sigma^2_e$) by fitting an intercept-only Linear Mixed-Effects Model:

$$d_{ij} = \bar{d} + u_i + \varepsilon_{ij}, \quad u_i \sim \mathcal{N}(0, \sigma_u^2), \quad \varepsilon_{ij} \sim \mathcal{N}(0, \sigma_e^2)$$

The 95% Limits of Agreement for repeated measures were calculated as:

$$\text{LoA}_{95\%} = \bar{d} \pm 1.96 \sqrt{\hat{\sigma}_u^2 + \hat{\sigma}_e^2}$$

Proportional bias was formally tested by fitting Ordinary Least Squares (OLS) regressions ($y_{\text{app}} = \alpha + \beta y_{\text{ref}}$) and evaluating $H_0: \beta = 1.0$ and $H_0: \alpha = 0$, supported by cluster bootstrap confidence intervals for $\beta$.

#### 1.10.4. Agreement Stability: Animal Biometrics and Environmental Microclimate
To evaluate whether system accuracy is sensitive to animal growth or environmental fluctuations, bivariate Pearson ($r$) and Spearman ($\rho$) correlation coefficients were computed between prediction errors (absolute channel errors and $\Delta E^*_{ab}$) and two distinct groups of operational variables:
1. **Animal Biometric and Physiological Growth Factors:**
   - Chronological Age (months, spanning $11.9--24.1\text{ months}$);
   - Live Body Weight (kg, spanning $217.7--549.4\text{ kg}$);
   - Average Daily Gain (ADG / GMD slope, kg/day, spanning $0.39--1.93\text{ kg/day}$).
2. **Field Meteorological and Microclimatic Variables:**
   - Dry-bulb Air Temperature ($^\circ\text{C}$);
   - Relative Air Humidity (\%RH);
   - Thermal Radiation Load (CTR, $\text{W/m}^2$);
   - Mean Radiant Temperature (TMR, $\text{K}$);
   - Black Globe Humidity Index (BGHI / ITGU).

#### 1.10.5. Longitudinal Linear Mixed-Effects Modeling (LMM)
To model the longitudinal stability of measurement agreement across campaigns while accounting for subject-level clustering, Linear Mixed-Effects Models were fitted via Restricted Maximum Likelihood (REML):

$$z_{ij} = \beta_0 + \beta_1 \cdot \text{Feb}_{ij} + \beta_2 \cdot \text{Jul}_{ij} + u_i + \varepsilon_{ij}$$

where $z_{ij}$ represents:
- The **signed error (bias)** for each of the six color channels ($L^*, a^*, b^*$ for skin and coat);
- The **log-transformed color difference** ($\log \Delta E^*_{ab}$ for skin and coat).

*Rationale for Response Selection:* Preliminary residual diagnostics revealed that models fitted to untransformed $\Delta E^*_{ab}$ or raw absolute errors severely violated Gaussian assumptions (Shapiro--Wilk $p < 10^{-7}$, positive skewness $> 1.4$). In contrast, signed errors and $\log \Delta E^*_{ab}$ exhibited near-normal residuals (Shapiro--Wilk $p > 0.05$ or low skewness).

The omnibus effect of campaign period was evaluated using Likelihood Ratio Tests (LRT) between full and intercept-only models fitted by Maximum Likelihood (ML), with $p$-values adjusted across responses using the Holm step-down procedure. Intraclass Correlation Coefficients ($\text{ICC} = \hat{\sigma}_u^2 / (\hat{\sigma}_u^2 + \hat{\sigma}_e^2)$), fixed-effect estimates, standard errors, and 95% Wald confidence intervals were compiled.

---

# PART II: VERSÃO COMPLETA EM PORTUGUÊS

## 1. Material e Métodos

### 1.1. Local Experimental, Aspectos Éticos e Coorte Bovina Longitudinal
O estudo experimental foi conduzido na Estação Experimental de Gado de Corte da Empresa Brasileira de Pesquisa Agropecuária (Embrapa Gado de Corte), em Campo Grande, Mato Grosso do Sul, Brasil ($20^\circ 26' 41{,}5''\text{ S}$, $54^\circ 43' 21{,}3''\text{ O}$, altitude de $530\text{ m}$). A região insere-se no bioma Cerrado, com clima tropical de savana (*Aw* segundo Köppen-Geiger), marcado por duas estações nítidas: verão quente e chuvoso (outubro a abril) e inverno seco (maio a setembro).

Todos os manejos, contenções, procedimentos de tricotomia e mensurações ópticas seguiram rigorosamente as diretrizes éticas do Conselho Nacional de Controle de Experimentação Animal (CONCEA, Brasil). O protocolo foi aprovado pelo Comitê de Ética no Uso de Animais (CEUA) da Embrapa Gado de Corte sob o Certificado de Protocolo nº 002/2022.

A coorte experimental foi composta inicialmente por $N = 47$ machos inteiros da raça Nelore (*Bos indicus*), criados sob pastejo rotacionado em pastagem tropical (*Urochloa brizantha* cv. Marandu) com água e suplementação mineral *ad libitum*. O manejo profilático e sanitário (vacinações obrigatórias e controle estratégico de endo e ectoparasitas) foi executado uniformemente. Três campanhas experimentais foram executadas em períodos meteorológicos contrastantes:
1. **Dezembro de 2025 (01 a 05/12; $n = 47$ animais avaliados):** Pleno verão chuvoso, com alta radiação solar e temperatura ($27{,}0 \pm 3{,}0\,^\circ\text{C}$, umidade relativa $56{,}2 \pm 12{,}5\%$, ITGU $75{,}7 \pm 3{,}2$). A idade média foi de $14{,}30 \pm 1{,}27\text{ meses}$ e o peso corporal de $293{,}5 \pm 31{,}2\text{ kg}$;
2. **Fevereiro/Março de 2026 (28/02 a 06/03; $n = 46$ animais avaliados):** Final de verão com elevado estresse térmico acumulado ($26{,}6 \pm 1{,}8\,^\circ\text{C}$, $72{,}5 \pm 9{,}3\%$, ITGU $77{,}3 \pm 3{,}1$). A idade média alcançou $17{,}27 \pm 1{,}27\text{ meses}$ e o peso $345{,}4 \pm 35{,}8\text{ kg}$;
3. **Julho de 2026 (30/06 a 03/07; $n = 40$ animais avaliados):** Inverno seco, com temperaturas mais amenas ($23{,}7 \pm 4{,}0\,^\circ\text{C}$, $77{,}1 \pm 8{,}3\%$, ITGU $72{,}1 \pm 5{,}2$) e pelame mais denso e espesso. A idade média foi de $21{,}37 \pm 1{,}35\text{ meses}$ e o peso corporal médio de $454{,}1 \pm 47{,}0\text{ kg}$.

As coletas foram padronizadas entre 09:00 e 12:00 h. Seis animais (IDs 2372, 2384, 2393, 2404, 2420 e 2421) foram descartados em julho por razões de manejo zootécnico, e o animal 2382 foi avaliado unicamente em dezembro. Portanto, o conjunto longitudinal de concordância compreende 46 animais acompanhados ao longo das campanhas (132 pares de observações de pele e 131 de pelame).

### 1.2. Equipamento Padrão de Referência: Colorímetro Tristímulo
As mensurações físicas padrão-ouro foram obtidas por meio de um colorímetro/espectrofotômetro tristímulo portátil de padrão laboratorial (Chroma Meter CR-400, Konica Minolta Inc., Tóquio, Japão). O cabeçote óptico opera com geometria de iluminação difusa e ângulo de observação de $0^\circ$ (d/$0^\circ$, componente especular incluído -- SCI), em conformidade com as normas da Commission Internationale de l’Éclairage (CIE). A iluminação é gerada por lâmpada de arco de xenônio pulsado de alta estabilidade, e o feixe refletido é captado por seis fotocélulas de silício em arquitetura de duplo feixe para compensar flutuações de intensidade.

O cabeçote possui abertura circular de medição de $8\text{ mm}$ e campo de iluminação de $11\text{ mm}$, com repetibilidade de $\Delta E^*_{ab} \le 0{,}07$ e concordância inter-instrumentos dentro de $\Delta E^*_{ab} \le 0{,}60$. As leituras foram configuradas no espaço uniforme CIELAB (CIE 1976), sob Iluminante Padrão CIE $\text{D}_{65}$ (temperatura de cor correlata $\approx 6504\text{ K}$) e observador padrão colorimétrico CIE $1931$ de $2^\circ$:
- $L^*$ (Luminosidade Psicométrica): Varia de 0 (preto absoluto) a 100 (branco difuso ideal);
- $a^*$ (Oponência Verde--Vermelho): Valores negativos indicam verde e positivos indicam vermelho;
- $b^*$ (Oponência Azul--Amarelo): Valores negativos indicam azul e positivos indicam amarelo.

A calibração do equipamento foi executada diariamente antes de cada rotina contra a placa cerâmica branca padrão ($Y = 92{,}4$, $x = 0{,}3160$, $y = 0{,}3323$). Para cada animal e tecido (pele tricotomizada e pelame intacto), foi registrada uma única leitura estabilizada no centro da área anatômica demarcada, definindo o vetor de referência:

$$\mathbf{y}_{\text{ref}} = [L^*_{\text{ref}}, a^*_{\text{ref}}, b^*_{\text{ref}}]^\top$$

### 1.3. Contenção dos Animais, Tricotomia e Preparo do Sítio Anatômico
Os bovinos foram conduzidos individualmente através do brete até o tronco de contenção mecânico/hidráulico para imobilização suave. A área amostral padronizada situou-se no flanco dorsal esquerdo, aproximadamente $20\text{ cm}$ ventral à linha dorsal (coluna vertebral), equidistante entre a borda caudal da escápula e a crista ilíaca:
1. **Preparo do Pelame Intacto:** Demarcou-se uma janela de $10 \times 10\text{ cm}$ ($100\text{ cm}^2$). As cerdas foram suavemente higienizadas com escova antiestática macia para remover poeira, resíduos de pasto e descamações cutâneas, sem alterar a orientação natural dos pelos nem danificar a cutícula;
2. **Exposição Epidérmica por Tricotomia:** Adjacente ao pelame, demarcou-se uma área de aproximadamente $5\text{ cm}^2$. A tricotomia foi realizada com lâminas de bisturi cirúrgico descartável nº 22, no sentido de inserção capilar para seccionar as cerdas rentes aos óstios foliculares. O procedimento foi inspecionado para assegurar ausência total de micro-escoriações ou hiperemia localizada (o que introduziria bandas de absorção da hemoglobina a $\approx 542\text{ nm}$ e $577\text{ nm}$);
3. **Rastreabilidade:** Os números de brinco foram conferidos em formulários digitais e físicos, garantindo correlação direta e bidirecional entre imagens, dados meteorológicos e leituras instrumentais.

### 1.4. Câmara Portátil de Isolamento Óptico e Aquisição Sincronizada
A iluminação natural externa no curral apresenta flutuações extremas de irradiância ($> 100.000\text{ lux}$ sob sol pleno até sombras densas e nuvens) e variação contínua da temperatura de cor. Para neutralizar essas variáveis, desenvolveu-se uma câmara cilíndrica portátil de isolamento óptico:
- **Corpo Cilíndrico:** Fabricado em policloreto de vinila (PVC) rígido com comprimento axial de $20\text{ cm}$ e diâmetro de $10\text{ cm}$, dimensionado para manter o foco ótimo da lente e evitar reflexos parasitas;
- **Revestimento Interno Antirreflexo:** Tratamento interno com tinta preta fosca óptica de ultra-baixa refletância (refletância especular $< 1{,}5\%$ em toda a faixa de $380--750\text{ nm}$);
- **Vedação Anatômica em Neoprene:** A extremidade em contato com o animal recebeu anel de borracha flexível celular que se molda à curvatura do flanco bovino, bloqueando integralmente a luz solar externa;
- **Suporte de Encaixe:** Adaptador rígido na base superior para alinhamento axial preciso entre a câmera do smartphone e a câmara de PVC.

A captura digital foi executada por smartphone com controle manual de hardware via API da câmera (Modo Pro com ISO 100 travado, tempo de exposição de $1/125\text{ s}$, distância focal fixa e balanço de branco desativado). A iluminação do tecido ocorreu exclusivamente pelo disparo sincronizado do flash LED embutido no aparelho.

### 1.5. Pipeline de Visão Computacional e Pré-Processamento Espacial
As imagens foram processadas por um fluxo computacional estruturado:
1. **Normalização Cromática via Algoritmo Gray World:** O flash LED exibe distribuição espectral com temperatura de cor fria ($\approx 5.500--6.500\text{ K}$) e pico azul acentuado ($\approx 450\text{ nm}$). O algoritmo Gray World normalizou as dominantes cromáticas com base na premissa biofísica de que a refletância média da cena biológica integrada tende ao cinza neutro:

$$\mu_{\text{gray}} = \frac{\bar{R} + \bar{G} + \bar{B}}{3}, \quad \alpha_R = \frac{\mu_{\text{gray}}}{\bar{R}}, \quad \alpha_G = \frac{\mu_{\text{gray}}}{\bar{G}}, \quad \alpha_B = \frac{\mu_{\text{gray}}}{\bar{B}}$$

$$I_{\text{corrigido}}(p) = [\alpha_R R(p), \alpha_G G(p), \alpha_B B(p)]^\top$$

2. **Segmentação Morfológica da Região de Interesse (ROI):** Filtro Gaussiano ($61 \times 61$, $\sigma = 10$) seguido de binarização adaptativa de Otsu e abertura morfológica ($B = 45 \times 45$) isolaram com precisão a cavidade circular de tecido biológico;
3. **Discretização em Grade Espacial $3 \times 3$:** O flash em câmara fechada gera atenuação angular centro-periferia. Para preservar essa informação física sem colapsar a imagem em uma única média global, a ROI foi dividida em uma grade $3 \times 3$ (9 células: 1 bloco central com incidência perpendicular direta do flash e 8 blocos periféricos com espalhamento volumétrico difuso).

### 1.6. Engenharia de Atributos Fotométricos Multicanal (14 Variáveis)
De cada uma das 9 células da grade foram extraídos 14 atributos representativos dos regimes de reflexão óptica:
- **Canais Diretos dos Espaços de Cor (9 atributos):**
  - Espaço RGB: Intensidades médias Vermelho ($R$), Verde ($G$) e Azul ($B$);
  - Espaço HSV: Matiz ($H$), Saturação ($S$) e Brilho ($V$);
  - Espaço CIELAB OpenCV: Luminosidade escalada ($L_{\text{cv2}}$), oponência verde-vermelho ($a_{\text{cv2}}$) e azul-amarelo ($b_{\text{cv2}}$);
- **Razões Biofísicas Não Lineares e Descritores Invariantes (5 atributos):**
  - $\text{Razao}_{\text{RG}} = \frac{R}{G + \epsilon}$: Indicador de eritema cutâneo e perfusão micro-vascular dérmica;
  - $\text{Razao}_{\text{RB}} = \frac{R}{B + \epsilon}$: Razão espectral associada à proporção eumelanina/feomelanina;
  - $\text{Razao}_{\text{GB}} = \frac{G}{B + \epsilon}$: Indicador de espalhamento óptico em fibras de queratina capilar;
  - $\text{Dif}_{LV} = L_{\text{cv2}} - V$: Desacoplamento entre brilho perceptual e intensidade acromática, neutralizando pontos especulares de flash;
  - $\text{Soma}_{\text{RGB}} = R + G + B$: Proxy de energia fotométrica total integrada refletida pelo tecido.

### 1.7. Modelagem por Inteligência Artificial, Duplo Especialista e Estudo de Ablação
A pele bovina (espalhamento subsuperficial turbidimétrico em epiderme vascularizada) e o pelame (fibras cilíndricas de queratina com reflexão especular e anisotrópica) possuem funções de reflectância óptica (BRDF) completamente distintas. Modelos unificados geram fronteiras de decisão conflitantes.

Implementou-se, portanto, uma **arquitetura de duplo especialista**:
1. **Regressores Especialistas em Pele ($\mathcal{M}_{\text{pele}}$):** Treinados exclusivamente sobre patches cutâneos tricotomizados;
2. **Regressores Especialistas em Pelame ($\mathcal{M}_{\text{pelo}}$):** Treinados exclusivamente sobre amostras de pelame intacto.

Para fundamentar a seleção da resolução espacial e do algoritmo, executou-se um **experimento sistemático de ablação** comparando 4 resoluções de grade ($1 \times 1$, $2 \times 2$, $3 \times 3$ e $4 \times 4$) e 3 classes de modelos supervisionados:
- **Random Forest:** Ensemble de 200 árvores de decisão com agregação bootstrap (*bagging*) e profundidade máxima 15;
- **Extra Trees:** Ensemble de 200 árvores extremamente aleatorizadas;
- **Gradient Boosting:** Ensembles sequenciais (`MultiOutputRegressor`) com taxa de aprendizado $\eta = 0{,}05$.

Os resultados da ablação (Tabela S1) comprovaram que a **Random Forest na grade $3 \times 3$ (9 células)** alcançou a melhor performance global ($\Delta E^*_{ab} = 2{,}923$, $R^2 = 0{,}791$, $\text{MAE}_{L^*} = 2{,}472$, $\text{MAE}_{a^*} = 0{,}625$, $\text{MAE}_{b^*} = 0{,}907$), superando recortes globais de célula única e modelos de Gradient Boosting (que sofreram sobreajuste a reflexos especulares locais).

### 1.8. Protocolo de Validação: Separação Estrita por Animal (`GroupShuffleSplit`)
Para evitar contaminação de dados (*data leakage*) e pseudorrepetição amostral, foi vetada a amostragem aleatória convencional (`train_test_split`). Como animais individuais compartilham características fenotípicas exclusivas de pelame e pigmentação, alocar recortes de um mesmo animal entre treino e teste faria o modelo memorizar indivíduos em vez de aprender o mapeamento colorimétrico universal.

A partição foi estruturada rigorosamente pelo identificador do animal (`GroupShuffleSplit`, `Group = Animal ID`):
- **Conjunto de Treinamento (80% dos indivíduos):** 37 animais únicos (1.872 amostras de grade);
- **Conjunto de Teste Independente (20% dos indivíduos):** 10 animais completamente inéditos (504 amostras de grade).

Nenhum dado ou imagem dos 10 animais de teste foi exposto aos algoritmos durante o ajuste, assegurando validação genuína para animais desconhecidos em condições reais de campo.

### 1.9. Aplicativo Móvel Edge-AI para Uso Comercial no Campo
Para viabilizar a transferência tecnológica imediata para fazendas comerciais e centros de pesquisa, o pipeline computacional e os modelos Random Forest foram compilados em um aplicativo móvel nativo para o sistema operacional Android:
- **Tecnologias de Desenvolvimento:** Construído em linguagem Kotlin com módulos de processamento de baixo nível em C++ através do OpenCV Android SDK e ONNX Runtime;
- **Serialização e Otimização:** Os modelos treinados foram convertidos para o formato aberto ONNX com quantização dinâmica em ponto flutuante de 8 bits, gerando binários compactos ($< 8{,}5\text{ MB}$);
- **Operação 100% Offline (Edge Computing):** O aplicativo executa inferência autônoma no próprio processador do smartphone, operando plenamente em currais e mangas sem conexão de internet ou sinal de telefonia;
- **Latência Operacional:** O ciclo completo (disparo sincronizado de câmera e flash, normalização Gray World, segmentação, extração das 14 features na grade $3 \times 3$ e inferência ONNX) completa-se em $< 140\text{ ms}$;
- **Interface Gráfica:** Exibe instantaneamente no visor as coordenadas $L^*, a^*, b^*$, a classificação perceptual e o histórico de leituras por brinco do animal.

### 1.10. Metodologia Estatística e Avaliação Metrológica Completa
A avaliação da substituibilidade clínica e da estabilidade metrológica seguiu procedimentos computacionais avançados em Python:

#### 1.10.1. Métricas de Concordância Metrológica
No conjunto longitudinal completo (132 observações de pele e 131 de pelame em 46 animais), calcularam-se:
- **Erro Médio Absoluto (MAE):** $\text{MAE}_k = \frac{1}{N} \sum |y_{\text{app},i,k} - y_{\text{ref},i,k}|$;
- **Raiz do Erro Quadrático Médio (RMSE):** $\text{RMSE}_k = \sqrt{\frac{1}{N} \sum (y_{\text{app},i,k} - y_{\text{ref},i,k})^2}$;
- **Coeficiente de Correlação de Pearson ($r$):** Associação linear univariada;
- **Coeficiente de Correlação de Concordância de Lin (CCC, $\rho_c$):** Mede simultaneamente precisão ($r$) e acurácia ($C_b$):
  $$\rho_c = \frac{2 s_{xy}}{s_x^2 + s_y^2 + (\bar{x} - \bar{y})^2}$$
- **Bootstrap por Conglomerado (Cluster/Animal-Level Bootstrap):** Devido à dependência intra-animal das medidas repetidas, intervalos de confiança de 95% para $r$, CCC, MAE, RMSE, viés e inclinação OLS foram derivados por reamostragem bootstrap ao nível de animal ($B = 5.000$ reamostragens com reposição; semente 42).

#### 1.10.2. Diferença Perceptual de Cor (CIE 1976 $\Delta E^*_{ab}$)
Calculou-se a distância euclidiana tridimensional no espaço CIELAB:

$$\Delta E^*_{ab} = \sqrt{(L^*_{\text{app}} - L^*_{\text{ref}})^2 + (a^*_{\text{app}} - a^*_{\text{ref}})^2 + (b^*_{\text{app}} - b^*_{\text{ref}})^2}$$

Classificada segundo os limiares metrológicos internacionais da CIE:
- $\Delta E^*_{ab} < 1{,}0$: Diferença imperceptível ao olho humano;
- $1{,}0 \le \Delta E^*_{ab} \le 3{,}0$: Diferença detectável apenas por especialistas; padrão aceito de equivalência laboratorial e instrumental;
- $3{,}0 < \Delta E^*_{ab} \le 5{,}0$: Tolerância aceitável em colorimetria industrial;
- $\Delta E^*_{ab} > 5{,}0$: Disparidade cromática evidente.

#### 1.10.3. Análise de Bland--Altman para Medidas Repetidas e Viés Proporcional
Para dados longitudinais, a variância das diferenças ($d_{ij} = y_{\text{app},ij} - y_{\text{ref},ij}$) foi particionada em componente entre-animais ($\sigma^2_u$) e intra-animal ($\sigma^2_e$) via modelo linear misto nulo:

$$d_{ij} = \bar{d} + u_i + \varepsilon_{ij}, \quad u_i \sim \mathcal{N}(0, \sigma_u^2), \quad \varepsilon_{ij} \sim \mathcal{N}(0, \sigma_e^2)$$

Os Limites de Concordância de 95% para medidas repetidas foram estabelecidos como:

$$\text{LoA}_{95\%} = \bar{d} \pm 1{,}96 \sqrt{\hat{\sigma}_u^2 + \hat{\sigma}_e^2}$$

O viés proporcional foi investigado por regressões lineares de mínimos quadrados ($y_{\text{app}} = \alpha + \beta y_{\text{ref}}$), com testes formais para $\beta \neq 1{,}0$ e $\alpha \neq 0$.

#### 1.10.4. Estabilidade da Concordância: Fatores Biométricos do Animal e Condições Climáticas
Investigou-se a estabilidade metrológica através de correlações de Pearson ($r$) e Spearman ($\rho$) entre os erros e dois grupos de variáveis dinâmicas:
1. **Fatores Biométricos e Fisiológicos do Animal:** Idade cronológica ($11{,}9--24{,}1\text{ meses}$), Peso vivo ($217{,}7--549{,}4\text{ kg}$) e Ganho Médio Diário ($0{,}39--1{,}93\text{ kg/dia}$);
2. **Variáveis Microclimáticas Ambientais:** Temperatura do ar ($^\circ\text{C}$), Umidade Relativa (\%RH), Carga Térmica de Radiação (CTR, $\text{W/m}^2$), Temperatura Média Radiante (TMR, $\text{K}$) e Índice de Temperatura do Globo e Umidade (ITGU).

#### 1.10.5. Modelagem Linear Mista Longitudinal (LMM)
A dependência longitudinal sazonal foi modelada via Modelos Lineares Mistos ajustados por Máxima Verossimilhança Restrita (REML):

$$z_{ij} = \beta_0 + \beta_1 \cdot \text{Fev}_{ij} + \beta_2 \cdot \text{Jul}_{ij} + u_i + \varepsilon_{ij}$$

onde a variável resposta $z_{ij}$ foi (a) o **erro com sinal (viés)** dos seis canais de cor e (b) $\log \Delta E^*_{ab}$ para pele e pelame (transformação logarítmica que normalizou os resíduos do modelo, contornando a violação severa de normalidade observada em $\Delta E$ bruto).

O efeito global do período sazonal foi avaliado pelo Teste de Razão de Verossimilhança (LRT) contra modelos reduzidos sem período ajustados por ML, com controle de taxa de erro familiar via método de Holm. Foram derivados o Coeficiente de Correlação Intraclasse (ICC), coeficientes fixos, erros-padrão e diagnósticos de normalidade residual (Shapiro-Wilk, assimetria e curtose).

---

# PART III: STATISTICAL BENCHMARKING TABLES

### Table S1. Architectural Ablation Study: Grid Resolution vs. Machine Learning Algorithm

| Algorithm | Grid Resolution | Instances (Train / Test) | MAE $L^*$ | MAE $a^*$ | MAE $b^*$ | $\Delta E^*_{ab}$ | $R^2$ |
|---|---|---|---|---|---|---|---|
| Random Forest | 1 (1 $\times$ 1) | 208 / 56 | 2.369 | 0.558 | 0.816 | **2.778** | 0.838 |
| Random Forest | 9 (3 $\times$ 3) | 1872 / 504 | 2.472 | 0.625 | 0.907 | **2.923** | 0.791 |
| Random Forest | 16 (4 $\times$ 4) | 3328 / 896 | 2.485 | 0.626 | 0.908 | **2.944** | 0.800 |
| Extra Trees | 16 (4 $\times$ 4) | 3328 / 896 | 2.506 | 0.637 | 0.915 | **2.980** | 0.787 |
| Extra Trees | 4 (2 $\times$ 2) | 832 / 224 | 2.544 | 0.628 | 0.881 | **2.997** | 0.797 |
| Extra Trees | 9 (3 $\times$ 3) | 1872 / 504 | 2.539 | 0.632 | 0.903 | **3.002** | 0.782 |
| Extra Trees | 1 (1 $\times$ 1) | 208 / 56 | 2.610 | 0.565 | 0.856 | **3.030** | 0.821 |
| Random Forest | 4 (2 $\times$ 2) | 832 / 224 | 2.618 | 0.616 | 0.874 | **3.054** | 0.799 |
| Gradient Boosting | 16 (4 $\times$ 4) | 3328 / 896 | 2.949 | 0.709 | 1.034 | **3.512** | 0.721 |
| Gradient Boosting | 9 (3 $\times$ 3) | 1872 / 504 | 3.111 | 0.726 | 1.139 | **3.742** | 0.695 |
| Gradient Boosting | 1 (1 $\times$ 1) | 208 / 56 | 3.343 | 0.675 | 0.980 | **3.816** | 0.764 |
| Gradient Boosting | 4 (2 $\times$ 2) | 832 / 224 | 3.956 | 0.722 | 1.074 | **4.538** | 0.691 |

### Table S2. Metrological Agreement and Cluster Bootstrap 95% Confidence Intervals (Field Dataset)

| Tissue & Coordinate | n | Pearson $r$ [95% CI] | Lin CCC [95% CI] | MAE [95% CI] | RMSE [95% CI] | Mean Bias [95% CI] | LoA 95% (Repeated Measures) | OLS Slope $\beta$ [95% CI] |
|---|---|---|---|---|---|---|---|---|
| L* (skin) | 132 | 0.652 [0.473, 0.768] | 0.588 [0.413, 0.711] | 1.307 [1.130, 1.496] | 1.684 [1.448, 1.932] | 0.039 [-0.321, 0.388] | [-3.34, 3.35] | 0.410 [0.278, 0.538] |
| a* (skin) | 132 | 0.839 [0.758, 0.902] | 0.793 [0.689, 0.868] | 0.842 [0.672, 1.038] | 1.237 [0.922, 1.582] | -0.016 [-0.198, 0.163] | [-2.45, 2.42] | 0.598 [0.487, 0.703] |
| b* (skin) | 132 | 0.892 [0.754, 0.946] | 0.849 [0.708, 0.901] | 0.603 [0.513, 0.705] | 0.809 [0.661, 0.958] | -0.008 [-0.182, 0.163] | [-1.61, 1.58] | 0.649 [0.527, 0.709] |
| L* (hair coat) | 131 | 0.582 [0.428, 0.716] | 0.548 [0.403, 0.663] | 2.882 [2.413, 3.377] | 4.054 [3.289, 4.785] | -0.041 [-0.868, 0.784] | [-8.00, 7.99] | 0.410 [0.312, 0.522] |
| a* (hair coat) | 131 | 0.875 [0.828, 0.916] | 0.862 [0.810, 0.907] | 0.820 [0.680, 0.971] | 1.133 [0.927, 1.336] | 0.018 [-0.164, 0.199] | [-2.21, 2.25] | 0.738 [0.662, 0.817] |
| b* (hair coat) | 131 | 0.818 [0.757, 0.865] | 0.785 [0.721, 0.834] | 1.013 [0.875, 1.169] | 1.320 [1.125, 1.528] | 0.030 [-0.213, 0.276] | [-2.57, 2.63] | 0.613 [0.543, 0.686] |

### Table S3. Global Color Difference ($\Delta E^*_{ab}$) and Equivalence Thresholds by Season

| Tissue Target | Seasonal Period | n | Mean $\pm$ SD | Median [Q1--Q3] | 95th Percentile | % $< 1.0$ (Imperceptible) | % $< 3.0$ (Lab Equivalent) | % $< 5.0$ (Industry Match) |
|---|---|---|---|---|---|---|---|---|
| Skin | All Campaigns | 132 | 1.87 $\pm$ 1.23 | 1.57 [1.10--2.34] | 4.12 | 22.7\% | **85.6\%** | 97.0\% |
| Skin | December (Summer) | 46 | 1.73 $\pm$ 1.13 | 1.45 [0.88--2.47] | 3.63 | 32.6\% | **87.0\%** | 100.0\% |
| Skin | February (Late-Summer) | 46 | 1.99 $\pm$ 1.44 | 1.57 [1.17--2.45] | 5.00 | 21.7\% | **80.4\%** | 93.5\% |
| Skin | July (Winter) | 40 | 1.91 $\pm$ 1.08 | 1.67 [1.38--2.16] | 3.63 | 12.5\% | **90.0\%** | 97.5\% |
| Hair Coat | All Campaigns | 131 | 3.47 $\pm$ 2.74 | 2.76 [1.85--4.29] | 9.54 | 9.9\% | **59.5\%** | 83.2\% |
| Hair Coat | December (Summer) | 46 | 2.86 $\pm$ 1.75 | 2.36 [1.60--3.92] | 6.36 | 15.2\% | **69.6\%** | 84.8\% |
| Hair Coat | February (Late-Summer) | 45 | 3.28 $\pm$ 2.53 | 2.78 [2.02--3.75] | 6.62 | 4.4\% | **62.2\%** | 88.9\% |
| Hair Coat | July (Winter) | 40 | 4.38 $\pm$ 3.59 | 3.47 [2.22--5.15] | 11.95 | 10.0\% | **45.0\%** | 75.0\% |

### Table S4. Stability of Computational Agreement Across Animal Growth and Biometric Factors

| Animal Biometric Factor | Prediction Error Metric | Pearson $r$ | $p$-value ($r$) | Spearman $\rho$ | $p$-value ($\rho$) | Clinical Interpretation |
|---|---|---|---|---|---|---|
| Idade (meses) | DeltaE_pele | -0.030 | 0.734 | 0.020 | 0.821 | Stable (No significant correlation) |
| Idade (meses) | DeltaE_pelo | 0.189 | 0.031 | 0.111 | 0.208 | Weak/moderate biological seasonal effect |
| Idade (meses) | erro_abs_L_pele | -0.205 | 0.018 | -0.191 | 0.028 | Weak/moderate biological seasonal effect |
| Idade (meses) | erro_abs_a_pele | 0.102 | 0.245 | 0.076 | 0.385 | Stable (No significant correlation) |
| Idade (meses) | erro_abs_b_pele | 0.135 | 0.122 | 0.167 | 0.056 | Stable (No significant correlation) |
| Idade (meses) | erro_abs_L_pelo | 0.176 | 0.044 | 0.095 | 0.281 | Weak/moderate biological seasonal effect |
| Idade (meses) | erro_abs_a_pelo | 0.069 | 0.433 | -0.053 | 0.547 | Stable (No significant correlation) |
| Idade (meses) | erro_abs_b_pelo | 0.084 | 0.342 | 0.069 | 0.437 | Stable (No significant correlation) |
| Peso médio (kg) | DeltaE_pele | -0.080 | 0.365 | 0.016 | 0.855 | Stable (No significant correlation) |
| Peso médio (kg) | DeltaE_pelo | 0.231 | 0.008 | 0.143 | 0.103 | Weak/moderate biological seasonal effect |
| Peso médio (kg) | erro_abs_L_pele | -0.214 | 0.014 | -0.170 | 0.052 | Weak/moderate biological seasonal effect |
| Peso médio (kg) | erro_abs_a_pele | 0.041 | 0.641 | 0.037 | 0.673 | Stable (No significant correlation) |
| Peso médio (kg) | erro_abs_b_pele | 0.113 | 0.198 | 0.165 | 0.059 | Stable (No significant correlation) |
| Peso médio (kg) | erro_abs_L_pelo | 0.220 | 0.011 | 0.114 | 0.197 | Weak/moderate biological seasonal effect |
| Peso médio (kg) | erro_abs_a_pelo | 0.042 | 0.632 | -0.049 | 0.582 | Stable (No significant correlation) |
| Peso médio (kg) | erro_abs_b_pelo | 0.078 | 0.375 | 0.106 | 0.226 | Stable (No significant correlation) |
| GMD inclinação | DeltaE_pele | -0.052 | 0.557 | 0.035 | 0.689 | Stable (No significant correlation) |
| GMD inclinação | DeltaE_pelo | 0.176 | 0.045 | 0.114 | 0.197 | Weak/moderate biological seasonal effect |
| GMD inclinação | erro_abs_L_pele | -0.165 | 0.059 | -0.137 | 0.118 | Stable (No significant correlation) |
| GMD inclinação | erro_abs_a_pele | 0.026 | 0.771 | 0.059 | 0.499 | Stable (No significant correlation) |
| GMD inclinação | erro_abs_b_pele | 0.155 | 0.075 | 0.194 | 0.026 | Stable (No significant correlation) |
| GMD inclinação | erro_abs_L_pelo | 0.178 | 0.042 | 0.109 | 0.215 | Weak/moderate biological seasonal effect |
| GMD inclinação | erro_abs_a_pelo | 0.008 | 0.930 | -0.126 | 0.152 | Stable (No significant correlation) |
| GMD inclinação | erro_abs_b_pelo | 0.001 | 0.988 | 0.032 | 0.716 | Stable (No significant correlation) |

### Table S5. Omnibus Seasonal Period Effect: Likelihood Ratio Test in Linear Mixed Models

| Response Variable | Number of Observations | Number of Unique Animals | LRT $\chi^2$ (2 d.f.) | Raw $p$-value | Holm-Adjusted $p$-value | Significance |
|---|---|---|---|---|---|---|
| Viés (erro com sinal) L_pele | 132 | 46 | 4.368 | 0.113 | 0.338 | Stable / Invariant |
| Viés (erro com sinal) a_pele | 132 | 46 | 30.562 | < 0.001 | < 0.001 | Significant ($p < 0.05$) |
| Viés (erro com sinal) b_pele | 132 | 46 | 26.643 | < 0.001 | < 0.001 | Significant ($p < 0.05$) |
| Viés (erro com sinal) L_pelo | 131 | 46 | 8.226 | 0.016 | 0.065 | Stable / Invariant |
| Viés (erro com sinal) a_pelo | 131 | 46 | 37.401 | < 0.001 | < 0.001 | Significant ($p < 0.05$) |
| Viés (erro com sinal) b_pelo | 131 | 46 | 13.518 | 0.001 | 0.006 | Significant ($p < 0.05$) |
| log ΔE pele | 132 | 46 | 2.882 | 0.237 | 0.338 | Stable / Invariant |
| log ΔE pelo | 131 | 46 | 4.197 | 0.123 | 0.338 | Stable / Invariant |

### Table S6. Linear Mixed-Effects Model Fixed Estimates and Intraclass Correlation (ICC)

| Response Variable | Fixed Parameter Term | Estimate | Standard Error | 95% Confidence Interval | $p$-value | Holm $p$-value | Intraclass Correlation (ICC) |
|---|---|---|---|---|---|---|---|
| Viés (erro com sinal) L_pele | Intercept | 0.343 | 0.251 | [-0.149, 0.834] | 0.172 | -- | 0.360 |
| Viés (erro com sinal) L_pele | Período[T.Fevereiro] | -0.515 | 0.285 | [-1.073, 0.043] | 0.071 | 0.566 | 0.360 |
| Viés (erro com sinal) L_pele | Período[T.Julho] | -0.537 | 0.298 | [-1.120, 0.046] | 0.071 | 0.566 | 0.360 |
| Viés (erro com sinal) a_pele | Intercept | 0.551 | 0.164 | [0.229, 0.873] | < 0.001 | -- | 0.000 |
| Viés (erro com sinal) a_pele | Período[T.Fevereiro] | -0.432 | 0.232 | [-0.888, 0.023] | 0.063 | 0.566 | 0.000 |
| Viés (erro com sinal) a_pele | Período[T.Julho] | -1.375 | 0.241 | [-1.847, -0.903] | < 0.001 | < 0.001 | 0.000 |
| Viés (erro com sinal) b_pele | Intercept | -0.035 | 0.112 | [-0.255, 0.184] | 0.752 | -- | 0.363 |
| Viés (erro com sinal) b_pele | Período[T.Fevereiro] | -0.303 | 0.127 | [-0.552, -0.054] | 0.017 | 0.186 | 0.363 |
| Viés (erro com sinal) b_pele | Período[T.Julho] | 0.424 | 0.133 | [0.164, 0.683] | 0.001 | 0.017 | 0.363 |
| Viés (erro com sinal) L_pelo | Intercept | 0.162 | 0.588 | [-0.991, 1.314] | 0.783 | -- | 0.248 |
| Viés (erro com sinal) L_pelo | Período[T.Fevereiro] | -1.272 | 0.729 | [-2.700, 0.157] | 0.081 | 0.566 | 0.248 |
| Viés (erro com sinal) L_pelo | Período[T.Julho] | 0.896 | 0.753 | [-0.580, 2.371] | 0.234 | 0.937 | 0.248 |
| Viés (erro com sinal) a_pelo | Intercept | 0.725 | 0.147 | [0.437, 1.013] | < 0.001 | -- | 0.096 |
| Viés (erro com sinal) a_pelo | Período[T.Fevereiro] | -0.860 | 0.199 | [-1.250, -0.469] | < 0.001 | < 0.001 | 0.096 |
| Viés (erro com sinal) a_pelo | Período[T.Julho] | -1.354 | 0.206 | [-1.758, -0.951] | < 0.001 | < 0.001 | 0.096 |
| Viés (erro com sinal) b_pelo | Intercept | -0.341 | 0.188 | [-0.709, 0.028] | 0.070 | -- | 0.147 |
| Viés (erro com sinal) b_pelo | Período[T.Fevereiro] | 0.249 | 0.247 | [-0.236, 0.734] | 0.314 | 0.942 | 0.147 |
| Viés (erro com sinal) b_pelo | Período[T.Julho] | 0.943 | 0.256 | [0.441, 1.444] | < 0.001 | 0.003 | 0.147 |
| log ΔE pele | Intercept | 0.324 | 0.097 | [0.134, 0.513] | < 0.001 | -- | 0.155 |
| log ΔE pele | Período[T.Fevereiro] | 0.122 | 0.126 | [-0.124, 0.369] | 0.330 | 0.942 | 0.155 |
| log ΔE pele | Período[T.Julho] | 0.221 | 0.131 | [-0.036, 0.478] | 0.091 | 0.566 | 0.155 |
| log ΔE pelo | Intercept | 0.864 | 0.103 | [0.662, 1.066] | < 0.001 | -- | 0.060 |
| log ΔE pelo | Período[T.Fevereiro] | 0.120 | 0.142 | [-0.159, 0.399] | 0.400 | 0.942 | 0.060 |
| log ΔE pelo | Período[T.Julho] | 0.300 | 0.147 | [0.012, 0.588] | 0.041 | 0.413 | 0.060 |
