import math
import networkx as nx


def layout(ug, components, frame, c):
    positions = {}
    large = [s for s in components if len(s) > c['layout_small_component']]
    small = [s for s in components if len(s) <= c['layout_small_component']]
    for i, part in enumerate(large):
        pos = nx.spring_layout(ug.subgraph(sorted(part)), seed=c['random_seed'], iterations=c['layout_iterations'], weight=None)
        radius = min(600, 850 / max(1, len(large)))
        for v, xy in pos.items():
            positions[v] = (float(xy[0]) * radius - 300, float(xy[1]) * radius + (i - (len(large)-1)/2) * 2 * radius)
    columns = max(1, math.ceil(math.sqrt(len(small))))
    for i, part in enumerate(small):
        cx, cy = 600 + (i % columns) * 100, (i // columns) * 100
        for j, v in enumerate(sorted(part)):
            angle = 2 * math.pi * j / len(part)
            positions[v] = (cx + 30 * math.cos(angle), cy + 30 * math.sin(angle))
    for axis, name in enumerate(('x', 'y')):
        vals = [positions[v][axis] for v in frame.gid]
        lo, hi = min(vals), max(vals)
        frame[name] = [round(2000 * (x-lo)/(hi-lo)-1000, 6) if hi > lo else 0.0 for x in vals]
    return frame
