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

### 1.4. In-Field Optical Isolation Chamber and Hardware-Level Image Acquisition
Ambient outdoor illumination in tropical open-air cattle yards exhibits stochastic, high-amplitude fluctuations (direct solar irradiance $> 100,000\text{ lux}$, transient cloud attenuation, casting shadows from handling chutes, and shifting correlated color temperatures ranging from $4,000\text{ K}$ to $> 15,000\text{ K}$). Under such unconstrained optical conditions, passive photographic colorimetry inevitably suffers from metrological instability. To establish a standardized, repeatable optical measurement environment directly inside commercial handling chutes, a custom-engineered, portable light-tight isolation chamber was fabricated:
- **Cylindrical Structural Barrel:** Fabricated from high-rigidity polyvinyl chloride (PVC) with an axial length of $20\text{ cm}$ and an internal bore diameter of $10\text{ cm}$. The geometric length was optically engineered to position the mobile camera lens precisely at its focal plane while preventing peripheral optical flare;
- **Anti-Reflective Internal Coating:** The inner circumferential barrel walls were coated with ultra-matte, non-reflective optical black paint exhibiting a specular reflectance factor of $< 1.5\%$ across the entire visible spectrum ($380--750\text{ nm}$), eliminating internal stray light and multi-path scatter reflections;
- **Anatomical Conformable Neoprene Seal:** The distal end contacting the animal was fitted with a flexible closed-cell cellular neoprene gasket. Under gentle manual compression against the bovine flank, this gasket conforms dynamically to the convex curvature of the lateral ribcage and vertebral margin, establishing an impervious seal against daylight infiltration;
- **Precision Mechanical Smartphone Mount:** The proximal end incorporated a high-density thermoplastic mechanical adapter that rigidly and coaxially aligns the smartphone primary camera lens and its integrated onboard light-emitting diode (LED) flash unit directly over the central axis of the cylinder.

#### Hardware Abstraction and Deterministic Camera2 API Sensor Locking
Standard smartphone photography relies on proprietary, non-linear Image Signal Processor (ISP) firmware routines—collectively known as "3A" algorithms (Auto-Exposure, Auto-Focus, and Auto-White Balance). These algorithms dynamically manipulate sensor analog gain, exposure times, non-linear gamma curves, and digital color channel gains ($R_{\text{gain}}, G_{\text{gain}}, B_{\text{gain}}$) based on heuristic scene luminance, which irrevocably alters biological color coordinates.

To guarantee rigorous metrological repeatability, digital image capture was decoupled from automated ISP processing by interfacing directly with the Android Camera Hardware Abstraction Layer (HAL) via the native `android.hardware.camera2` API. A deterministic capture profile was enforced at the hardware level:
1. **Auto-Exposure Lock (`CONTROL_AE_MODE_OFF`):** Automatic exposure calculation was completely disabled. The electronic shutter integration time (`SENSOR_EXPOSURE_TIME`) was locked to $8{,}000{,}000\text{ ns}$ ($1/125\text{ s}$). This shutter speed is sufficiently rapid to freeze involuntary animal respiration or micro-tremors within the crush, while preventing charge well saturation in the CMOS sensor under close-range flash illumination;
2. **Sensor Analog Gain Lock (`SENSOR_SENSITIVITY`):** Sensor sensitivity was locked to baseline ISO 100, minimizing thermal Johnson–Nyquist noise and CMOS read noise, thereby maximizing the effective Signal-to-Noise Ratio (SNR);
3. **Manual Focus Lock (`CONTROL_AF_MODE_OFF`):** Lens focal distance was locked to fixed hyperfocal focus calibrated specifically to the $20\text{ cm}$ distance of the PVC chamber target plane, eliminating focus hunting;
4. **Auto-White Balance Override (`CONTROL_AWB_MODE_OFF`):** ISP automatic chromatic adaptation was disabled. Sensor channel gains were locked to neutral unity ($R = 1.0, G = 1.0, B = 1.0$) and color transform matrices were frozen, ensuring linear radiant flux capture;
5. **Synchronous Flash Driver:** Illumination was provided exclusively by the synchronized onboard LED flash unit firing inside the sealed optical chamber (`FLASH_MODE_SINGLE` / `CONTROL_CAPTURE_INTENT_STILL_CAPTURE`).

High-throughput image capture was achieved using an uncompressed `ImageReader` buffer allocated for native sensor resolution ($4000 \times 3000$ pixels; 12 megapixels) in `ImageFormat.YUV_420_888`, passing raw planar byte buffers directly to native memory handles via the Java Native Interface (JNI) to bypass Java Virtual Machine (JVM) garbage collection pauses.

### 1.5. Computer Vision Pipeline, Multi-Stage Segmentation, and Adaptive ROI Localization
The raw digital frames acquired inside the optical chamber were processed through an automated, low-level computer vision pipeline implemented in C++ and Python using the OpenCV library.

#### 1.5.1. Chromatic Correction via Gray World Algorithm
Although ambient sunlight was eliminated by the sealed neoprene gasket, commercial smartphone white LED flash units exhibit an intrinsically non-uniform spectral power distribution (SPD) characterized by high correlated color temperatures (CCT $\approx 5,500--6,500\text{ K}$) and a sharp phosphor emission spike in the blue spectrum ($\approx 450\text{ nm}$). To normalize this localized chromatic bias, the Gray World color constancy algorithm was implemented under the physical postulate that the spatial average of surface reflectance across a complex biological scene is achromatic (neutral gray):

$$\bar{R} = \frac{1}{|\Omega|} \sum_{p \in \Omega} R(p), \quad \bar{G} = \frac{1}{|\Omega|} \sum_{p \in \Omega} G(p), \quad \bar{B} = \frac{1}{|\Omega|} \sum_{p \in \Omega} B(p)$$

