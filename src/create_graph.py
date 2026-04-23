
import matplotlib.pyplot as plt
X = [0.05*x for x in range(1, 21)]

Y_0_9 = [72645, 787895, 316265, 115240, 98525, 46865, 37830, 34705, 34165, 33240, 32265, 31040, 31280, 30925, 30865,
         30685, 30705, 30290, 30875, 30510]
Y_0_3 = [96140, 527085, 247930, 74255, 79350, 41885, 36880, 34680, 33990, 33580, 32510, 32300, 32135, 31455, 31475,
         31910, 31105, 31030, 31200, 31220]

plt.figure(figsize=(10, 6))
plt.plot(X, Y_0_9, label="Inter. prob.=0.9")
# plt.plot(X, Y_0_3, label="Inter. prob.=0.3")
plt.title("Average Steps to Convergence vs Confidence Threshold")
plt.xlabel("Confidence Threshold")
plt.ylabel("Average Steps to Convergence")
# plt.legend()
plt.grid()
plt.savefig("prueba.png")
plt.close()