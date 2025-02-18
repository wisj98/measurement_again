import pandas as pd

df = pd.read_csv("data/ingredients.csv")

invalid_rows = df[df["현재량(kg)"] <= 0]
for index, row in invalid_rows.iterrows():
    ingredient_name = row["원료명"]
    amount = row["현재량(kg)"]

    target_row = df[(df["원료명"] == ingredient_name) & (df["현재량(kg)"] > 0)].sort_values("유통기한").head(1)

    if not target_row.empty:
        target_index = target_row.index[0]
        df.at[target_index, "현재량(kg)"] += amount

    df.drop(index, inplace=True)
print(df)