$$\mu_{\text{gray}} = \frac{\bar{R} + \bar{G} + \bar{B}}{3}$$

$$\alpha_R = \frac{\mu_{\text{gray}}}{\bar{R}}, \quad \alpha_G = \frac{\mu_{\text{gray}}}{\bar{G}}, \quad \alpha_B = \frac{\mu_{\text{gray}}}{\bar{B}}$$

Each pixel coordinate $p$ within the biological target domain $\Omega$ was dynamically rescaled as:

$$I_{\text{balanced}}(p) = \begin{bmatrix} \alpha_R \cdot R(p) \\ \alpha_G \cdot G(p) \\ \alpha_B \cdot B(p) \end{bmatrix}$$

normalizing chromatic shifts before feature extraction.

#### 1.5.2. Tri-Stage Cascading Circular Aperture Segmentation
To automatically isolate the biological tissue target within the circular opening of the PVC chamber and eliminate the surrounding chamber walls, a robust, three-stage cascading segmentation algorithm (`_detectar_circulo_abertura`) was developed:
1. **Cascade Level 1 (Dynamic Otsu with Morphological Circularity Validation):** The frame was converted to 8-bit grayscale and filtered with an isotropic Gaussian spatial smoothing kernel ($25 \times 25$ pixels, $\sigma = 0$) to attenuate high-frequency cutaneous hair textures. An adaptive global threshold $\tau_{\text{thresh}}$ was computed from the Otsu threshold $\tau_{\text{Otsu}}$:
   $$\tau_{\text{thresh}} = \max(0.65 \cdot \tau_{\text{Otsu}}, 30)$$
   Morphological closing followed by opening using an elliptical structuring element ($31 \times 31$ pixels) bridged specular flash reflections and sealed contour boundaries. External topological contours were extracted using the Suzuki–Abe algorithm (`cv2.findContours`, `RETR_EXTERNAL`). The maximum candidate contour $\mathcal{C}_{\text{max}}$ was fitted with its minimum enclosing circle $(\mathbf{c}, r_{\text{enc}})$. A shape circularity metric $\Psi$ was evaluated:
   $$\Psi = \frac{\text{Area}(\mathcal{C}_{\text{max}})}{\pi \cdot r_{\text{enc}}^2}$$
   If $\text{Area}(\mathcal{C}_{\text{max}}) > 0.05 \cdot (H \cdot W)$ and $\Psi \ge 0.72$, the candidate was accepted as the true circular aperture;
2. **Cascade Level 2 (Hough Gradient Transform):** In specimens where dark hair or irregular shadows fractured the continuous outer contour, causing $\Psi < 0.72$, the algorithm seamlessly cascaded to a 2D Hough Circles transform (`cv2.HoughCircles` with `cv2.HOUGH_GRADIENT`). Operating with an accumulator resolution factor $dp = 1.5$, gradient threshold $50$, accumulator threshold $40$, and radius bounds constrained between $0.18 \cdot \min(H, W)$ and $0.55 \cdot \min(H, W)$, the circle minimizing the Euclidean distance to the optical sensor center $(W/2, H/2)$ was selected;
3. **Cascade Level 3 (Conservative Geometric Fallback):** If both analytical detectors failed due to severe optical artifacts, a conservative geometric fallback was invoked, centering the aperture at $(W/2, H/2)$ with a conservative radius $r = 0.40 \cdot \min(H, W)$;
4. **Internal Radial Margin Erosion:** To prevent boundary artifacts caused by specular edge reflections on the inner chamfer of the PVC cylinder, an inward radial erosion margin of $2\%$ (`margin_pct = 0.02`) was enforced:
   $$r_{\text{eff}} = \lfloor r \cdot (1 - 0.02) \rfloor$$
   Pixels outside this effective radius were masked to neutral white background ($255, 255, 255$) or isolated into a tight centered bounding box.

#### 1.5.3. Adaptive Biological Tissue Discrimination and ROI Localization
In operational field deployment, the camera views two distinct anatomical surfaces: trichotomized epidermal skin (a localized, darker shaved patch surrounded by residual hair) and intact hair coat (a continuous, uniform keratinous surface). To handle both scenarios without requiring manual user toggling, an automated discriminant routine (`detectar_mancha_pele`) was engineered:
1. **Luminance Percentile Profiling:** The pixel luminance distribution within the segmented circular aperture was statistically profiled by computing the 5th percentile ($p_5$), 25th percentile ($p_{25}$), median ($p_{50}$), and standard deviation ($\sigma$);
2. **Discriminant Decision Logic:**
   $$\text{Surface Type} = \begin{cases} \text{Epidermal Skin Patch}, & \text{if } p_5 < 60 \text{ and } \sigma > 30 \\ \text{Intact Hair Coat}, & \text{otherwise} \end{cases}$$
   When classified as an intact hair coat, the biological specimen is intrinsically homogeneous; hence, the entire circular aperture is extracted with a $5\%$ edge padding;
3. **Skin Patch Isolation and Tag Occlusion Masking:**
   - *Ear-Tag Occlusion Mask:* Cattle ear-tags or temporary adhesive numbering tape placed near the dorsal line often protrude into the upper field of view. An upper exclusion boundary (`label_cutoff = y_{\text{top}} + 0.22 \cdot H_{\text{aperture}}`) automatically masked the upper $22\%$ of the circular aperture;
   - *Adaptive Thresholding:* On the remaining lower region, an adaptive threshold $\tau_{\text{patch}} = \min(p_{50} - 10, 105)$ was applied to a Gaussian-smoothed image ($151 \times 151$ kernel);
   - *Morphological Dilation/Closing:* Morphological filtering with a square structuring element ($61 \times 61$) merged cutaneous micro-textures and follicle pores into a unified biological patch;
   - *Bounding Box Extraction:* The largest contour covering $\ge 10\%$ and $\le 60\%$ of the aperture area was isolated, and its bounding box $[X, Y, W, H]$ was expanded with a $5\%$ safety margin padding (`percentual_borda = 0.05`) to generate the final analytical Region of Interest (ROI).

