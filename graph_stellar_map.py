"""
Destiny 2 - Sol Sector Graph
Shortest path finder using Dijkstra's algorithm
Interactive visualization with highlighted path
"""
import tkinter as tk
from tkinter import ttk, messagebox
import math
import heapq
import random

#graph data (my pain and suffering) 
EDGES_RAW = [
    ["earth", "tower", "edz", "cosmodrome"],
    ["tower", "courtyard"],
    ["tower", "annex"],
    ["annex", "bazaar"],
    ["bazaar", "courtyard"],
    ["courtyard", "hangar", "bazaar", "quest_archive", "Postmaster", "tess_everis",
     "ironwood_tree", "zavala", "lord_shaxx", "valus_saladin", "monument_to_lost_lights",
     "monument_to_season_past", "banshee-44", "vault", "master_rahool",
     "special_deliveries_terminal"],
    ["hangar", "saint-14"],
    ["bazaar", "annex", "suraya_hawthorne", "xur", "ikora_rey"],
    ["annex", "the_drifter", "ada-1", "loom"],
    ["cosmodrome", "the_steppes"],
    ["cosmodrome", "skywatch"],
    ["the_steppes", "shaw_han", "mothyards", "dock_13"],
    ["dock_13", "the_divide"],
    ["the_divide", "exodus_garden_2a", "the_breach", "gateway"],
    ["mothyards", "lunar_complex", "forgotten_shore"],
    ["lunar_complex", "skywatch"],
    ["skywatch", "lunar_complex", "jovian_complex", "terrestrial_complex", "grasp_of_avarice"],
    ["terrestrial_complex", "forgotten_shore"],
    ["forgotten_shore", "the_disgraced", "fallen_s.a.b.e.r", "the_devils'lair", "veles_labyrinth"],
    ["edz", "trostland", "the_sludge", "the_gulch", "winding_cove", "sunken_isles"],
    ["trostland", "devrim_kay", "terminus_east", "atrium", "widow's_walk", "salt_mines",
     "maevic_square", "outskirts"],
    ["maevic_square", "warlord's_ruin", "the_reservoir"],
    ["the_reservoir", "lake_of_shadows"],
    ["outskirts", "scavenger's_den", "the_drain", "whispered_falls", "sojurner's_camp",
     "winding_cove", "the_sludge", "trostland"],
    ["the_sludge", "shaft_13", "cavern_of_souls", "hallowed_grove", "the_dark_forest",
     "the_gulch", "outskirts"],
    ["the_gulch", "flooded_chasm", "the_sludge", "firebase_hades", "the_tunnels"],
    ["firebase_hades", "excavation_site_12", "pathfinder's_crash", "the_pit",
     "the_arms_dealer", "legion's_anchor", "the_gulch", "winding_cove"],
    ["sunken_isles", "the_quarry", "skydock_4", "echion_hold", "echion_batlledeck",
     "echion_control"],
    ["winding_cove", "the_weep", "firebase_hades", "outskirts"],
]

# Node categories  (important to not confuse EVERYONE)
HUBS     = {"earth", "tower", "courtyard", "hangar", "annex", "bazaar"}

PATROLS  = {"edz", "cosmodrome", "trostland", "the_sludge", "the_gulch",
             "winding_cove", "sunken_isles", "the_steppes", "skywatch",
             "mothyards", "dock_13", "the_divide", "forgotten_shore",
             "lunar_complex", "terrestrial_complex", "outskirts",
             "maevic_square", "the_reservoir", "firebase_hades"}

VENDORS  = {"zavala", "lord_shaxx", "banshee-44", "master_rahool", "tess_everis",
             "ikora_rey", "xur", "suraya_hawthorne", "the_drifter", "ada-1",
             "saint-14", "valus_saladin", "shaw_han", "devrim_kay", "Postmaster",
             "special_deliveries_terminal", "quest_archive", "vault", "loom",
             "ironwood_tree", "monument_to_lost_lights", "monument_to_season_past"}

ACTIVITIES = {"exodus_garden_2a", "grasp_of_avarice", "lake_of_shadows",
               "the_disgraced", "fallen_s.a.b.e.r", "the_devils'lair",
               "veles_labyrinth", "warlord's_ruin", "shaft_13", "hallowed_grove",
               "the_dark_forest", "flooded_chasm", "the_tunnels", "the_arms_dealer",
               "excavation_site_12", "pathfinder's_crash", "the_pit", "legion's_anchor",
               "the_quarry", "skydock_4", "echion_hold", "echion_batlledeck",
               "echion_control", "scavenger's_den", "the_drain", "whispered_falls",
               "sojurner's_camp", "the_weep", "jovian_complex", "cavern_of_souls",
               "atrium", "terminus_east", "widow's_walk", "salt_mines",
               "the_breach", "gateway"}

