
import pandas as pd

p1 = pd.read_csv("data/P1.csv")
neighbors = pd.read_csv("data/top5_similarity.csv")
target_id = int(open("data/target_visitor.txt").read().strip())

# Hanya gunakan tetangga dengan similarity positif
neighbors = neighbors[neighbors["similarity"] > 0].copy()

# Item yang sudah pernah diinteraksikan target tidak direkomendasikan
items_target = set(
    p1.loc[p1["visitorid"] == target_id, "itemid"]
)

events = p1[
    p1["visitorid"].isin(neighbors["visitorId"])
].copy()

events = events[~events["itemid"].isin(items_target)]
events = events.merge(
    neighbors,
    left_on="visitorid",
    right_on="visitorId",
    how="inner"
)

recommendations = (
    events.groupby("itemid")
    .agg(
        skor_rekomendasi=("similarity", "sum"),
        jumlah_tetangga=("visitorid", "nunique"),
        jumlah_interaksi=("event", "count")
    )
    .reset_index()
    .sort_values(
        ["skor_rekomendasi", "jumlah_tetangga", "jumlah_interaksi"],
        ascending=False
    )
    .head(3)
    .reset_index(drop=True)
)

recommendations.to_csv("data/rekomendasi.csv", index=False)

print("Visitor target:", target_id)
print("Jumlah tetangga positif:", len(neighbors))
print("\n3 rekomendasi item:")
print(recommendations.to_string(index=False))
print("\nHasil tersimpan di data/rekomendasi.csv")
