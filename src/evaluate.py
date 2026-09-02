import csv
from pathlib import Path

import matplotlib.pyplot as plt


# ==============================
# Paths
# ==============================

CSV_PATH = Path("results/image_statistics.csv")
RESULTS_DIR = Path("results")


# ==============================
# Load CSV
# ==============================

data = []

with open(
    CSV_PATH,
    "r",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        data.append(row)


print(
    f"Loaded {len(data)} images."
)


# ==============================
# Extract segmentation results
# ==============================

fixed = []
otsu = []
adaptive = []


for row in data:

    fixed.append(
        float(
            row[
                "Fixed Segmented Area Percentage"
            ]
        )
    )

    otsu.append(
        float(
            row[
                "Otsu Segmented Area Percentage"
            ]
        )
    )

    adaptive.append(
        float(
            row[
                "Adaptive Segmented Area Percentage"
            ]
        )
    )


# ==============================
# Calculate averages
# ==============================

fixed_average = (
    sum(fixed) / len(fixed)
)

otsu_average = (
    sum(otsu) / len(otsu)
)

adaptive_average = (
    sum(adaptive) / len(adaptive)
)


print("\nSegmentation Evaluation")
print("============================")

print(
    f"Fixed threshold average: "
    f"{fixed_average:.2f}%"
)

print(
    f"Otsu threshold average: "
    f"{otsu_average:.2f}%"
)

print(
    f"Adaptive threshold average: "
    f"{adaptive_average:.2f}%"
)


# ==============================
# Calculate variation
# ==============================

def calculate_std(values):

    mean = sum(values) / len(values)

    squared_differences = [
        (value - mean) ** 2
        for value in values
    ]

    variance = (
        sum(squared_differences)
        / len(values)
    )

    return variance ** 0.5


fixed_std = calculate_std(fixed)

otsu_std = calculate_std(otsu)

adaptive_std = calculate_std(adaptive)


print("\nVariation")
print("============================")

print(
    f"Fixed threshold STD: "
    f"{fixed_std:.2f}"
)

print(
    f"Otsu threshold STD: "
    f"{otsu_std:.2f}"
)

print(
    f"Adaptive threshold STD: "
    f"{adaptive_std:.2f}"
)


# ==============================
# Box plot
# ==============================

plt.figure(
    figsize=(10, 6)
)

plt.boxplot(
    [
        fixed,
        otsu,
        adaptive
    ],
    tick_labels=[
        "Fixed",
        "Otsu",
        "Adaptive"
    ]
)

plt.title(
    "Segmentation Method Comparison"
)

plt.xlabel(
    "Segmentation Method"
)

plt.ylabel(
    "Segmented Area (%)"
)

plt.tight_layout()


boxplot_path = (
    RESULTS_DIR /
    "segmentation_boxplot.png"
)


plt.savefig(
    boxplot_path,
    dpi=150,
    bbox_inches="tight"
)

plt.close()


# ==============================
# Final report
# ==============================

report_path = (
    RESULTS_DIR /
    "analysis_summary.txt"
)


with open(
    report_path,
    "w"
) as report:

    report.write(
        "Medical Image Processing Analysis\n"
    )

    report.write(
        "=================================\n\n"
    )

    report.write(
        f"Number of images analyzed: "
        f"{len(data)}\n\n"
    )

    report.write(
        "Segmentation methods:\n"
    )

    report.write(
        f"- Fixed threshold: "
        f"{fixed_average:.2f}% average area\n"
    )

    report.write(
        f"- Otsu threshold: "
        f"{otsu_average:.2f}% average area\n"
    )

    report.write(
        f"- Adaptive threshold: "
        f"{adaptive_average:.2f}% average area\n\n"
    )

    report.write(
        "Standard deviation:\n"
    )

    report.write(
        f"- Fixed: "
        f"{fixed_std:.2f}\n"
    )

    report.write(
        f"- Otsu: "
        f"{otsu_std:.2f}\n"
    )

    report.write(
        f"- Adaptive: "
        f"{adaptive_std:.2f}\n\n"
    )

    report.write(
        "Note:\n"
    )

    report.write(
        "The segmentation results represent "
        "thresholded image regions and should "
        "not be interpreted as clinically "
        "validated tumor measurements.\n"
    )


print(
    "\nEvaluation completed!"
)

print(
    f"Box plot saved to: "
    f"{boxplot_path}"
)

print(
    f"Summary saved to: "
    f"{report_path}"
)