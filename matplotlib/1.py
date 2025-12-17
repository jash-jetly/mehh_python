import matplotlib.pyplot as plt


scores=[30,25,15,50,6]
i = [25, 60, 12, 56, 78]
hrs=[30, 10, 4, 5, 9]

plt.scatter(scores, hrs, color='green', s=100, label='mehhh')
plt.scatter(i, hrs, color='red', s=100, label='fuckk')
plt.grid(True)
plt.legend()
plt.show()
