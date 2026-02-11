# Assignment 2, Filip Drincic, LTU 2026,Industrial AI and eMaintenance - Part I: Theories & Concepts
# The Python program use load and time-to-failure data from three manufacturers (A, B, and C) to provide statistical and distribution-based methods.
import pandas as pd
import matplotlib.pyplot as plt


# Read and clean data
df = pd.read_csv("machine_data.csv")
df = df.drop(columns=["Unnamed: 0"])

# Group by manufacturer
groups = df.groupby("manufacturef")

for manu, g in groups:
    print(f"\nManufacturer {manu}")

    # Load statistics
    print("Load range:", g["load"].min(), "-", g["load"].max())
    print("Mean load:", g["load"].mean())
    print("Median load:", g["load"].median())
    print("Mode load:", g["load"].mode().iloc[0])
    print("Load variance:", g["load"].var())
    print("Load std deviation:", g["load"].std())

    # Time statistics
    print("Time range:", g["time"].min(), "-", g["time"].max())
    print("Mean time:", g["time"].mean())
    print("Median time:", g["time"].median())
    print("Time variance:", g["time"].var())
    print("Time std deviation:", g["time"].std())

    # Relationship
    print("Correlation (load vs time):", g["load"].corr(g["time"]))



    # Scatter plot
    plt.figure(figsize=(6,4))
    plt.scatter(g["load"], g["time"], alpha=0.7)
    plt.title(f"Load vs Time - Manufacturer {manu}")
    plt.xlabel("Load")
    plt.ylabel("Time to Failure")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Histograms
    g["load"].plot(kind="hist", bins=10, title=f"Load Distribution - {manu}")
    plt.show()

    g["time"].plot(kind="hist", bins=10, title=f"Time Distribution - {manu}")
    plt.show()