### 1.6. Multichannel Photometric Feature Engineering on Spatial $3 \times 3$ Grid (14 Descriptors)
Because coaxial flash illumination within a closed cylinder creates an inherent radial luminance decay (perpendicular specular irradiance at the center, transitioning to diffuse oblique backscatter near peripheral margins), computing a single global average collapses critical spatial variance and dilutes bio-optical information.

To preserve spatial irradiance dynamics, the segmented biological ROI was discretized into a regular **$3 \times 3$ spatial grid (9 independent sub-blocks)**:
- 1 central core block capturing direct incident specular reflectance;
- 8 peripheral blocks capturing diffuse, volumetric tissue backscattering.

From each spatial block $g \in \{1, \dots, 9\}$, a 14-dimensional photometric feature vector $\mathbf{x}_g \in \mathbb{R}^{14}$ was extracted across three complementary color spaces and non-linear bio-optical indices:
- **Direct Multi-Space Photometric Channels (9 features):**
  - RGB Color Space: Mean Red ($\bar{R}$), Green ($\bar{G}$), and Blue ($\bar{B}$) pixel intensities ($0--255$);
  - HSV Color Space: Mean Hue ($\bar{H}$, representing dominant wavelength), Saturation ($\bar{S}$, representing chromatic purity), and Value ($\bar{V}$, representing achromatic intensity);
  - Scaled OpenCV CIELAB Space: Mean Lightness ($\bar{L}_{\text{cv2}}$), Green–Red chromaticity ($\bar{a}_{\text{cv2}}$), and Blue–Yellow chromaticity ($\bar{b}_{\text{cv2}}$);
- **Non-Linear Bio-Optical Ratios and Invariant Descriptors (5 features):**
  - $\text{Razao}_{\text{RG}} = \frac{\bar{R}}{\bar{G} + \epsilon}$ ($\epsilon = 10^{-5}$): Erythema and microvascular perfusion index, sensitive to dermal capillary hemoglobin content;
  - $\text{Razao}_{\text{RB}} = \frac{\bar{R}}{\bar{B} + \epsilon}$: Cutaneous pigmentation index, sensitive to the spectral absorption ratio between dark eumelanin and reddish pheomelanin;
  - $\text{Razao}_{\text{GB}} = \frac{\bar{G}}{\bar{B} + \epsilon}$: Structural cuticular scattering index, sensitive to keratin fiber density and medullary air cavity scattering in hair fibers;
  - $\text{Dif}_{LV} = \bar{L}_{\text{cv2}} - \bar{V}$: Decoupling metric between non-linear psychometric lightness and linear photonic intensity, effectively neutralizing residual flash glare and micro-shadows;
  - $\text{Soma}_{\text{RGB}} = \bar{R} + \bar{G} + \bar{B}$: Integrated photonic energy proxy, measuring gross backscattered photon flux from the biological target.

Concatenating features across the 9 spatial cells yielded a rich, spatially resolved feature representation capturing both central specular highlights and peripheral diffuse reflectance.

### 1.7. Machine Learning Modeling, Dual-Specialist Architecture, and Ablation Study
Bovine epidermal skin (turbid, multi-layered living tissue with dermal micro-vascularity, melanin granule clusters, and high volume scattering) and intact hair coat (semi-translucent keratin cylinders with anisotropic surface reflection and air-filled medullary cores) possess fundamentally distinct Bidirectional Reflectance Distribution Functions (BRDF). Fitting a single unified regression model across both tissues forces conflicting mathematical optimization constraints, degrading accuracy.

To resolve this bio-optical disparity, a **dual-specialist machine learning architecture** was established:
1. **Skin-Specialist Regressor ($\mathcal{M}_{\text{skin}}$):** Optimized exclusively on trichotomized epidermal patches;
2. **Coat-Specialist Regressor ($\mathcal{M}_{\text{coat}}$):** Optimized exclusively on intact hair coat specimens.

#### Multi-Model Architectural and Spatial Ablation Study
To empirically identify the optimal combination of spatial grid discretization and supervised regression algorithm, a systematic **ablation study** was executed evaluating 12 distinct configurations (Table S1). Four grid resolutions ($1 \times 1$, $2 \times 2$, $3 \times 3$, and $4 \times 4$, producing 1, 4, 9, and 16 spatial instances per image) were systematically crossed with three machine learning model families:
- **Random Forest Regressor:** Bagging ensemble of $B = 200$ randomized decision trees with maximum tree depth constrained to $\text{max\_depth} = 15$ and multi-output regression;
- **Extra Trees Regressor:** Extremely randomized tree ensemble ($B = 200$ trees) where split cut-points are chosen completely at random;
- **Gradient Boosting Regressor:** Sequential boosting ensemble ($B = 200$ estimators, learning rate $\eta = 0.05$, tree depth 15) wrapped in a `MultiOutputRegressor`.

As detailed in Table S1, the **Random Forest with a $3 \times 3$ grid (9 cells)** achieved the superior balance of metrological precision and generalization ($\Delta E^*_{ab} = 2.923$, $R^2 = 0.791$, $\text{MAE}_{L^*} = 2.472$, $\text{MAE}_{a^*} = 0.625$, $\text{MAE}_{b^*} = 0.907$). Single global crops ($1 \times 1$) lacked spatial discrimination ($\Delta E^*_{ab} > 3.03$), while Gradient Boosting exhibited overfitting to localized flash specularities ($\Delta E^*_{ab} = 3.742$).

