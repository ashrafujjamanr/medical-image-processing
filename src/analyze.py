import csv
from pathlib import Path
import matplotlib.pyplot as plt


# =========================
# Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "results" / "image_statistics.csv"
RESULTS_DIR = BASE_DIR / "results"

RESULTS_DIR.mkdir(exist_ok=True)


# =========================
# Load CSV
# =========================

data = []

with open(CSV_FILE, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        data.append(row)

print(f"Loaded {len(data)} images.")


# =========================
# Class names
# =========================

classes = [
    "Glioma",
    "Meningioma",
    "Pituitary",
    "No Tumor"
]


# =========================
# Calculate class averages
# =========================

class_data = {}

for class_name in classes:

    rows = [
        row for row in data
        if row["Class"] == class_name
    ]

    if not rows:
        continue

    mean_intensity = sum(
        float(row["Mean Intensity"])
        for row in rows
    ) / len(rows)

    edge_percentage = sum(
        float(row["Edge Percentage"])
        for row in rows
    ) / len(rows)

    fixed_percentage = sum(
        float(row["Fixed Segmented Area Percentage"])
        for row in rows
    ) / len(rows)

    otsu_percentage = sum(
        float(row["Otsu Segmented Area Percentage"])
        for row in rows
    ) / len(rows)

    adaptive_percentage = sum(
        float(row["Adaptive Segmented Area Percentage"])
        for row in rows
    ) / len(rows)

    class_data[class_name] = {
        "Mean Intensity": mean_intensity,
        "Edge Percentage": edge_percentage,
        "Fixed": fixed_percentage,
        "Otsu": otsu_percentage,
        "Adaptive": adaptive_percentage
    }


# =========================
# Print results
# =========================

print("\nClass Analysis")
print("============================")

for class_name, values in class_data.items():

    print(f"\n{class_name}")

    print(
        f"Mean intensity: "
        f"{values['Mean Intensity']:.2f}"
    )

    print(
        f"Edge percentage: "
        f"{values['Edge Percentage']:.2f}%"
    )

    print(
        f"Fixed segmentation: "
        f"{values['Fixed']:.2f}%"
    )

    print(
        f"Otsu segmentation: "
        f"{values['Otsu']:.2f}%"
    )

    print(
        f"Adaptive segmentation: "
        f"{values['Adaptive']:.2f}%"
    )


# =========================
# 1. Average intensity
# =========================

class_names = list(class_data.keys())

intensities = [
    class_data[c]["Mean Intensity"]
    for c in class_names
]

plt.figure(figsize=(8, 5))

plt.bar(
    class_names,
    intensities
)

plt.title("Average Image Intensity by Class")
plt.xlabel("Class")
plt.ylabel("Mean Intensity")

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "average_intensity.png",
    dpi=300
)

plt.close()


# =========================
# 2. Edge comparison
# =========================

edge_values = [
    class_data[c]["Edge Percentage"]
    for c in class_names
]

plt.figure(figsize=(8, 5))

plt.bar(
    class_names,
    edge_values
)

plt.title("Average Edge Percentage by Class")
plt.xlabel("Class")
plt.ylabel("Edge Percentage (%)")

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "class_edge_comparison.png",
    dpi=300
)

plt.close()


# =========================
# 3. Segmentation comparison
# =========================

fixed_values = [
    class_data[c]["Fixed"]
    for c in class_names
]

otsu_values = [
    class_data[c]["Otsu"]
    for c in class_names
]

adaptive_values = [
    class_data[c]["Adaptive"]
    for c in class_names
]

x = range(len(class_names))
width = 0.25

plt.figure(figsize=(10, 6))

plt.bar(
    [i - width for i in x],
    fixed_values,
    width=width,
    label="Fixed"
)

plt.bar(
    x,
    otsu_values,
    width=width,
    label="Otsu"
)

plt.bar(
    [i + width for i in x],
    adaptive_values,
    width=width,
    label="Adaptive"
)

plt.xticks(
    list(x),
    class_names
)

plt.title("Segmentation Methods by Class")
plt.xlabel("Class")
plt.ylabel("Segmented Area (%)")

plt.legend()

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "class_segmented_comparison.png",
    dpi=300
)

plt.close()


# =========================
# 4. Intensity vs edges
# =========================

plt.figure(figsize=(8, 6))

for class_name in class_names:

    plt.scatter(
        class_data[class_name]["Mean Intensity"],
        class_data[class_name]["Edge Percentage"],
        label=class_name,
        s=100
    )

plt.title("Mean Intensity vs Edge Percentage")
plt.xlabel("Mean Intensity")
plt.ylabel("Edge Percentage (%)")

plt.legend()

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "intensity_vs_edges.png",
    dpi=300
)

plt.close()


# =========================
# Finished
# =========================

print("\nAnalysis completed!")

print("Charts saved in:")
print("results/")