COLORS = {
    "hub":      "#7F77DD",
    "patrol":   "#1D9E75",
    "vendor":   "#378ADD",
    "activity": "#D85A30",
    "default":  "#888780",
}

def node_color(nid):
    if nid in HUBS:      return COLORS["hub"]
    if nid in VENDORS:   return COLORS["vendor"]
    if nid in ACTIVITIES:return COLORS["activity"]
    if nid in PATROLS:   return COLORS["patrol"]
    return COLORS["default"]

def node_radius(nid):
    if nid in HUBS:   return 10
    if nid in PATROLS:return 8
    return 6

# this is to Build the adjacencys list 

def build_graph():
    graph = {}
    edge_set = set()

    def add_edge(a, b):
        key = tuple(sorted([a, b]))
        if key not in edge_set:
            edge_set.add(key)
            graph.setdefault(a, set()).add(b)
            graph.setdefault(b, set()).add(a)

    for row in EDGES_RAW:
        src = row[0]
        for tgt in row[1:]:
            add_edge(src, tgt)

    all_nodes = set(graph.keys())
    return graph, all_nodes, edge_set

#  Dijkstra beacause i can

def dijkstra(graph, start, end):
    """Return (distance, path) or (inf, []) if unreachable."""
    dist = {start: 0}
    prev = {}
    pq   = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, math.inf):
            continue
        if u == end:
            break
        for v in graph.get(u, []):
            nd = d + 1
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if end not in dist:
        return math.inf, []

    path = []
    cur = end
    while cur in prev:
        path.append(cur)
        cur = prev[cur]
    path.append(start)
    path.reverse()
    return dist[end], path

# claud's Force-directed layout i didnt manage to proprely organize my layouts so i used claude to make an overly complicated adjustable "art "canvas

class ForceLayout:
    def __init__(self, nodes, edges, width, height):
        self.nodes  = list(nodes)
        self.edges  = edges
        self.width  = width
        self.height = height
        random.seed(42)
        self.pos = {n: [random.uniform(80, width-80), random.uniform(80, height-80)]
                    for n in self.nodes}
        self.vel = {n: [0.0, 0.0] for n in self.nodes}

    def step(self, iterations=1):
        k = math.sqrt((self.width * self.height) / max(len(self.nodes), 1)) * 0.85
        repulse = k * k
        attract = 0.006
        damp    = 0.80
        cx, cy  = self.width / 2, self.height / 2
        maxf    = 8

        for _ in range(iterations):
            forces = {n: [0.0, 0.0] for n in self.nodes}

            # Gravity toward center
            for n in self.nodes:
                px, py = self.pos[n]
                forces[n][0] += (cx - px) * 0.003
                forces[n][1] += (cy - py) * 0.003

            # Repulsion
            for i, a in enumerate(self.nodes):
                for b in self.nodes[i+1:]:
                    dx = self.pos[b][0] - self.pos[a][0]
                    dy = self.pos[b][1] - self.pos[a][1]
                    d2 = dx*dx + dy*dy + 0.1
                    d  = math.sqrt(d2)
                    f  = repulse / d2
                    fx, fy = f*dx/d, f*dy/d
                    forces[a][0] -= fx; forces[a][1] -= fy
                    forces[b][0] += fx; forces[b][1] += fy

            # Attraction along edges
            for a, b in self.edges:
                if a not in self.pos or b not in self.pos:
                    continue
                dx = self.pos[b][0] - self.pos[a][0]
                dy = self.pos[b][1] - self.pos[a][1]
                d  = math.sqrt(dx*dx + dy*dy) + 0.1
                target = k * 1.2
                f  = (d - target) * attract
                fx, fy = f*dx/d, f*dy/d
                forces[a][0] += fx; forces[a][1] += fy
                forces[b][0] -= fx; forces[b][1] -= fy

            # Update velocities & positions
            for n in self.nodes:
                fx = max(-maxf, min(maxf, forces[n][0]))
                fy = max(-maxf, min(maxf, forces[n][1]))
                self.vel[n][0] = (self.vel[n][0] + fx) * damp
                self.vel[n][1] = (self.vel[n][1] + fy) * damp
                self.pos[n][0] = max(20, min(self.width-20,  self.pos[n][0] + self.vel[n][0]))
                self.pos[n][1] = max(20, min(self.height-20, self.pos[n][1] + self.vel[n][1]))