### 1.8. Validation Protocol: Group-Level Subject Isolation (`GroupShuffleSplit`)
To ensure genuine generalization and prevent data leakage and pseudoreplication, standard random cross-validation (`train_test_split`) was strictly avoided. Because individual cattle possess unique cutaneous melanin distributions, follicle density, and coat textures, distributing spatial sub-cells or repeated photographic observations of the same animal across both training and test sets would cause models to memorize individual animal signatures rather than learning universal bio-optical color mappings.

Validation was enforced using `GroupShuffleSplit` structured strictly on unique biological subject identifiers ($\text{Group} = \text{Animal ID}$):
- **Training Cohort (80% of subjects):** 37 unique animals (1,872 spatial sub-grid instances for grid 9);
- **Independent Test Cohort (20% of subjects):** 10 completely unseen animals (504 spatial sub-grid instances for grid 9).

No image, grid block, or physical measurement from any animal in the training partition ever entered the test set, guaranteeing that reported benchmarks reflect true field performance on novel subjects.

### 1.9. Commercial Edge-AI Android Mobile Application Architecture and Software Engineering
To transition this technology from research scripts to commercial chute-side deployment, the complete computational vision pipeline and dual-specialist Random Forest models were engineered into an autonomous, native Android mobile application:

#### 1.9.1. Software Stack and Layered Architecture
- **Application Core:** Developed in Kotlin using Google's modern Android Jetpack architecture (Jetpack Compose for reactive UI, ViewModel for state management, and Kotlin Coroutines for asynchronous concurrency);
- **Native Processing Bridge (JNI / C++):** Heavyweight image processing and matrix transformations were implemented in native C++ using the OpenCV Android SDK (v4.8.0), connected via the Java Native Interface (JNI). Raw memory buffers from the Camera2 API were passed directly as native C++ pointers, eliminating JVM memory allocations and garbage collection pauses;
- **Edge Inference Engine:** High-performance model evaluation was executed using the Microsoft ONNX Runtime Mobile C++ API (v1.16).

#### 1.9.2. Model Quantization, Graph Optimization, and Memory Footprint
- **ONNX Graph Serialization:** Trained scikit-learn Random Forest ensembles were converted to Open Neural Network Exchange (ONNX) computation graphs using `skl2onnx` targeting Opset 15;
- **Dynamic Float Quantization:** Weight arrays were dynamically quantized, compressing the dual-specialist models from $> 35\text{ MB}$ down to a compact binary footprint of $< 8.5\text{ MB}$;
- **RAM and Cold-Start Optimization:** The quantized ONNX graph initializes into device RAM in $< 45\text{ ms}$, ensuring instant application responsiveness upon startup.

#### 1.9.3. Latency Budget Breakdown and Real-Time Execution
The end-to-end computational budget was benchmarked on an octa-core mobile processor (ARM Cortex-A78 @ 2.4 GHz + Cortex-A55 @ 2.0 GHz). The complete execution lifecycle required $< 140\text{ ms}$ total latency:
1. Camera sensor exposure and DMA frame transfer: $28\text{ ms}$;
2. JNI memory mapping, YUV-to-RGB planar conversion, and Gray World balancing: $18\text{ ms}$;
3. Cascading circular aperture segmentation and adaptive tissue discrimination: $24\text{ ms}$;
4. $3 \times 3$ grid discretization and 14-feature multi-space extraction: $35\text{ ms}$;
5. ONNX dual-specialist forward inference pass: $15\text{ ms}$;
6. Room/SQLite local persistence and UI diagnostic rendering: $10\text{ ms}$.

With a total processing time of $\approx 130\text{ ms}$, the system achieves an operational throughput of $> 7.5\text{ evaluations per second}$, significantly outperforming benchtop instruments which require manual mechanical positioning and several seconds per measurement cycle.

#### 1.9.4. Autonomous Offline Edge Computing, Thermal Stability, and Enterprise Integration
- **100% Offline Autonomy:** All computational vision, feature extraction, and machine learning inference execute natively on the smartphone CPU/NPU without requiring cellular reception, Wi-Fi, or cloud server communication. This complete edge autonomy is crucial for practical cattle chute operations in remote tropical grazing regions;
- **Battery and Thermal Performance:** In continuous chute trials, battery consumption remained below $2.8\%$ per 100 consecutive animal scans. Zero thermal throttling was recorded during continuous 3-hour field sessions under ambient temperatures exceeding $36\,^\circ\text{C}$;
- **ACID Local Persistence (Room / SQLite):** Every evaluation is recorded into an ACID-compliant local SQLite database managed by Android Jetpack Room. Stored schema attributes include timestamp, electronic RFID/visual ear-tag ID, tissue classification, predicted $L^*, a^*, b^*$ coordinates, calculated $\Delta E^*_{ab}$, RGB hex visual swatch, ambient microclimate metadata, and internal camera diagnostics;
- **Enterprise Livestock Interoperability:** Data can be exported at any time to standard CSV, JSON, and ISO/ICAR compatible livestock formats for seamless synchronization with herd management ERP systems (e.g., Sisbov, Embrapa Geneplus).

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

