
import pandas as pd
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity

vsm = load_npz("data/vsm_visitor_item_P1_normalized.npz")
visitor_ids = pd.read_csv("data/vsm_visitor_ids_P1.csv")["visitorid"]
target_id = int(open("data/target_visitor.txt").read().strip())

target_index = visitor_ids[visitor_ids == target_id].index[0]
scores = cosine_similarity(vsm[target_index], vsm).ravel()
scores[target_index] = -1

# Hitung jumlah tetangga dengan similarity positif
jumlah_positif = int((scores > 0).sum())
print("Visitor target:", target_id)
print("Jumlah tetangga dengan similarity positif:", jumlah_positif)

# Ambil maksimal 5 tetangga, tanpa mengharuskan similarity positif
# jika jumlah tetangga positif kurang dari 5.
top_indices = scores.argsort()[::-1][:5]

hasil = pd.DataFrame({
    "visitorId": visitor_ids.iloc[top_indices].values,
    "similarity": scores[top_indices]
})

hasil.to_csv("data/top5_similarity.csv", index=False)

print("\nTop 5 tetangga:")
print(hasil.to_string(index=False))
print("\nHasil tersimpan di data/top5_similarity.csv")
