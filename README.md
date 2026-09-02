# Medical Image Processing Pipeline

A Python-based medical image processing project for analyzing brain MRI images using classical computer vision techniques.

## Overview

This project demonstrates a complete image-processing pipeline applied to a small subset of a public brain MRI dataset.

The pipeline performs:

- Image preprocessing
- Grayscale conversion
- Gaussian filtering
- Canny edge detection
- Fixed threshold segmentation
- Otsu threshold segmentation
- Adaptive threshold segmentation
- Morphological processing
- Contour detection
- Feature extraction
- Statistical analysis
- Visualization

## Dataset

The project uses a small sample of a public brain MRI dataset containing four classes:

- Glioma
- Meningioma
- No Tumor
- Pituitary

For this demonstration, 20 images were used, with 5 images from each class.

The dataset is used only for educational and portfolio purposes.

## Project Pipeline

```text
MRI Images
     |
     v
Image Loading
     |
     v
Grayscale Conversion
     |
     v
Gaussian Blur
     |
     +----------------------+
     |                      |
     v                      v
Canny Edge Detection    Segmentation
                            |
                 +----------+----------+
                 |          |          |
                 v          v          v
               Fixed       Otsu     Adaptive
                 |          |          |
                 +----------+----------+
                            |
                            v
                  Morphological Processing
                            |
                            v
                    Contour Detection
                            |
                            v
                    Feature Extraction
                            |
                            v
                   Statistical Analysis
                            |
                            v
                     Visualization


                     ## Interpretation of Segmentation Results

The segmentation percentages represent the proportion of image pixels classified as foreground by each thresholding method. They should **not** be interpreted as tumor size or tumor area.

For example, the average Otsu segmentation value of **42.04%** means that approximately 42.04% of the image pixels were classified as foreground by the Otsu thresholding method across the 20-image sample. It does not mean that 42.04% of the brain contains a tumor.

Similarly, the Fixed Threshold and Adaptive Threshold values represent foreground-pixel percentages produced by those respective image-processing methods.

Because this project uses a small sample and does not have manually annotated tumor masks (ground truth), the segmentation results are intended for **image-processing method comparison and educational analysis**, not clinical diagnosis or quantitative tumor measurement.

### Limitations

* The dataset used for this demonstration contains only 20 MRI images.
* The segmentation methods are traditional image-processing techniques and are not clinically validated.
* No ground-truth tumor masks are available for calculating segmentation accuracy metrics such as Dice score or IoU.
* Foreground regions detected by thresholding may include normal brain structures, background, or other image artifacts.
* The reported segmented-area percentages should therefore not be considered medically meaningful tumor measurements.