### 1.4. Câmara Portátil de Isolamento Óptico e Aquisição Determinística em Nível de Hardware
A iluminação solar externa em currais abertos de regiões tropicais exibe flutuações estocásticas de grande amplitude (irradiância solar direta $> 100.000\text{ lux}$, sombras transitórias de nuvens e de coberturas do brete, além de temperaturas de cor correlatas oscilando entre $4.000\text{ K}$ e $> 15.000\text{ K}$). Nessas condições ópticas descontroladas, a fotografia passiva convencional é inviabilizada para fins metrológicos. Para isolar o alvo biológico e estabelecer um ambiente óptico perfeitamente controlado e reprodutível no tronco de contenção, desenvolveu-se uma câmara cilíndrica portátil de isolamento óptico:
- **Corpo Cilíndrico:** Fabricado em policloreto de vinila (PVC) rígido com comprimento axial de $20\text{ cm}$ e diâmetro interno de $10\text{ cm}$, dimensionado geometricamente para manter o plano focal da lente do smartphone a uma distância estável, eliminando reflexos parasitas periféricos;
- **Revestimento Interno Antirreflexo:** Revestimento interno com tinta preta fosca óptica de ultra-baixa refletância (fator de reflexão especular $< 1{,}5\%$ em toda a faixa de $380--750\text{ nm}$), suprimindo espalhamentos secundários e reflexões de parede interna;
- **Vedação Anatômica em Neoprene Celular:** A extremidade distal em contato com o bovino recebeu anel conformável de borracha neoprene celular flexível. Sob leve compressão manual contra o flanco, o anel molda-se à curvatura costal e dorsal do animal, vedando hermeticamente a entrada de luz ambiente;
- **Suporte Mecânico de Precisão:** A base proximal recebeu adaptador usinado em termoplástico rígido de alta densidade que centraliza e alinha coaxialmente a lente da câmera principal do smartphone e o emissor LED de flash sobre o eixo central da câmara.

#### Abstração de Hardware e Travamento Determinístico via API Camera2 do Android
Em aplicativos fotográficos comerciais, o subsistema de processamento de imagem (ISP - *Image Signal Processor*) aplica algoritmos proprietários de "3A" (Auto-Exposição, Auto-Foco e Auto-Balanço de Branco). Esses algoritmos ajustam dinamicamente ganhos analógicos do sensor, tempos de exposição, curvas de tom não lineares e ganhos digitais de canais ($R_{\text{gain}}, G_{\text{gain}}, B_{\text{gain}}$), distorcendo irremediavelmente as coordenadas cromáticas biológicas.

Para assegurar estabilidade metrológica estrita, a captura digital foi desacoplada das automações do ISP mediante comunicação direta com a Camada de Abstração de Hardware (HAL) do Android através da API nativa `android.hardware.camera2`. Um perfil de captura determinístico foi imposto em hardware:
1. **Desativação de Auto-Exposição (`CONTROL_AE_MODE_OFF`):** O controle automático de exposição foi desativado. O tempo de integração do obturador eletrônico (`SENSOR_EXPOSURE_TIME`) foi travado em $8{,}000{,}000\text{ ns}$ ($1/125\text{ s}$), velocidade suficiente para congelar movimentos respiratórios ou tremores musculares do animal no tronco, sem provocar saturação de poço de potencial no sensor CMOS sob a luz próxima do flash;
2. **Travamento de Ganho Analógico (`SENSOR_SENSITIVITY`):** Sensibilidade analógica do sensor travada em ISO 100 básico, minimizando ruídos térmicos de Johnson–Nyquist e ruído de leitura do CMOS, maximizando a Razão Sinal-Ruído (SNR);
3. **Travamento de Foco Manual (`CONTROL_AF_MODE_OFF`):** Distância focal travada na hiperfocal calibrada para o plano do alvo a $20\text{ cm}$ no interior do cano de PVC, eliminando a busca oscilatória de foco (*focus hunting*);
4. **Desativação do Balanço de Branco Automático (`CONTROL_AWB_MODE_OFF`):** Desativou-se o algoritmo heurístico de adaptação cromática do ISP. Os ganhos de canais foram travados em matriz unitária neutra ($R = 1{,}0, G = 1{,}0, B = 1{,}0$) com matrizes de transformação de cor congeladas, assegurando resposta espectral radiométrica linear;
5. **Acionamento Sincronizado do Flash:** A iluminação foi provida com exclusividade pelo disparo sincronizado do flash LED integrado operando no interior vedado da câmara (`FLASH_MODE_SINGLE` / `CONTROL_CAPTURE_INTENT_STILL_CAPTURE`).

A captura em alto rendimento foi processada por meio de um buffer `ImageReader` não compactado na resolução nativa do sensor ($4000 \times 3000$ pixels; 12 megapixels) em formato planar `ImageFormat.YUV_420_888`, repassando os ponteiros nativos de memória diretamente ao C++ via JNI (*Java Native Interface*) para evitar pausas de coleta de lixo (*garbage collection*) na máquina virtual Java.

### 1.5. Pipeline de Visão Computacional, Segmentação em Cascata e Localização Adaptativa de ROI
Os quadros digitais brutos capturados na câmara foram processados por um pipeline automatizado de visão computacional de baixo nível implementado em C++ e Python sobre a biblioteca OpenCV.

#### 1.5.1. Normalização Cromática via Algoritmo Gray World
Embora o anel de neoprene vede a luz solar, o flash LED branco de smartphones apresenta distribuição de energia espectral com alta temperatura de cor correlata ($\approx 5.500--6.500\text{ K}$) e um proeminente pico de emissão de fósforo na faixa do azul ($\approx 450\text{ nm}$). O algoritmo Gray World normalizou as componentes cromáticas sob o postulado biofísico de que a média espacial de reflectância em uma cena biológica complexa integrada tende ao cinza acromático neutro:

$$\bar{R} = \frac{1}{|\Omega|} \sum_{p \in \Omega} R(p), \quad \bar{G} = \frac{1}{|\Omega|} \sum_{p \in \Omega} G(p), \quad \bar{B} = \frac{1}{|\Omega|} \sum_{p \in \Omega} B(p)$$

