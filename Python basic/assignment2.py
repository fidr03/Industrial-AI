import pandas as pd
import matplotlib.pyplot as plt
import pandas
import numpy
import matplotlib
import scipy
print("All good!")


# Read and clean data
df = pd.read_csv("machine_data.csv")
df = df.drop(columns=["Unnamed: 0"])

# Group by manufacturer
groups = df.groupby("manufacturef")

for manu, g in groups:
    print(f"\nManufacturer {manu}")
    print("Load range:", g["load"].min(), "-", g["load"].max())
    print("Time range:", g["time"].min(), "-", g["time"].max())
    print("Mean load:", g["load"].mean())
    print("Mean time:", g["time"].mean())
    print("Correlation:", g["load"].corr(g["time"]))

    # Scatter plot
    plt.figure()
    plt.scatter(g["load"], g["time"])
    plt.title(f"Load vs Time – Manufacturer {manu}")
    plt.xlabel("Load")
    plt.ylabel("Time")
    plt.show()

    # Histograms
    g["load"].plot(kind="hist", bins=10, title=f"Load Distribution – {manu}")
    plt.show()

    g["time"].plot(kind="hist", bins=10, title=f"Time Distribution – {manu}")
    plt.show()
