
import pandas as pd
from pathlib import Path
from scipy.sparse import coo_matrix, save_npz
from sklearn.preprocessing import normalize

# Membaca data training
df = pd.read_csv("data/P1.csv")

# Membuat indeks angka untuk setiap Visitor dan Item
visitor_codes, visitor_ids = pd.factorize(df["visitorid"])
item_codes, item_ids = pd.factorize(df["itemid"])

# Membuat matriks sparse Visitor x Item
vsm = coo_matrix(
    (
        [1] * len(df),
        (visitor_codes, item_codes)
    ),
    shape=(len(visitor_ids), len(item_ids)),
    dtype="int32"
).tocsr()

# Menggabungkan interaksi berulang pada pasangan Visitor-Item
vsm.sum_duplicates()

# Normalisasi untuk perhitungan kemiripan
vsm_normalized = normalize(vsm, norm="l2", axis=1)

# Menyimpan hasil
Path("data").mkdir(exist_ok=True)
save_npz("data/vsm_visitor_item_P1.npz", vsm)
save_npz("data/vsm_visitor_item_P1_normalized.npz", vsm_normalized)

pd.Series(visitor_ids, name="visitorid").to_csv(
    "data/vsm_visitor_ids_P1.csv", index=False
)
pd.Series(item_ids, name="itemid").to_csv(
    "data/vsm_item_ids_P1.csv", index=False
)

print("Ukuran matriks VSM:", vsm.shape)
print("Jumlah sel terisi:", vsm.nnz)
print("Jumlah Visitor:", len(visitor_ids))
print("Jumlah Item:", len(item_ids))
print("VSM sparse berhasil disimpan.")
