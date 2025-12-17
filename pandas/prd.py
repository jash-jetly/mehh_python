import pandas as pd

dafr = pd.read_csv("prd.csv")
dafr["price"] = pd.to_numeric(dafr["price"].astype(str).str.replace(",", "", regex=False), errors="coerce")
spr = dafr.loc[(dafr["price"] >= 10000) & (dafr["price"] <= 50000)]
print(spr)
