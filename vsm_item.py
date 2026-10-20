
import pandas as pd
from scipy.sparse import load_npz, save_npz
from sklearn.preprocessing import normalize

# VSM Visitor: baris = Visitor, kolom = Item
vsm_visitor = load_npz("data/vsm_visitor_item_P1.npz")

# Transpose: baris = Item, kolom = Visitor
vsm_item = vsm_visitor.T.tocsr()
vsm_item_normalized = normalize(vsm_item, norm="l2", axis=1)

visitor_ids = pd.read_csv("data/vsm_visitor_ids_P1.csv")["visitorid"]
item_ids = pd.read_csv("data/vsm_item_ids_P1.csv")["itemid"]

save_npz("data/vsm_item_P1.npz", vsm_item)
save_npz("data/vsm_item_P1_normalized.npz", vsm_item_normalized)

print("VSM Visitor shape:", vsm_visitor.shape)
print("VSM Item shape:", vsm_item.shape)
print("Visitor:", len(visitor_ids))
print("Item:", len(item_ids))
print("Jumlah pasangan Visitor-Item:", vsm_visitor.nnz)
print("Jumlah sel terisi VSM Item:", vsm_item.nnz)
print("VSM Item berhasil disimpan.")
