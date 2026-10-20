
# import pandas as pd
# import math

# # 1. Baca data P2 dan hasil rekomendasi
# p2 = pd.read_csv("data/P2.csv")
# recommendations = pd.read_csv(
#     "data/rekomendasi_visitor_53842.csv"
# )

# target_id = 53842
# k = 5

# # 2. Ambil maksimal 5 item rekomendasi sesuai urutan
# recommended = recommendations["itemid"].head(k).tolist()

# # 3. Ambil item yang diinteraksikan Visitor pada P2
# actual_p2 = set(
#     p2.loc[p2["visitorid"] == target_id, "itemid"]
# )

# # 4. Tandai apakah tiap rekomendasi cocok dengan P2
# relevance = [
#     1 if item in actual_p2 else 0
#     for item in recommended
# ]

# # 5. Hit@5: 1 jika ada minimal satu item yang cocok
# hit_at_5 = 1.0 if sum(relevance) > 0 else 0.0

# # 6. DCG@5
# dcg = sum(
#     rel / math.log2(rank + 2)
#     for rank, rel in enumerate(relevance)
# )

# # 7. IDCG@5: nilai ideal berdasarkan jumlah item relevan
# ideal_relevance = sorted(relevance, reverse=True)
# idcg = sum(
#     rel / math.log2(rank + 2)
#     for rank, rel in enumerate(ideal_relevance)
# )

# ndcg_at_5 = dcg / idcg if idcg > 0 else 0.0

# # 8. Tampilkan hasil evaluasi
# print("Visitor target:", target_id)
# print("Jumlah item yang diinteraksikan pada P2:", len(actual_p2))
# print("Daftar rekomendasi:", recommended)
# print("Relevansi tiap rekomendasi:", relevance)
# print("Jumlah rekomendasi yang cocok:", sum(relevance))
# print(f"Hit@5: {hit_at_5:.4f}")
# print(f"NDCG@5: {ndcg_at_5:.4f}")



import pandas as pd
import math

p2 = pd.read_csv("data/P2.csv")
recommendations = pd.read_csv("data/rekomendasi.csv")
target_id = int(open("data/target_visitor.txt").read().strip())
k = 5

# Item yang benar-benar muncul untuk Visitor target pada P2
actual_items = set(p2.loc[p2.visitorid == target_id, "itemid"])
recommended = recommendations["itemid"].head(k).tolist()

# 1 jika item rekomendasi ada pada P2, selain itu 0
relevance = [int(item in actual_items) for item in recommended]

# Hit@5: apakah setidaknya satu rekomendasi relevan?
hit_at_5 = float(sum(relevance) > 0)

# DCG@5: memperhitungkan posisi item relevan
dcg = sum(
    rel / math.log2(rank + 2)
    for rank, rel in enumerate(relevance)
)

# Ideal DCG memakai jumlah item relevan di seluruh P2,
# dibatasi sampai k=5
ideal_count = min(len(actual_items), k)
idcg = sum(1 / math.log2(rank + 2) for rank in range(ideal_count))

ndcg_at_5 = dcg / idcg if idcg > 0 else 0.0

print("Visitor target:", target_id)
print("Jumlah item aktual pada P2:", len(actual_items))
print("Item rekomendasi:", recommended)
print("Relevance:", relevance)
print(f"Hit@5: {hit_at_5:.4f}")
print(f"NDCG@5: {ndcg_at_5:.4f}")