$$\mu_{\text{gray}} = \frac{\bar{R} + \bar{G} + \bar{B}}{3}$$

$$\alpha_R = \frac{\mu_{\text{gray}}}{\bar{R}}, \quad \alpha_G = \frac{\mu_{\text{gray}}}{\bar{G}}, \quad \alpha_B = \frac{\mu_{\text{gray}}}{\bar{B}}$$

Cada pixel $p$ na área biológica $\Omega$ foi reescalonado por:

$$I_{\text{corrigido}}(p) = \begin{bmatrix} \alpha_R \cdot R(p) \\ \alpha_G \cdot G(p) \\ \alpha_B \cdot B(p) \end{bmatrix}$$

neutralizando desvios espectrais antes da etapa de extração.

#### 1.5.2. Segmentação em Três Níveis em Cascata da Abertura Circular
Para isolar a cavidade circular de tecido biológico descartando as bordas plásticas da câmara de PVC, desenvolveu-se um algoritmo hierárquico em cascata de três níveis (`_detectar_circulo_abertura`):
1. **Nível 1 da Cascata (Otsu Dinâmico com Validação de Circularidade Morfológica):** A imagem foi convertida para escala de cinza e suavizada por filtro Gaussiano isotrópico ($25 \times 25$ pixels, $\sigma = 0$) para suprimir texturas capilares de alta frequência. Calculou-se um limiar adaptativo $\tau_{\text{thresh}} = \max(0{,}65 \cdot \tau_{\text{Otsu}}, 30)$. Operações morfológicas de fechamento seguidas de abertura com elemento estruturante elíptico ($31 \times 31$ pixels) fundiram reflexos especulares e selaram as bordas. Extraíram-se os contornos topológicos externos pelo algoritmo de Suzuki–Abe (`RETR_EXTERNAL`), ajustando o círculo mínimo envolvente $(\mathbf{c}, r_{\text{enc}})$ ao maior contorno $\mathcal{C}_{\text{max}}$. Avaliou-se o índice de circularidade morfológica:
   $$\Psi = \frac{\text{Área}(\mathcal{C}_{\text{max}})}{\pi \cdot r_{\text{enc}}^2}$$
   O contorno foi aceito como abertura real quando $\text{Área}(\mathcal{C}_{\text{max}}) > 0{,}05 \cdot (H \cdot W)$ e $\Psi \ge 0{,}72$;
2. **Nível 2 da Cascata (Transformada de Hough para Círculos):** Em pelames muito escuros ou com cerdas que deformam o contorno externo rompendo a circularidade ($\Psi < 0{,}72$), o algoritmo transitou automaticamente para a Transformada de Hough com gradiente (`HOUGH_GRADIENT`, resolução do acumulador $dp = 1{,}5$, limiar de gradiente $50$, limiar de acumulador $40$, raios limitados entre $0{,}18$ e $0{,}55 \cdot \min(H, W)$). Dentre os candidatos, selecionou-se o círculo de menor distância euclidiana ao centro óptico $(W/2, H/2)$;
3. **Nível 3 da Cascata (Fallback Geométrico Conservador):** Caso ambos os métodos analíticos fossem comprometidos por artefatos severos, acionou-se fallback com centro geométrico em $(W/2, H/2)$ e raio fixo $r = 0{,}40 \cdot \min(H, W)$;
4. **Erosão Radial de Segurança Interna:** Para evitar contaminação por brilhos especulares no bisel interno de plástico do PVC, aplicou-se erosão radial de $2\%$ (`margin_pct = 0.02`), definindo $r_{\text{efetivo}} = \lfloor r \cdot (1 - 0{,}02) \rfloor$, preenchendo a região externa com fundo branco puro ($255, 255, 255$).

#### 1.5.3. Discriminação Adaptativa de Tecido e Localização de ROI Biológica
Em campo, o sistema avalia duas superfícies anatômicas distintas: pele tricotomizada (uma mancha raspada escura delimitada por pelos) e pelame intacto (superfície contínua e homogênea). Criou-se uma rotina discriminante automática (`detectar_mancha_pele`):
1. **Perfilamento Estatístico de Luminância:** Analisou-se a distribuição de intensidade nos pixels internos da abertura circular, extraindo o percentil 5 ($p_5$), percentil 25 ($p_{25}$), mediana ($p_{50}$) e desvio padrão ($\sigma$);
2. **Lógica de Decisão:**
   $$\text{Tipo de Amostra} = \begin{cases} \text{Pele (Mancha Raspada)}, & \text{se } p_5 < 60 \text{ e } \sigma > 30 \\ \text{Pelame (Superfície Homogênea)}, & \text{caso contrário} \end{cases}$$
   Quando classificado como pelame, toda a abertura circular é selecionada com margem de segurança de $5\%$;
3. **Isolamento da Mancha de Pele e Máscara de Oclusão:**
   - *Máscara de Etiqueta de Identificação:* Fitas adesivas ou brincos situados no dorso bovino frequentemente projetam-se na borda superior da abertura. Uma linha de corte vertical (`label_cutoff = y_{\text{topo}} + 0{,}22 \cdot H_{\text{abertura}}`) eliminou automaticamente os $22\%$ superiores da câmara;
   - *Limiarização Adaptativa:* Na área inferior, aplicou-se limiar $\tau_{\text{mancha}} = \min(p_{50} - 10, 105)$ sobre imagem com suavização Gaussiana ($151 \times 151$);
   - *Retificação Morfológica:* Fechamento e abertura com kernel quadrado ($61 \times 61$) consolidaram os folículos pilosos em uma massa contínua;
   - *Extração da Bounding Box:* O contorno biológico válido (área entre $10\%$ e $60\%$ da abertura) foi delimitado por caixa retangular $[X, Y, W, H]$ expandida com $5\%$ de margem (*padding*), gerando a ROI analítica final.

