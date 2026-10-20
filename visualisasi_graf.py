
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Ambil data training
df = pd.read_csv("data/P1.csv")

# Batasi contoh agar visualisasi mudah dibaca
sample = df[df["event"] == "view"].head(100)

# Buat graf bipartit Visitor-Item
G = nx.Graph()

for row in sample.itertuples(index=False):
    visitor = f"V{row.visitorid}"
    item = f"I{row.itemid}"

    G.add_node(visitor, node_type="Visitor")
    G.add_node(item, node_type="Item")
    G.add_edge(visitor, item)

# Pisahkan posisi node Visitor dan Item
visitors = [
    n for n, d in G.nodes(data=True)
    if d["node_type"] == "Visitor"
]
items = [
    n for n, d in G.nodes(data=True)
    if d["node_type"] == "Item"
]

pos = {}
pos.update(nx.bipartite_layout(G, visitors))

plt.figure(figsize=(14, 9))
nx.draw_networkx(
    G,
    pos=pos,
    with_labels=False,
    node_size=35,
    width=0.5
)

plt.title("Graf Bipartit Visitor-Item (Sampel 100 Aktivitas VIEWED P1)")
plt.axis("off")
plt.tight_layout()
plt.savefig("data/graf_p1.png", dpi=200)
plt.show()

print("Jumlah node pada graf sampel:", G.number_of_nodes())
print("Jumlah edge pada graf sampel:", G.number_of_edges())
print("Visualisasi tersimpan di data/graf_p1.png")
