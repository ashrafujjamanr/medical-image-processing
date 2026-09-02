import cv2
from pathlib import Path
import matplotlib.pyplot as plt
import csv


# ==============================
# Project directories
# ==============================

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
RESULTS_DIR = Path("results")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ==============================
# CSV file
# ==============================

csv_path = RESULTS_DIR / "image_statistics.csv"

statistics = []


# ==============================
# MRI class mapping
# ==============================

class_mapping = {
    "gl": "Glioma",
    "me": "Meningioma",
    "no": "No Tumor",
    "pi": "Pituitary"
}


# ==============================
# Process each image
# ==============================

for image_path in RAW_DIR.iterdir():

    if image_path.suffix.lower() not in [
        ".jpg",
        ".jpeg",
        ".png"
    ]:
        continue

    image = cv2.imread(str(image_path))

    if image is None:
        print(
            f"Could not read: {image_path.name}"
        )
        continue


    # ==============================
    # Identify class
    # ==============================

    prefix = (
        image_path.stem
        .split("-")[1]
        .split("_")[0]
    )

    image_class = class_mapping.get(
        prefix,
        "Unknown"
    )


    # ==============================
    # Preprocessing
    # ==============================

    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    blurred = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )


    # ==============================
    # Canny edge detection
    # ==============================

    edges = cv2.Canny(
        blurred,
        50,
        150
    )

    processed_path = (
        PROCESSED_DIR /
        f"{image_path.stem}_processed.png"
    )

    cv2.imwrite(
        str(processed_path),
        edges
    )


    # ==============================
    # 1. Fixed threshold
    # ==============================

    _, fixed_threshold = cv2.threshold(
        blurred,
        100,
        255,
        cv2.THRESH_BINARY
    )


    # ==============================
    # 2. Otsu thresholding
    # ==============================

    otsu_threshold_value, otsu = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )


    # ==============================
    # 3. Adaptive thresholding
    # ==============================

    adaptive = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )


    # ==============================
    # Morphological processing
    # ==============================

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (5, 5)
    )


    fixed_segmentation = cv2.morphologyEx(
        fixed_threshold,
        cv2.MORPH_OPEN,
        kernel
    )


    otsu_segmentation = cv2.morphologyEx(
        otsu,
        cv2.MORPH_OPEN,
        kernel
    )


    adaptive_segmentation = cv2.morphologyEx(
        adaptive,
        cv2.MORPH_OPEN,
        kernel
    )


    # ==============================
    # Save segmentation images
    # ==============================

    cv2.imwrite(
        str(
            PROCESSED_DIR /
            f"{image_path.stem}_fixed.png"
        ),
        fixed_segmentation
    )


    cv2.imwrite(
        str(
            PROCESSED_DIR /
            f"{image_path.stem}_otsu.png"
        ),
        otsu_segmentation
    )


    cv2.imwrite(
        str(
            PROCESSED_DIR /
            f"{image_path.stem}_adaptive.png"
        ),
        adaptive_segmentation
    )


    # ==============================
    # Basic image statistics
    # ==============================

    height, width = gray.shape

    total_pixels = width * height

    mean_intensity = gray.mean()

    standard_deviation = gray.std()


    # ==============================
    # Edge statistics
    # ==============================

    edge_pixels = cv2.countNonZero(
        edges
    )

    edge_percentage = (
        edge_pixels /
        total_pixels
    ) * 100


    # ==============================
    # Segmentation statistics
    # ==============================

    fixed_pixels = cv2.countNonZero(
        fixed_segmentation
    )

    otsu_pixels = cv2.countNonZero(
        otsu_segmentation
    )

    adaptive_pixels = cv2.countNonZero(
        adaptive_segmentation
    )


    fixed_percentage = (
        fixed_pixels /
        total_pixels
    ) * 100


    otsu_percentage = (
        otsu_pixels /
        total_pixels
    ) * 100


    adaptive_percentage = (
        adaptive_pixels /
        total_pixels
    ) * 100


    # ==============================
    # Find Otsu contours
    # ==============================

    contours, _ = cv2.findContours(
        otsu_segmentation,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    contours = sorted(
        contours,
        key=cv2.contourArea,
        reverse=True
    )


    # ==============================
    # Largest Otsu contour
    # ==============================

    if len(contours) > 0:

        largest_contour = contours[0]

        largest_contour_area = (
            cv2.contourArea(
                largest_contour
            )
        )

        x, y, w, h = cv2.boundingRect(
            largest_contour
        )

    else:

        largest_contour_area = 0

        x = 0
        y = 0
        w = 0
        h = 0


    largest_contour_percentage = (
        largest_contour_area /
        total_pixels
    ) * 100


    # ==============================
    # Draw Otsu contours
    # ==============================

    contour_image = image_rgb.copy()


    cv2.drawContours(
        contour_image,
        contours[:5],
        -1,
        (255, 0, 0),
        2
    )


    contour_path = (
        RESULTS_DIR /
        f"{image_path.stem}_contours.png"
    )


    cv2.imwrite(
        str(contour_path),
        cv2.cvtColor(
            contour_image,
            cv2.COLOR_RGB2BGR
        )
    )


    # ==============================
    # Save statistics
    # ==============================

    statistics.append([

        image_path.name,

        image_class,

        width,

        height,

        round(
            mean_intensity,
            2
        ),

        round(
            standard_deviation,
            2
        ),

        edge_pixels,

        round(
            edge_percentage,
            2
        ),

        fixed_pixels,

        round(
            fixed_percentage,
            2
        ),

        otsu_pixels,

        round(
            otsu_percentage,
            2
        ),

        adaptive_pixels,

        round(
            adaptive_percentage,
            2
        ),

        round(
            otsu_threshold_value,
            2
        ),

        round(
            largest_contour_area,
            2
        ),

        round(
            largest_contour_percentage,
            2
        ),

        w,

        h
    ])


    # ==============================
    # 5-panel comparison
    # ==============================

    plt.figure(
        figsize=(20, 5)
    )


    # Original
    plt.subplot(
        1,
        5,
        1
    )

    plt.imshow(
        image_rgb
    )

    plt.title(
        f"Original - {image_class}"
    )

    plt.axis("off")


    # Fixed
    plt.subplot(
        1,
        5,
        2
    )

    plt.imshow(
        fixed_segmentation,
        cmap="gray"
    )

    plt.title(
        "Fixed Threshold"
    )

    plt.axis("off")


    # Otsu
    plt.subplot(
        1,
        5,
        3
    )

    plt.imshow(
        otsu_segmentation,
        cmap="gray"
    )

    plt.title(
        f"Otsu (T={otsu_threshold_value:.0f})"
    )

    plt.axis("off")


    # Adaptive
    plt.subplot(
        1,
        5,
        4
    )

    plt.imshow(
        adaptive_segmentation,
        cmap="gray"
    )

    plt.title(
        "Adaptive Threshold"
    )

    plt.axis("off")


    # Contours
    plt.subplot(
        1,
        5,
        5
    )

    plt.imshow(
        contour_image
    )

    plt.title(
        "Otsu Contours"
    )

    plt.axis("off")


    plt.tight_layout()


    comparison_path = (
        RESULTS_DIR /
        f"{image_path.stem}_comparison.png"
    )


    plt.savefig(
        comparison_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()


    print(
        f"Processed: {image_path.name} "
        f"({image_class})"
    )


# ==============================
# Save CSV
# ==============================

with open(
    csv_path,
    "w",
    newline=""
) as file:

    writer = csv.writer(file)


    writer.writerow([

        "Image",
        "Class",
        "Width",
        "Height",
        "Mean Intensity",
        "Standard Deviation",
        "Edge Pixels",
        "Edge Percentage",

        "Fixed Segmented Pixels",
        "Fixed Segmented Area Percentage",

        "Otsu Segmented Pixels",
        "Otsu Segmented Area Percentage",

        "Adaptive Segmented Pixels",
        "Adaptive Segmented Area Percentage",

        "Otsu Threshold",

        "Largest Otsu Contour Area",
        "Largest Otsu Contour Percentage",

        "Bounding Box Width",
        "Bounding Box Height"
    ])


    writer.writerows(
        statistics
    )


# ==============================
# Compare segmentation methods
# ==============================

methods = {
    "Fixed Threshold": [],
    "Otsu Threshold": [],
    "Adaptive Threshold": []
}


for row in statistics:

    methods[
        "Fixed Threshold"
    ].append(row[9])

    methods[
        "Otsu Threshold"
    ].append(row[11])

    methods[
        "Adaptive Threshold"
    ].append(row[13])


average_methods = {}


for method, values in methods.items():

    average_methods[method] = (
        sum(values)
        / len(values)
    )


print(
    "\nAverage Segmented Area:"
)

print(
    "============================"
)


for method, average in average_methods.items():

    print(
        f"{method}: "
        f"{average:.2f}%"
    )


# ==============================
# Segmentation comparison graph
# ==============================

method_names = list(
    average_methods.keys()
)

method_values = list(
    average_methods.values()
)


plt.figure(
    figsize=(10, 6)
)

plt.bar(
    method_names,
    method_values
)

plt.title(
    "Comparison of Segmentation Methods"
)

plt.xlabel(
    "Segmentation Method"
)

plt.ylabel(
    "Average Segmented Area (%)"
)

plt.tight_layout()


segmentation_chart = (
    RESULTS_DIR /
    "segmentation_method_comparison.png"
)


plt.savefig(
    segmentation_chart,
    dpi=150,
    bbox_inches="tight"
)

plt.close()


# ==============================
# Finished
# ==============================

print(
    "\nImage processing completed!"
)

print(
    f"Statistics saved to: {csv_path}"
)

print(
    "Segmentation comparison saved to:"
)

print(
    segmentation_chart
)