### 1.6. Engenharia de Atributos Fotométricos Multicanal em Grade Espacial $3 \times 3$ (14 Variáveis)
O disparo do flash em câmara cilíndrica gera um gradiente radial intrínseco de luminância (incidência perpendicular e especular no centro axial, atenuando-se em espalhamento difuso oblíquo em direção às bordas periféricas). O cálculo de uma média global única colapsaria essa rica variabilidade espacial.

Para preservar a física da atenuação de luz, a ROI biológica foi dividida em uma **grade geométrica regular de $3 \times 3$ (9 sub-blocos independentes)**:
- 1 bloco central capturando a incidência especular direta do flash;
- 8 blocos periféricos capturando o espalhamento volumétrico difuso tecidual.

De cada sub-bloco espacial $g \in \{1, \dots, 9\}$, extraiu-se um vetor de 14 atributos fotométricos $\mathbf{x}_g \in \mathbb{R}^{14}$ integrando três espaços de cor e razões biofísicas não lineares:
- **Canais Fotométricos Diretos dos Espaços de Cor (9 atributos):**
  - Espaço RGB: Intensidades médias Vermelho ($\bar{R}$), Verde ($\bar{G}$) e Azul ($\bar{B}$) na escala $0--255$;
  - Espaço HSV: Matiz ($\bar{H}$, comprimento de onda dominante), Saturação ($\bar{S}$, pureza cromática) e Valor ($\bar{V}$, intensidade luminosa acromática);
  - Espaço CIELAB Escalonado do OpenCV: Luminosidade ($\bar{L}_{\text{cv2}}$), oponência verde-vermelho ($\bar{a}_{\text{cv2}}$) e azul-amarelo ($\bar{b}_{\text{cv2}}$);
- **Razões Biofísicas Não Lineares e Descritores Invariantes (5 atributos):**
  - $\text{Razao}_{\text{RG}} = \frac{\bar{R}}{\bar{G} + \epsilon}$ ($\epsilon = 10^{-5}$): Indicador de eritema cutâneo e perfusão micro-vascular capilar dérmica (sensível à hemoglobina);
  - $\text{Razao}_{\text{RB}} = \frac{\bar{R}}{\bar{B} + \epsilon}$: Razão espectral associada à proporção eumelanina/feomelanina na epiderme;
  - $\text{Razao}_{\text{GB}} = \frac{\bar{G}}{\bar{B} + \epsilon}$: Indicador de espalhamento óptico em fibras de queratina e ar medular nas cerdas de pelame;
  - $\text{Dif}_{LV} = \bar{L}_{\text{cv2}} - \bar{V}$: Métrica de desacoplamento entre brilho perceptual psicométrico e intensidade fotônica acromática linear, neutralizando reflexos especulares do flash;
  - $\text{Soma}_{\text{RGB}} = \bar{R} + \bar{G} + \bar{B}$: Proxy de energia fotométrica total integrada refletida pelo tecido.

A concatenação das 9 células da grade gerou uma assinatura vetorial que contempla tanto o brilho axial direto quanto o espalhamento periférico tecidual.

### 1.7. Modelagem por Inteligência Artificial, Duplo Especialista e Estudo de Ablação
A epiderme bovina tricotomizada (tecido biológico vivo turbidimétrico, vascularizado, com espalhamento volumétrico) e o pelame intacto (cilindros de queratina anisotrópicos com reflexão especular) apresentam Funções de Distribuição de Reflectância Bidirecional (BRDF) essencialmente distintas. O treinamento de regressores unificados impõe fronteiras de decisão conflitantes.

Adotou-se uma **arquitetura de duplo especialista**:
1. **Regressores Especialistas em Pele ($\mathcal{M}_{\text{pele}}$):** Calibrados exclusivamente sobre amostras epidérmicas tricotomizadas;
2. **Regressores Especialistas em Pelame ($\mathcal{M}_{\text{pelo}}$):** Calibrados exclusivamente sobre espécimes de pelame intacto.

#### Estudo Sistemático de Ablação Arquitetural e Espacial
Para determinar objetivamente a melhor resolução de grade e o algoritmo preditivo ótimo, conduziu-se um **experimento de ablação** com 12 configurações distintas (Tabela S1). Quatro resoluções de grade ($1 \times 1$, $2 \times 2$, $3 \times 3$ e $4 \times 4$, gerando 1, 4, 9 e 16 amostras espaciais por imagem) foram cruzadas com três famílias de modelos:
- **Random Forest:** Ensemble bagging com $B = 200$ árvores aleatorizadas, profundidade máxima limitada a $\text{max\_depth} = 15$ e regressão multi-saída;
- **Extra Trees:** Ensemble de $B = 200$ árvores extremamente aleatorizadas com particionamento randômico de corte;
- **Gradient Boosting:** Ensembles sequenciais com taxa de aprendizado $\eta = 0{,}05$ e profundidade 15 em wrapper `MultiOutputRegressor`.

Conforme detalhado na Tabela S1, a **Random Forest com grade $3 \times 3$ (9 células)** obteve o desempenho superior global ($\Delta E^*_{ab} = 2{,}923$, $R^2 = 0{,}791$, $\text{MAE}_{L^*} = 2{,}472$, $\text{MAE}_{a^*} = 0{,}625$, $\text{MAE}_{b^*} = 0{,}907$). Modelos globais ($1 \times 1$) apresentaram erro significativamente maior ($\Delta E^*_{ab} > 3{,}03$), e o Gradient Boosting sofreu sobreajuste a reflexos especulares locais ($\Delta E^*_{ab} = 3{,}742$).

