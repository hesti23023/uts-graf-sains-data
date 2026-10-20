
import pandas as pd
from pathlib import Path

# Lokasi dataset asli
input_file = Path("data/events.csv")

# Buat folder data jika belum ada
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

# Periode P1: 9–14 Mei 2015
p1_start = 1431129600000
p1_end = 1431648000000

# Periode P2: 15–20 Mei 2015
p2_start = 1431648000000
p2_end = 1432166400000

# Baca dataset
df = pd.read_csv(input_file)

# Filter berdasarkan timestamp
p1 = df[(df["timestamp"] >= p1_start) &
        (df["timestamp"] < p1_end)].copy()

p2 = df[(df["timestamp"] >= p2_start) &
        (df["timestamp"] < p2_end)].copy()

# Simpan hasil filter
p1.to_csv(output_dir / "P1.csv", index=False)
p2.to_csv(output_dir / "P2.csv", index=False)

# Tampilkan ringkasan
print("Jumlah data P1:", len(p1))
print("Jumlah data P2:", len(p2))
print("File tersimpan di folder data.")
