
# import pandas as pd
# import random

# p1 = pd.read_csv("data/P1.csv")
# p2 = pd.read_csv("data/P2.csv")

# # Pilih Visitor yang muncul di kedua periode
# visitor_p1 = set(p1["visitorid"].unique())
# visitor_p2 = set(p2["visitorid"].unique())
# kandidat = sorted(visitor_p1 & visitor_p2)

# # Seed membuat hasil pemilihan bisa diulang
# seed = 42
# rng = random.Random(seed)
# target_id = rng.choice(kandidat)

# with open("data/target_visitor.txt", "w") as f:
#     f.write(str(target_id))

# print("Seed:", seed)
# print("Jumlah kandidat Visitor:", len(kandidat))
# print("Visitor terpilih:", target_id)
# print("ID disimpan di data/target_visitor.txt")


import pandas as pd
import random
from scipy.sparse import load_npz

p1 = pd.read_csv("data/P1.csv")
p2 = pd.read_csv("data/P2.csv")

visitor_ids = pd.read_csv("data/vsm_visitor_ids_P1.csv")["visitorid"]
vsm = load_npz("data/vsm_visitor_item_P1.npz")

# Cari Visitor yang ada di P1 dan P2
# serta memiliki setidaknya satu item yang sama
visitor_p2 = set(p2["visitorid"].unique())
kandidat = []

for i, visitor_id in enumerate(visitor_ids):
    if visitor_id not in visitor_p2:
        continue

    # Harus memiliki item yang beririsan dengan Visitor lain
    kemiripan = vsm[i].multiply(vsm).getnnz(axis=1)
    kemiripan[i] = 0

    if kemiripan.max() > 0:
        kandidat.append(visitor_id)

# Pilih secara acak, tetapi hasilnya bisa diulang
rng = random.Random(42)
target_id = rng.choice(kandidat)

with open("data/target_visitor.txt", "w") as f:
    f.write(str(target_id))

print("Jumlah kandidat yang bisa dibandingkan:", len(kandidat))
print("Visitor terpilih:", target_id)
print("Target berhasil disimpan.")
