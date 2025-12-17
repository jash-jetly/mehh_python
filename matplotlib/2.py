import matplotlib.pyplot as plt
import numpy as np

# Engineers have a relatively fixed salary (small standard deviation)
engineers_salaries = np.random.normal(loc=80000, scale=3000, size=150)

# Sales have commission-based salaries, implying wider variation (larger standard deviation)
sales_salaries = np.random.normal(loc=70000, scale=25000, size=180)

data_to_plot = [engineers_salaries, sales_salaries]

plt.boxplot(data_to_plot)

plt.title('Salary Distribution: Engineers vs. Sales', fontsize=16, color='darkblue')
plt.xlabel('Department', fontsize=12, color='darkgreen')
plt.ylabel('Annual Salary (USD)', fontsize=12, color='darkred')

plt.xticks([1, 2], ['Engineers', 'Sales'])

plt.grid(True, linestyle=':', alpha=0.6)

plt.show()

