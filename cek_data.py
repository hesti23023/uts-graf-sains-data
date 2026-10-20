
import pandas as pd
from pathlib import Path

for nama in ["P1.csv", "P2.csv"]:
    file_csv = Path("data") / nama
    df = pd.read_csv(file_csv)

    print(f"\n=== {nama} ===")
    print("Jumlah baris:", len(df))
    print("Kolom:", list(df.columns))
    print("Jenis interaksi:")
    print(df["event"].value_counts().to_string())
    print("Jumlah user unik:", df["visitorid"].nunique())
    print("Jumlah item unik:", df["itemid"].nunique())
    print("Jumlah transactionid terisi:", df["transactionid"].notna().sum())
