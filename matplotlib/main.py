import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
df = pd.read_csv('~/python/matplotlib/fertility.csv')

# Extract the 'age' column
age_data = df['Age']

# Plot the histogram of the 'age' column
plt.hist(age_data, bins=10, edgecolor="black", color="green")
plt.title("Distribution of Age")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

