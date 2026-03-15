# Destiny 2 — Sol Sector Graph
### Shortest Path Finder & Interactive Map

A tool built in Python that visualises the interconnected locations of **some parts of Destiny 2's Sol system** as a navigable graph, it uses **Dijkstra's algorithm** to find the shortest route between any two points given by the user — vendors, patrol zones, activities, or hub areas.

---

## What it Does

When you first start to play Destiny 2, moving between locations isn't easy: it isnt obvios if you need to take your ship to the Tower first, or go directly through the EDZ. This app models every meaningful connection in the game's current Sol sector (just earth for now) as a graph and lets you instantly answer that question.

You pick a starting location and a destination, hit **Find the Path**, the app will highlights the optimal route across the graph with step numbers, hop count, and a full readable path string.

---

## Features

- **Shortest path via Dijkstra's algorithm** — finds the minimum-hop route between any two nodes in the graph chosen by the user
- **Force-directed graph layout** — nodes organically arrange themselves based on their connections, producing a readable spatial map 
- **Four node categories** — Hubs, Patrol Zones, Vendors/NPCs, and Activities, each with its own colour
- **Filterable view** — show or hide entire categories with checkboxes; the path display adapts accordingly
- **Draggable nodes** — click and drag any node to manually adjust the layout
- **Hover tooltips** — hover over a node to see its name, category, connection count, and its step index if it's on the current path
- **Live autocomplete dropdowns** — start typing in either field and the combo box filters to matching nodes

---

## Requirements

- Python 3.8 or newer
- `tkinter` 
---

## Running the App

```bash
python sol_graph.py
```

The window will open and the graph will animate into position over the first couple of seconds.

---

## How to Use

### Finding a Path

1. Type a location into the **current location** field (e.g. `tower`, `trostland`, `ada-1`)
2. Type your destination into the **destination** field (e.g. `lake_of_shadows`, `devrim_kay`)
3. Click **find the path**

The shortest route will be highlighted in orange across the graph, with each node numbered in order. The result bar at the bottom shows:
- The number of **hops** (edges) in the path
- The **full sequence** of locations to pass through

Click **clear** to reset the highlight.

> **Tip:** Node names use underscores instead of spaces (e.g. `the_sludge`, `firebase_hades`). The dropdown will filter as you type — you don't need to know the exact name upfront.

### Filtering Node Types

Use the checkboxes in the **Show** bar to hide or reveal entire categories:

| Category | Colour | Examples |
|----------|--------|---------|
| Hubs | Purple | Tower, Earth, Courtyard, Annex |
| Patrols | Green | EDZ, Cosmodrome, Skywatch |
| Vendors | Blue | Zavala, Banshee-44, Ada-1, The Drifter |
| Activities | Orange-Red | Lake of Shadows, Grasp of Avarice, The Pit |

Use **All** or **None** to toggle everything at once. Filtering doesn't affect the pathfinding calculation — it only affects what's drawn on screen. If a path passes through a hidden node, the relevant edge will appear as a dashed line to indicate the connection still exists.

### Interacting with the Graph

- **Drag** any node to reposition it manually
- **Hover** over a node to see a tooltip with its name, category, and connection count
- The canvas is **resizable** — drag the window edges to give the graph more room; nodes will clamp to the new bounds

---

## Graph Structure

The graph is **undirected** and **unweighted** — every connection has a cost of 1 hop. This means Dijkstra finds the route that passes through the fewest intermediate locations, not necessarily the "fastest" in real-world game time.

### Node Categories Explained

**Hubs** are the central transit nodes: `earth`, `tower`, `courtyard`, `hangar`, `annex`, `bazaar`. Many vendors and activities can only be reached by going through one of these.

**Patrol Zones** are explorable open-world areas: the EDZ, Cosmodrome, Skywatch, Mothyards, etc. They connect to each other geographically and to activities within them.

**Vendors & NPCs** are mostly leaves (1 connection) hanging off hub areas. Reaching a vendor always routes you through its hub first.

**Activities** are strikes, dungeons, and lost sectors. They connect to the patrol zones they are physically located in.

### How Edges Are Defined

Connections are defined in `EDGES_RAW` as adjacency rows. Each row is `[source, neighbour_1, neighbour_2, ...]`. The builder deduplicates edges and constructs a bidirectional adjacency list, so every connection is traversable in both directions.

---

## Code Overview

| Section | What it does |
|---------|-------------|
| `EDGES_RAW` | Raw adjacency data — the entire graph structure |
| `HUBS / PATROLS / VENDORS / ACTIVITIES` | Category sets used for colouring and filtering |
| `build_graph()` | uses `EDGES_RAW`to build the graph |
| `dijkstra(graph, start, end)` | Standard priority-queue Dijkstra returning `(distance, path)` |
| `ForceLayout` | Physics simulation: repulsion between all node pairs + attraction along edges + gravity toward canvas centre |
| `SolGraphApp` | Main `tk.Tk` subclass — builds the UI, drives the layout animation, handles all interaction |

---

## Known Limitations

- The graph reflects a **limited part** of Destiny 2's Sol sector — the earth it can an will be updated in the future
- Edge weights are uniform (1 hop per connection), so the "shortest" path is by connection count, not by actual in-game travel time 
- Some vendor/NPC nodes are only connected to one hub, meaning the path to them is always fixed regardless of origin
-  manual dragging is not saved between sessions

---

## Extending the Graph

To add new nodes or connections, edit `EDGES_RAW` in the source file. Each row follows this format:

```python
["source_node", "connected_node_1", "connected_node_2"],
```

Then add the node's name to the appropriate category set (`HUBS`, `PATROLS`, `VENDORS`, or `ACTIVITIES`) so it gets the right colour and is included in filter logic.

Node names should use lowercase with underscores in place of spaces there is a reason yes there is (its simpler when i copy paste names).

---

## Screenshots / Layout

On launch the graph settles from a random initial state into a stable layout over ~2 seconds. Hub nodes are rendered larger than patrol nodes, which are in turn larger than vendor and activity leaf nodes, giving a natural visual hierarchy.

When a path is found, the highlighted route draws on top of the existing graph in orange — making it easy to see even in a dense, heavily-connected region like the EDZ.
