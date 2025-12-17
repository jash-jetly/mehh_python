import pandas as pd

df = pd.read_csv('students.csv')
print("First 5 rows:")
print(df.head())
print("\nLast 5 rows:")
print(df.tail())
print("\nDataframe info:")
print(df.info())
print("\nDescriptive statistics:")
print(df.describe())