# main 
# i create the window using tkinter
# then build the graph inside of it
class SolGraphApp(tk.Tk):
    CANVAS_W = 960
    CANVAS_H = 660
    SETTLE_ITERS = 400

    def __init__(self):
        super().__init__()
        self.title("Destiny 2 — Sol Sector Graph  |  Shortest Path Finder")
        self.resizable(True, True)
        self.configure(bg="#1a1a18")

        self.graph, self.all_nodes, self.edge_set = build_graph()
        self.sorted_nodes = sorted(self.all_nodes)

        self.layout = ForceLayout(self.all_nodes, list(self.edge_set),
                                  self.CANVAS_W, self.CANVAS_H)

        self.path_nodes = set()
        self.path_edges = set()
        self.path_seq   = []
        self.path_dist  = 0

        self.dragging   = None
        self.drag_off   = (0, 0)
        self.settled    = False
        self.tick       = 0

        # filter for clear separation of the different kind of nodes set to visible by default
        self.filter_vars = {
            "hub":      tk.BooleanVar(value=True),
            "patrol":   tk.BooleanVar(value=True),
            "vendor":   tk.BooleanVar(value=True),
            "activity": tk.BooleanVar(value=True),
        }

        self._build_ui()
        self._settle_then_draw()

# user interface 
    def _build_ui(self):
        # top bar
        top = tk.Frame(self, bg="#1a1a18", pady=6)
        top.pack(fill="x", padx=12)

        tk.Label(top, text="Sol Graph", bg="#1a1a18", fg="#c2c0b6",font=("Helvetica", 14, "bold")).pack(side="top", padx=(0,16))

        # legend
        for label, color in [("Hub","#7F77DD"),("Patrol","#1D9E75"),
                               ("Vendor","#378ADD"),("Activity","#D85A30")]:
            f = tk.Frame(top, bg="#1a1a18")
            f.pack(side="left", padx=6)
            c = tk.Canvas(f, width=12, height=12, bg="#1a1a18", highlightthickness=0)
            c.pack(side="left")
            c.create_oval(1,1,11,11, fill=color, outline="")
            tk.Label(f, text=label, bg="#1a1a18", fg="#888780", font=("Helvetica", 10)).pack(side="left", padx=2)

        # filter 
        filt = tk.Frame(self, bg="#1e1e1b", pady=5)
        filt.pack(fill="x", padx=12, pady=(0,2))

        tk.Label(filt, text="Show:", bg="#1e1e1b", fg="#888780", font=("Helvetica", 10)).pack(side="left", padx=(4,10))

        filter_defs = [
            ("hub",      "Hubs",       "#7F77DD"),
            ("patrol",   "Patrols",    "#1D9E75"),
            ("vendor",   "Vendors",    "#378ADD"),
            ("activity", "Activities", "#D85A30"),]

        for key, label, color in filter_defs:
            f = tk.Frame(filt, bg="#1e1e1b")
            f.pack(side="left", padx=6)
            cb = tk.Checkbutton(
                f, text=label,
                variable=self.filter_vars[key],
                command=self._draw,
                bg="#1e1e1b", fg=color,
                selectcolor="#2c2c2a",
                activebackground="#1e1e1b", activeforeground=color,
                font=("Helvetica", 10), cursor="hand2",
                relief="flat", bd=0,
            )
            cb.pack(side="left")

        tk.Frame(filt, bg="#1e1e1b", width=16).pack(side="left")

        btn_all  = tk.Button(filt, text="All",  command=lambda: self._set_all_filters(True),
                             bg="#3d3d3a", fg="#c2c0b6", relief="flat",
                             padx=8, pady=2, font=("Helvetica", 9), cursor="hand2")
        btn_all.pack(side="left", padx=2)

        btn_none = tk.Button(filt, text="None", command=lambda: self._set_all_filters(False),
                             bg="#3d3d3a", fg="#c2c0b6", relief="flat",
                             padx=8, pady=2, font=("Helvetica", 9), cursor="hand2")
        btn_none.pack(side="left", padx=2)

        # path controls
        ctrl = tk.Frame(self, bg="#232320", pady=8)
        ctrl.pack(fill="x", padx=12, pady=(0,4))

        tk.Label(ctrl, text="current location :", bg="#232320", fg="#c2c0b6", font=("Helvetica", 10)).grid(row=0, column=0, padx=(8,4))
        self.var_from = tk.StringVar()
        cb_from = ttk.Combobox(ctrl, textvariable=self.var_from, width=28, values=self.sorted_nodes, state="normal")
        cb_from.grid(row=0, column=1, padx=4)
        cb_from.bind("<KeyRelease>", lambda e: self._filter_combo(cb_from, self.var_from))

        tk.Label(ctrl, text="destination:", bg="#232320", fg="#c2c0b6", font=("Helvetica", 10)).grid(row=0, column=2, padx=(16,4))
        self.var_to = tk.StringVar()
        cb_to = ttk.Combobox(ctrl, textvariable=self.var_to, width=28, values=self.sorted_nodes, state="normal")
        cb_to.grid(row=0, column=3, padx=4)
        cb_to.bind("<KeyRelease>", lambda e: self._filter_combo(cb_to, self.var_to))

        btn = tk.Button(ctrl, text="find the path", command=self._find_path, bg="#534AB7", fg="white", relief="flat", padx=14, pady=4, font=("Helvetica", 10, "bold"), cursor="hand2", activebackground="#3C3489", activeforeground="white")
        btn.grid(row=0, column=4, padx=16)

        btn_clear = tk.Button(ctrl, text="clear", command=self._clear_path, bg="#3d3d3a", fg="#c2c0b6", relief="flat", padx=10, pady=4, font=("Helvetica", 10), cursor="hand2")
        btn_clear.grid(row=0, column=5, padx=4)

        self.lbl_result = tk.Label(ctrl, text="", bg="#232320", fg="#c2c0b6", font=("Helvetica", 10))
        self.lbl_result.grid(row=0, column=6, padx=16)

        # drawing handle/ canva
        self.canvas = tk.Canvas(self, width=self.CANVAS_W, height=self.CANVAS_H, bg="#12120f", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=12, pady=(0,8))

        self.canvas.bind("<ButtonPress-1>",   self._on_press)
        self.canvas.bind("<B1-Motion>",       self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Motion>",          self._on_hover)
        self.canvas.bind("<Configure>",       self._on_resize)

        # pop ups
        self.tooltip = tk.Toplevel(self)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)
        self.tooltip.configure(bg="#232320")
        self.tip_lbl = tk.Label(self.tooltip, bg="#232320", fg="#c2c0b6",
                                 font=("Helvetica", 9), padx=8, pady=4)
        self.tip_lbl.pack()

        self.hovered = None

    def _set_all_filters(self, state):
        for v in self.filter_vars.values():
            v.set(state)
        self._draw()

    def _node_visible(self, nid):
        """Return True if this node should be drawn given current state of filter checkboxes."""
        if nid in HUBS:       return self.filter_vars["hub"].get()
        if nid in VENDORS:    return self.filter_vars["vendor"].get()
        if nid in ACTIVITIES: return self.filter_vars["activity"].get()
        if nid in PATROLS:    return self.filter_vars["patrol"].get()
        
        return self.filter_vars["patrol"].get()

    def _filter_combo(self, cb, var):
        typed = var.get().lower()
        filtered = [n for n in self.sorted_nodes if typed in n.lower()]
        cb["values"] = filtered

