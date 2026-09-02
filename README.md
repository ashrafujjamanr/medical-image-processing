# Medical Image Processing & MRI Segmentation

A Python-based medical image processing project for analyzing brain MRI images using classical computer vision techniques.

The project implements an end-to-end image-processing pipeline including preprocessing, edge detection, threshold-based segmentation, morphological operations, contour detection, feature extraction, and quantitative analysis.

## Project Overview

This project explores how traditional image-processing techniques can be applied to brain MRI images to identify and analyze image regions based on intensity and structural characteristics.

The pipeline processes MRI images and generates quantitative statistics and visualizations for comparing different segmentation approaches.

> **Important:** This is an educational image-processing project and is **not a clinical diagnostic system**. The segmentation results represent foreground regions detected by image-processing algorithms and should not be interpreted as actual tumor measurements.

## Processing Pipeline

```text
MRI Image
   ↓
Grayscale Conversion
   ↓
Gaussian Blur
   ↓
Canny Edge Detection
   ↓
Threshold-Based Segmentation
   ├── Fixed Threshold
   ├── Otsu Threshold
   └── Adaptive Threshold
   ↓
Morphological Opening
   ↓
Contour Detection
   ↓
Feature Extraction
   ↓
Statistical Analysis & Visualization
```

## Features

* MRI image loading and preprocessing
* RGB-to-grayscale conversion
* Gaussian noise reduction
* Canny edge detection
* Fixed threshold segmentation
* Otsu threshold segmentation
* Adaptive threshold segmentation
* Morphological opening
* Contour detection
* Largest contour analysis
* Image intensity analysis
* Edge percentage calculation
* Segmented-area analysis
* Class-level statistical comparison
* CSV-based result generation
* Automated visualization
* Segmentation method comparison

## Dataset

The project was demonstrated using a small sample of **20 brain MRI images** from a publicly available Brain MRI dataset.

The sample contains four classes:

* Glioma
* Meningioma
* Pituitary
* No Tumor

The dataset itself is **not included in this repository**. This keeps the repository lightweight and avoids unnecessarily distributing the dataset.

To reproduce the project, place the selected MRI images inside:

```text
data/raw/
```

## Technologies Used

* **Python**
* **OpenCV**
* **NumPy**
* **Matplotlib**
* **Pillow**
* **CSV**
* **Git & GitHub**

## Project Structure

```text
medical-image-processing/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── main.py
│   ├── analyze.py
│   └── evaluate.py
│
└── results/
    ├── analysis_summary.txt
    ├── average_contour_area.png
    ├── average_edge_percentage.png
    ├── average_intensity.png
    ├── average_segmented_area.png
    ├── class_edge_comparison.png
    ├── class_segmented_comparison.png
    ├── image_statistics.csv
    ├── intensity_vs_edges.png
    └── segmentation_boxplot.png
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/ashrafujjamanr/medical-image-processing.git
cd medical-image-processing
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Add MRI images

Place the MRI images inside:

```text
data/raw/
```

### 6. Run the processing pipeline

```bash
python src/main.py
```

### 7. Run the analysis

```bash
python src/analyze.py
```

### 8. Run segmentation evaluation

```bash
python src/evaluate.py
```

The generated statistics and visualizations will be stored in:

```text
results/
```

## Results

The project compared three threshold-based segmentation techniques across the 20-image sample.

| Segmentation Method | Average Foreground Pixel Percentage |
| ------------------- | ----------------------------------: |
| Fixed Threshold     |                          **10.94%** |
| Otsu Threshold      |                          **42.04%** |
| Adaptive Threshold  |                          **73.66%** |

### Interpretation

These percentages represent the proportion of image pixels classified as **foreground** by each segmentation method.

For example, the Otsu result of **42.04% does not mean that 42.04% of the brain contains a tumor**.

Because the dataset does not provide manually annotated tumor masks (ground truth), these measurements are used to compare the behavior of different image-processing techniques rather than to measure actual tumor size.

## Limitations

* Only 20 MRI images were used for this demonstration.
* The segmentation methods are traditional image-processing techniques and are not clinically validated.
* No ground-truth tumor masks are available.
* Dice coefficient and IoU therefore cannot be reliably calculated for tumor segmentation.
* Threshold-based segmentation may classify normal brain structures, background, or image artifacts as foreground.
* The reported segmentation percentages should not be considered medical or clinical measurements.

## Future Improvements

Possible extensions include:

* Use a larger MRI dataset
* Add manually annotated tumor masks
* Evaluate segmentation using Dice coefficient and IoU
* Experiment with watershed segmentation
* Explore active contour methods
* Add image normalization
* Investigate deep-learning-based segmentation
* Develop a simple graphical user interface
* Add automated experiment reporting

## Learning Outcomes

Through this project, I gained practical experience with:

* Medical image preprocessing
* Classical computer vision techniques
* Image segmentation
* Edge and contour detection
* Morphological image processing
* Feature extraction
* Statistical analysis
* Python-based automation
* Git and GitHub project management

## Author

**Ashrafujjaman Raky**

Electronics & Communication Engineering Graduate
Medical Engineering(Medical Image and Data Processing)(Pursuing)

GitHub: [ashrafujjamanr](https://github.com/ashrafujjamanr)
