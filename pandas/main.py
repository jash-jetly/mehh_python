import pandas as pd


data = {
'date': ['12/6/2025', '12/5/25'],
'category': ['vadav', 'taxi'],
'amount': [100, 200]
}
new_exp={
        "date": "12/7/25",
        'category': 'g stand',
        'amount': 80
}
df = pd.DataFrame(data)

new_exp_df = pd.DataFrame([new_exp])

df = pd.concat([df, new_exp_df], ignore_index=True)

ta = df['amount'].sum()
print(df)
print(f"TA: {ta}")

print(df.loc[0])