# startup / drawing 

    def _settle_then_draw(self):
        if self.tick < self.SETTLE_ITERS:
            iters = 5 if self.tick < 200 else 2
            self.layout.step(iters)
            self.tick += iters
            self._draw()
            self.after(16, self._settle_then_draw)
        else:
            self.settled = True
            self._draw()

    def _draw(self):
        c = self.canvas
        c.delete("all")
        pos = self.layout.pos

        # Edge only draw if both endpoints are visible
        for a, b in self.edge_set:
            if a not in pos or b not in pos:
                continue
            a_vis = self._node_visible(a)
            b_vis = self._node_visible(b)
            on_path = (tuple(sorted([a, b])) in self.path_edges)
            x1, y1 = pos[a]; x2, y2 = pos[b]
            if on_path and a_vis and b_vis:
                c.create_line(x1, y1, x2, y2, fill="#EF9F27", width=2.5)
            elif a_vis and b_vis:
                c.create_line(x1, y1, x2, y2, fill="#2e2e2b", width=1)
            elif on_path and (a_vis or b_vis):
                c.create_line(x1, y1, x2, y2, fill="#6b5010", width=1, dash=(4,4))

        # nodes
        for n in self.all_nodes:
            if n not in pos:
                continue
            if not self._node_visible(n):
                continue
            x, y = pos[n]
            r = node_radius(n)
            on_path = n in self.path_nodes
            is_start = self.path_seq and n == self.path_seq[0]
            is_end   = self.path_seq and n == self.path_seq[-1]
            col = node_color(n)

            if is_start or is_end:
                c.create_oval(x-r-4, y-r-4, x+r+4, y+r+4,
                              fill="#EF9F27", outline="#FAC775", width=2)
            elif on_path:
                c.create_oval(x-r-2, y-r-2, x+r+2, y+r+2,
                              fill="#BA7517", outline="#EF9F27", width=1.5)
            elif n == self.hovered:
                c.create_oval(x-r-2, y-r-2, x+r+2, y+r+2,
                              fill=col, outline="white", width=1.5)
            else:
                c.create_oval(x-r, y-r, x+r, y+r, fill=col, outline="#12120f", width=1)

            # labels for hubs, patrols, path nodes, hovered
            show_label = (n in HUBS or n in PATROLS or on_path or n == self.hovered)
            if show_label:
                text = n.replace("_", " ")
                weight = "bold" if n in HUBS else "normal"
                fg = "#EF9F27" if on_path else ("#ffffff" if n == self.hovered else "#a09e96")
                c.create_text(x, y - r - 5, text=text, fill=fg,
                              font=("Helvetica", 8, weight), anchor="s")

        # Path step numbers (only on visible nodes)
        for i, n in enumerate(self.path_seq):
            if n not in pos or not self._node_visible(n):
                continue
            x, y = pos[n]
            r = node_radius(n)
            c.create_text(x, y, text=str(i), fill="white",
                          font=("Helvetica", 7, "bold"), anchor="center")

