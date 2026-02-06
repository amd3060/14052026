import tkinter as tk
from tkinter import ttk
import heapq
import math
from PIL import Image, ImageTk
class Graph:
    def __init__(self):
        self.adj = {}
    def add_edge(self, u, v, w):
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, []).append((u, w))
    def dijkstra(self, start, end):
        dist = {n: math.inf for n in self.adj}
        prev = {n: None for n in self.adj}
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in self.adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path, dist[end]
def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])
def build_nodes():
    return {
    "P01": (752, 5),
    "P02": (432, 5),
    "P03": (183, 4),
    "P04": (11, 216),
    "P05": (11, 420),
    "P06": (9, 581),
    "P07": (45, 784),
    "P08": (362, 785),
    "P09": (620, 784),
    "P10": (1016, 712),
    "P11": (1022, 534),
    "P12": (1015, 365),
    "P13": (1015, 165),
    "P14": (747, 151),
    "P15": (422, 148),
    "P16": (366, 222),
    "P17": (368, 426),
    "P18": (371, 580),
    "P19": (670, 704),
    "P20": (597, 736),
    "P21": (368, 737),
    "P22": (326, 701),
    "P23": (755, 304),
    "P24": (757, 387),
    "P25": (365, 305),
    "P26": (741, 437),
    "P27": (646, 742),
    "P28": (157, 717),
    }
def build_street_edges():
    return [
        ("P02", "P15"),
        ("P15", "P03"),
        ("P15", "P14"),
        ("P14", "P01"),
        ("P14", "P13"),
        ("P14", "P23"),
        ("P23", "P12"),
        ("P23", "P24"),
        ("P23", "P25"),
        ("P25", "P16"),
        ("P16", "P15"),
        ("P16", "P04"),
        ("P25", "P17"),
        ("P17", "P05"),
        ("P17", "P26"),
        ("P26", "P11"),
        ("P17", "P18"),
        ("P18", "P06"),
        ("P18", "P19"),
        ("P19", "P10"),
        ("P19", "P27"),
        ("P27", "P20"),
        ("P20", "P21"),
        ("P21", "P22"),
        ("P22", "P28"),
        ("P28", "P07"),
        ("P21", "P08"),
        ("P21", "P18"),
        ("P27", "P09"),
        ("P20", "P09"),
    ]
def build_graph(nodes):
    g = Graph()
    for u, v in build_street_edges():
        w = distance(nodes[u], nodes[v])
        g.add_edge(u, v, w)
    return g
class RoutingGUI:
    def __init__(self, root):
        self.root = root
        root.title("Intelligent Routing System - Dijkstra")
        self.map_img = Image.open("map.png")
        self.map_tk = ImageTk.PhotoImage(self.map_img)
        self.nodes = build_nodes()
        self.edges = build_street_edges()
        self.graph = build_graph(self.nodes)
        panel = ttk.Frame(root, padding=10)
        panel.pack(side="left", fill="y")
        ttk.Label(panel, text="Start").pack()
        self.start_cb = ttk.Combobox(panel, values=list(self.nodes.keys()), state="readonly")
        self.start_cb.pack()
        self.start_cb.set("P01")
        ttk.Label(panel, text="End").pack(pady=(10, 0))
        self.end_cb = ttk.Combobox(panel, values=list(self.nodes.keys()), state="readonly")
        self.end_cb.pack()
        self.end_cb.set("P07")
        ttk.Button(panel, text="Find Path", command=self.run).pack(fill="x", pady=10)
        ttk.Button(panel, text="Clear", command=self.clear).pack(fill="x")
        self.info = ttk.Label(panel, text="")
        self.info.pack(pady=10)
        self.canvas = tk.Canvas(
            root,
            width=self.map_img.width,
            height=self.map_img.height
        )
        self.canvas.pack(side="right")
        self.canvas.create_image(0, 0, image=self.map_tk, anchor="nw")
        self.path_lines = []
        self.draw_streets()
        self.draw_nodes()
    def draw_streets(self):
        for u, v in self.edges:
            x1, y1 = self.nodes[u]
            x2, y2 = self.nodes[v]
            self.canvas.create_line(x1, y1, x2, y2, fill="#888", width=2)
    def draw_nodes(self):
        for n, (x, y) in self.nodes.items():
            self.canvas.create_oval(x-6, y-6, x+6, y+6, fill="blue")
            self.canvas.create_text(x, y-12, text=n, font=("Tahoma", 9, "bold"))
    def clear(self):
        for l in self.path_lines:
            self.canvas.delete(l)
        self.path_lines.clear()
        self.info.config(text="")
    def run(self):
        self.clear()
        s = self.start_cb.get()
        e = self.end_cb.get()
        path, dist = self.graph.dijkstra(s, e)
        for i in range(len(path) - 1):
            x1, y1 = self.nodes[path[i]]
            x2, y2 = self.nodes[path[i + 1]]
            self.path_lines.append(
                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=4)
            )

        self.info.config(
            text=f"Path: {' -> '.join(path)}\nDistance: {dist:.1f}"
        )
if __name__ == "__main__":
    root = tk.Tk()
    app = RoutingGUI(root)
    root.mainloop()