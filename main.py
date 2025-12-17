import pandas as pd


data = {
'id': [1, 2, 3, 4, 5],
      'number': [10, 20, 30, 40, 50],
      'purchase': ['yes', 'no', 'yes', 'no', 'yes']
}
df = pd.DataFrame(data)
print(df)
