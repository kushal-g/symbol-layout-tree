import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def _cross2d(o, u, v):
    return (u[0]-o[0])*(v[1]-o[1]) - (u[1]-o[1])*(v[0]-o[0])

def segments_cross(a, b, c, d):
    if a == c or a == d or b == c or b == d:
        return False
    return (_cross2d(c,d,a) * _cross2d(c,d,b) < 0 and
            _cross2d(a,b,c) * _cross2d(a,b,d) < 0)

nodes = {
    'A': (0, 2), 'B': (2, 3), 'C': (4, 2),
    'D': (2, 0), 'E': (2, 2), 'F': (3, 3)
}
edges = [('E','F'), ('B','C'), ('C','D'), ('D','A'), ('A','E'), ('B','E'), ('C','E'), ('D','E')]

# For each crossing pair, bend the two edges in opposite directions
curvatures = [0.0] * len(edges)
for i in range(len(edges)):
    for j in range(i+1, len(edges)):
        u1, v1 = edges[i]
        u2, v2 = edges[j]
        if segments_cross(nodes[u1], nodes[v1], nodes[u2], nodes[v2]):
            curvatures[i] = 0.3
            curvatures[j] = -0.3

fig, ax = plt.subplots(figsize=(8, 7))

for (u, v), rad in zip(edges, curvatures):
    ax.annotate("", xy=nodes[v], xytext=nodes[u],
                arrowprops=dict(
                    arrowstyle="-",
                    connectionstyle=f"arc3,rad={rad}",
                    color='#444',
                    lw=1.5,
                    shrinkA=14, shrinkB=14,
                ))

for name, (x, y) in nodes.items():
    ax.scatter(x, y, s=900, c='#a8d8ea', zorder=5, linewidths=1.5, edgecolors='#555')
    ax.text(x, y, name, ha='center', va='center', zorder=6, fontsize=12, fontweight='bold')

ax.set_aspect('equal')
ax.axis('off')
ax.set_xlim(-0.6, 4.6)
ax.set_ylim(-0.6, 3.8)
plt.tight_layout()
plt.savefig('graph_fixed.png', dpi=120, bbox_inches='tight')
print('Wrote graph_fixed.png')
