import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# Smuggling log data
data = [
    ("ADGA", "Temple", "Shipping Yard", 1.5, "Stack of photos in rubber band"),
    ("AFDG", "Customs Outpost", "Transit Hub", 1.0, "Empty tin labeled 'sardines'"),
    ("AFAF", "Transit Hub", "Port", 0.5, "Hollow pendant"),
    ("AFX", "Transit Hub", "Storage House", 2.1, "Boot pocket"),
    ("AGFX", "Shipping Yard", "Customs Outpost", 2.1, "Velvet-lined walnut case"),
    ("AGF", "Shipping Yard", "Port", 4.6, "Canvas sack marked 'tools'"),
    ("AXAD", "Customs Outpost", "Transit Hub", 2.6, "Small carved box with foam lining (2.5 oz)"),
    ("DAGG", "Storage House", "Shipping Yard", 2.1, "Boot pocket"),
    ("DGAF", "Zolo's Camp", "Customs Outpost", 10.0, "Matchsticks (10)"),
    ("DGFX", "Customs Outpost", "Transit Hub", 2.5, "Small carved box with foam lining (2.5 oz)"),
    ("FAXX", "Customs Outpost", "Temple", 9.0, "Stack of newspapers"),
    ("FDFA", "Jungle", "Shipping Yard", 1.6, "Slim harmonica in cloth"),
    ("FXDF", "Transit Hub", "Port", 1.5, "Stack of photos in rubber band"),
    ("FXXD", "Customs Outpost", "Transit Hub", 2.5, "Small carved box with foam lining (2.5 oz)"),
    ("FADX", "Transit Hub", "Port", 1.5, "Packet of chewing gum sleeves"),
    ("FFDF", "Temple", "Shipping Yard", 1.5, "Packet of chewing gum sleeves"),
    ("FGD", "Jungle", "Temple", 7.2, "Wrapped in banana leaves"),
    ("FXA", "Temple", "Zolo's Camp", 3.2, "Miniature bust in plaster"),
    ("GAFX", "Zolo's Camp", "Jungle", 6.7, "Rolled hammock wrapped in netting"),
    ("GXFD", "Transit Hub", "Port", 1.5, "Box of crickets"),
    ("GXXF", "Temple", "Zolo's Camp", 10.0, "Paper clips (10, individual)"),
    ("XADX", "Zolo's Camp", "Customs Outpost", 5.5, "Sealed coffee canister"),
    ("XFGA", "Port", "Zolo's Camp", 9.0, "Coffee beans boxes"),
    ("XXFA", "Transit Hub", "Port", 1.5, "Packet of chewing gum sleeves")
]

# Create DataFrame
df = pd.DataFrame(data, columns=['ID', 'Source', 'Dest', 'Weight', 'Description'])

# Create directed graph
G = nx.DiGraph()

# Add edges with weights and descriptions
for _, row in df.iterrows():
    G.add_edge(row['Source'], row['Dest'], 
               weight=row['Weight'], 
               id=row['ID'],
               description=row['Description'])

# Create visualization
plt.figure(figsize=(16, 12))

# Use spring layout for better visualization
pos = nx.spring_layout(G, k=3, iterations=50, seed=42)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                      node_size=2000, alpha=0.8)

# Draw edges with different colors for different weights
edge_colors = []
edge_widths = []
for u, v, d in G.edges(data=True):
    weight = d['weight']
    if weight > 7:
        edge_colors.append('red')
        edge_widths.append(3)
    elif weight > 4:
        edge_colors.append('orange')
        edge_widths.append(2.5)
    elif weight > 2:
        edge_colors.append('yellow')
        edge_widths.append(2)
    else:
        edge_colors.append('green')
        edge_widths.append(1.5)

nx.draw_networkx_edges(G, pos, edge_color=edge_colors, 
                      width=edge_widths, alpha=0.7, arrows=True, 
                      arrowsize=20, arrowstyle='->')

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

# Add edge labels with IDs and weights
edge_labels = {}
for u, v, d in G.edges(data=True):
    edge_labels[(u, v)] = f"{d['id']}\n{d['weight']}oz"

nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

plt.title("Smuggling Network Analysis\n(Edge thickness/color indicates weight: Green<2oz, Yellow 2-4oz, Orange 4-7oz, Red>7oz)", 
          fontsize=14, fontweight='bold')

# Color legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='green', label='Light (< 2 oz)'),
    Patch(facecolor='yellow', label='Medium (2-4 oz)'),
    Patch(facecolor='orange', label='Heavy (4-7 oz)'),
    Patch(facecolor='red', label='Very Heavy (> 7 oz)')
]
plt.legend(handles=legend_elements, loc='upper right')

plt.axis('off')
plt.tight_layout()
plt.savefig('smuggling_network.png', dpi=300, bbox_inches='tight')
plt.show()

print("=== NETWORK ANALYSIS ===")
print(f"Total locations: {G.number_of_nodes()}")
print(f"Total shipments: {G.number_of_edges()}")

print("\n=== ROUTES FROM PORT ===")
# Find all outgoing routes from Port
port_routes = [(u, v, d) for u, v, d in G.edges(data=True) if u == 'Port']
print(f"Shipments FROM Port: {len(port_routes)}")
for u, v, d in port_routes:
    print(f"  {d['id']}: Port → {v} ({d['weight']}oz) - {d['description']}")

print("\n=== ROUTES TO PORT ===")
# Find all incoming routes to Port
to_port_routes = [(u, v, d) for u, v, d in G.edges(data=True) if v == 'Port']
print(f"Shipments TO Port: {len(to_port_routes)}")
for u, v, d in to_port_routes:
    print(f"  {d['id']}: {u} → Port ({d['weight']}oz) - {d['description']}")

print("\n=== SUSPICIOUS ITEMS (Potential Emerald Containers) ===")
# Look for hollow/container items that could hide an emerald
suspicious_keywords = ['hollow', 'box', 'case', 'canister', 'tin', 'sack', 'pocket']
suspicious_items = []

for _, row in df.iterrows():
    desc_lower = row['Description'].lower()
    if any(keyword in desc_lower for keyword in suspicious_keywords):
        suspicious_items.append(row)
        
for item in suspicious_items:
    print(f"  {item['ID']}: {item['Source']} → {item['Dest']} ({item['Weight']}oz) - {item['Description']}")

print("\n=== WEIGHT ANALYSIS ===")
# Analyze weight patterns
weights = df['Weight'].tolist()
avg_weight = sum(weights) / len(weights)
print(f"Average shipment weight: {avg_weight:.2f}oz")

# Find unusually heavy or light items
light_items = df[df['Weight'] < 1.0]
heavy_items = df[df['Weight'] > 8.0]

print(f"\nUnusually light items (< 1oz): {len(light_items)}")
for _, item in light_items.iterrows():
    print(f"  {item['ID']}: {item['Description']} ({item['Weight']}oz)")

print(f"\nUnusually heavy items (> 8oz): {len(heavy_items)}")
for _, item in heavy_items.iterrows():
    print(f"  {item['ID']}: {item['Description']} ({item['Weight']}oz)")