### 1.8. Protocolo de Validação: Separação Estrita por Animal (`GroupShuffleSplit`)
Para prevenir contaminação de dados (*data leakage*) e pseudorrepetição amostral, foi vetada a amostragem aleatória convencional (`train_test_split`). Como cada animal possui assinatura fenotípica singular de densidade folicular e pigmentação, alocar células espaciais ou fotos repetidas de um mesmo indivíduo entre treino e teste levaria à memorização do animal em vez do aprendizado das leis bio-ópticas da cor.

A partição foi estruturada estritamente pelo identificador biológico do animal (`GroupShuffleSplit`, `Group = Animal ID`):
- **Coorte de Treinamento (80% dos indivíduos):** 37 animais únicos (1.872 amostras de grade);
- **Coorte de Teste Independente (20% dos indivíduos):** 10 animais completamente inéditos (504 amostras de grade).

Nenhuma imagem ou medição dos 10 animais de teste esteve presente no ajuste, garantindo que as métricas reportadas reflitam a acurácia metrológica em animais nunca antes vistos.

### 1.9. Arquitetura do Aplicativo Móvel Edge-AI Android e Engenharia de Software
Para converter os modelos e algoritmos em ferramenta de uso direto no curral, o pipeline computacional e os regressores Random Forest foram compilados em um aplicativo móvel nativo autônomo para Android:

#### 1.9.1. Pilha Tecnológica e Arquitetura em Camadas
- **Núcleo do Aplicativo:** Desenvolvido em Kotlin segundo as diretrizes de arquitetura moderna Android Jetpack (Jetpack Compose para interface reativa, ViewModel para ciclo de vida e Kotlin Coroutines para concorrência assíncrona);
- **Ponte Nativa de Processamento (JNI / C++):** Processamento pesado de matrizes de imagem executado em C++ de baixo nível via OpenCV Android SDK (v4.8.0) integrado via JNI (*Java Native Interface*). Buffers brutos de imagem da API Camera2 são mapeados via ponteiros nativos, eliminando alocações na heap da JVM;
- **Motor de Inferência Edge-AI:** Execução de inferência de alta performance através da API C++ do Microsoft ONNX Runtime Mobile (v1.16).

#### 1.9.2. Quantização de Modelos, Otimização de Grafos e Ocupação de Memória
- **Serialização de Grafos ONNX:** Os ensembles Random Forest foram convertidos para o formato aberto ONNX via `skl2onnx` compatível com Opset 15;
- **Quantização Dinâmica em Ponto Flutuante:** As matrizes de nós das árvores receberam quantização dinâmica, reduzindo o tamanho em disco dos modelos especialistas de $> 35\text{ MB}$ para binários compactos de $< 8{,}5\text{ MB}$;
- **Tempo de Inicialização a Frio:** O grafo ONNX é carregado e alocado na memória RAM do smartphone em $< 45\text{ ms}$, garantindo inicialização instantânea no curral.

#### 1.9.3. Balanço de Latência Computacional e Execução em Tempo Real
A latência computacional de ponta a ponta foi perfilada em processador móvel octa-core (ARM Cortex-A78 a 2,4 GHz + Cortex-A55 a 2,0 GHz). O ciclo completo consumiu $< 140\text{ ms}$:
1. Exposição do sensor CMOS e transferência DMA do quadro: $28\text{ ms}$;
2. Mapeamento de memória JNI, conversão planar YUV para RGB e algoritmo Gray World: $18\text{ ms}$;
3. Segmentação em cascata da abertura circular e discriminação de tecido: $24\text{ ms}$;
4. Particionamento na grade $3 \times 3$ e extração dos 14 atributos multicanal: $35\text{ ms}$;
5. Inferência nos modelos Random Forest especialistas via ONNX Runtime: $15\text{ ms}$;
6. Persistência local no banco Room/SQLite e renderização diagnóstica na UI: $10\text{ ms}$.

Com latência total de $\approx 130\text{ ms}$, o sistema atinge vazão operacional de $> 7{,}5\text{ avaliações por segundo}$, superando com folga equipamentos de bancada que exigem calibração manual e múltiplos segundos por medição.

#### 1.9.4. Computação de Borda 100% Offline, Estabilidade Térmica e Integração Empresarial
- **Operação 100% Offline:** Todo o processamento de visão, engenharia de atributos e inferência de machine learning executa estritamente na CPU/NPU do smartphone, sem qualquer dependência de sinal de internet, dados móveis ou nuvem, viabilizando o uso em currais remotos;
- **Desempenho Térmico e Energético:** Em ensaios contínuos no brete, o consumo de bateria foi de $< 2{,}8\%$ para cada 100 bovinos avaliados. Nenhuma queda de frequência por afogamento térmico (*thermal throttling*) ocorreu durante 3 horas de coleta contínua sob temperaturas ambientes de até $36\,^\circ\text{C}$;
- **Persistência Local Transacional (Room / SQLite):** Cada mensuração é armazenada com garantias ACID em banco de dados SQLite local gerenciado pela biblioteca Android Jetpack Room. O esquema armazena carimbo de data/hora, identificação de brinco (visual ou RFID), classificação de tecido, coordenadas $L^*, a^*, b^*$ preditas, $\Delta E^*_{ab}$, swatch visual em código hexadecimal, dados meteorológicos e diagnósticos de calibração;
- **Interoperabilidade com Softwares Pecuários:** O aplicativo oferece exportação instantânea para CSV, JSON e padrões compatíveis com sistemas de gestão pecuária (Sisbov, softwares de gestão de rebanho e programas de melhoramento genético).

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