#  pathfinding 

    def _find_path(self):
        src = self.var_from.get().strip()
        dst = self.var_to.get().strip()

        if src not in self.all_nodes:
            messagebox.showerror("Unknown node", f'"{src}" is not in the graph.')
            return
        if dst not in self.all_nodes:
            messagebox.showerror("Unknown node", f'"{dst}" is not in the graph.')
            return

        dist, path = dijkstra(self.graph, src, dst)

        if not path:
            messagebox.showinfo("No path", f"No path found between {src} and {dst}.")
            self._clear_path()
            return

        self.path_seq   = path
        self.path_nodes = set(path)
        self.path_edges = set()
        for i in range(len(path) - 1):
            self.path_edges.add(tuple(sorted([path[i], path[i+1]])))
        self.path_dist = dist

        step_str = " → ".join(p.replace("_"," ") for p in path)
        self.lbl_result.config(text=f"Distance: {dist} hops  |  {step_str}", fg="#EF9F27")
        self._draw()

    def _clear_path(self):
        self.path_nodes = set()
        self.path_edges = set()
        self.path_seq   = []
        self.path_dist  = 0
        self.lbl_result.config(text="", fg="#c2c0b6")
        self._draw()

#  interaction 

    def _node_at(self, x, y, threshold=14):
        for n, (nx, ny) in self.layout.pos.items():
            if (nx-x)**2 + (ny-y)**2 < threshold**2:
                return n
        return None

    def _on_press(self, e):
        n = self._node_at(e.x, e.y)
        if n:
            self.dragging = n
            px, py = self.layout.pos[n]
            self.drag_off = (px - e.x, py - e.y)

    def _on_drag(self, e):
        if self.dragging:
            ox, oy = self.drag_off
            self.layout.pos[self.dragging] = [e.x + ox, e.y + oy]
            self._draw()

    def _on_release(self, e):
        self.dragging = None

    def _on_hover(self, e):
        n = self._node_at(e.x, e.y)
        # ignore hover on hidden nodes 
        if n and not self._node_visible(n):
            n = None
        if n != self.hovered:
            self.hovered = n
            self._draw()
        if n:
            conns = len(self.graph.get(n, []))
            cat = ("Hub" if n in HUBS else
                   "Patrol zone" if n in PATROLS else
                   "Vendor/NPC" if n in VENDORS else
                   "Activity" if n in ACTIVITIES else "Location")
            on_path_idx = ""
            if n in self.path_nodes and self.path_seq:
                idx = self.path_seq.index(n)
                on_path_idx = f"\nStep {idx} on path"
            self.tip_lbl.config(
                text=f"{n.replace('_',' ')}\n{cat}  |  {conns} connections{on_path_idx}"
            )
            rx, ry = self.winfo_rootx(), self.winfo_rooty()
            self.tooltip.geometry(f"+{rx+e.x+16}+{ry+e.y-10}")
            self.tooltip.deiconify()
            self.tooltip.lift()
        else:
            self.tooltip.withdraw()

    def _on_resize(self, e):
        self.layout.width  = e.width
        self.layout.height = e.height
        if not self.settled:
            return
        # Clamp nodes to new size
        for n in self.layout.pos:
            self.layout.pos[n][0] = max(20, min(e.width-20,  self.layout.pos[n][0]))
            self.layout.pos[n][1] = max(20, min(e.height-20, self.layout.pos[n][1]))
        self._draw()



if __name__ == "__main__":
    app = SolGraphApp()
    app.mainloop()
