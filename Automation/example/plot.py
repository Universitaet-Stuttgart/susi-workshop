import matplotlib.pyplot as plt
from numpy import genfromtxt

data = genfromtxt("plot_data.csv", delimiter=",", names=True)

plt.plot(data["arc_length"], data["function"], label="function")
plt.xlabel("arc_length")
plt.ylabel("function")
plt.savefig("function_plot.pdf", bbox_inches="tight")
