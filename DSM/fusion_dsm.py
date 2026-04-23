"""
Standalone DSM script for a fusion system.

What it does
------------
- Defines a small set of fusion subsystems
- Adds sample dependencies of type:
    * Information
    * Design
    * Function
- Builds a DSM matrix
- Exports:
    * fusion_system_dsm.html
    * fusion_system_nodes.csv
    * fusion_system_edges.csv

Install once:
    pip install plotly

Run:
    python fusion_system_dsm.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import plotly.graph_objects as go


OUTPUT_DIR = Path(".")


# ---------------------------------------------------------------------
# Sample fusion-system components
# ---------------------------------------------------------------------
# Nodes as variables


# Core plasma + magnets
PLASMA = "Plasma"
TF_COILS = "Toroidal Field Coils"
PF_COILS = "Poloidal Field Coils"
STAB_COILS = "Stabilizing Coils"
CENTRAL_SOLENOID = "Central Solenoid"

# Vessel / in-vessel
VACUUM_VESSEL = "Vacuum Vessel"
FIRST_WALL = "First Wall"
DIVERTOR = "Divertor"
PORTS = "Ports"

# Systems
HEATING = "Heating System"
FUELING = "Fueling System"
PUMPING = "Pumping System"
CRYOSTAT = "Cryostat"
COOLING_BLANKET = "Cooling System Blanket"


NODES = [
    PLASMA,
    TF_COILS,
    PF_COILS,
    STAB_COILS,
    CENTRAL_SOLENOID,
    VACUUM_VESSEL,
    FIRST_WALL,
    DIVERTOR,
    PORTS,
    HEATING,
    FUELING,
    PUMPING,
    CRYOSTAT,
    COOLING_BLANKET,
]

# Each edge is:
# (source, target, dependency_type, short_label)

DESIGN_EDGES = [
    # Toroidal field coils
    (TF_COILS, VACUUM_VESSEL, "Design", ""),
    (TF_COILS, PORTS, "Design", ""),
    (TF_COILS, DIVERTOR, "Design", ""),
    (TF_COILS, CENTRAL_SOLENOID, "Design", ""),
    (TF_COILS, STAB_COILS, "Design", ""),
    (TF_COILS, CRYOSTAT, "Design", ""),

    # Poloidal field coils
    (PF_COILS, VACUUM_VESSEL, "Design", ""),
    (PF_COILS, CRYOSTAT, "Design", ""),
    (PF_COILS, TF_COILS, "Design", ""),
    (PF_COILS, PORTS, "Design", ""),
    (PF_COILS, CENTRAL_SOLENOID, "Design", ""),

    # Stabilizing coils
    (STAB_COILS, TF_COILS, "Design", ""),
    (STAB_COILS, DIVERTOR, "Design", ""),
    (STAB_COILS, VACUUM_VESSEL, "Design", ""),
    (STAB_COILS, FIRST_WALL, "Design", ""),
    (STAB_COILS, PORTS, "Design", ""),

    # Central solenoid
    (CENTRAL_SOLENOID, TF_COILS, "Design", ""),
    (CENTRAL_SOLENOID, PF_COILS, "Design", ""),
    (CENTRAL_SOLENOID, VACUUM_VESSEL, "Design", ""),
    (CENTRAL_SOLENOID, CRYOSTAT, "Design", ""),

    # Ports
    (PORTS, VACUUM_VESSEL, "Design", ""),
    (PORTS, CRYOSTAT, "Design", ""),
    (PORTS, FIRST_WALL, "Design", ""),
    (PORTS, DIVERTOR, "Design", ""),
    (PORTS, HEATING, "Design", ""),
    (PORTS, FUELING, "Design", ""),
    (PORTS, PUMPING, "Design", ""),

    # Vacuum vessel
    (VACUUM_VESSEL, FIRST_WALL, "Design", ""),
    (VACUUM_VESSEL, DIVERTOR, "Design", ""),
    (VACUUM_VESSEL, PORTS, "Design", ""),
    (VACUUM_VESSEL, CRYOSTAT, "Design", ""),
    (VACUUM_VESSEL, COOLING_BLANKET, "Design", ""),
    (VACUUM_VESSEL, HEATING, "Design", ""),
    (VACUUM_VESSEL, FUELING, "Design", ""),
    (VACUUM_VESSEL, PUMPING, "Design", ""),

    # First wall
    (FIRST_WALL, VACUUM_VESSEL, "Design", ""),
    (FIRST_WALL, DIVERTOR, "Design", ""),
    (FIRST_WALL, PORTS, "Design", ""),
    (FIRST_WALL, COOLING_BLANKET, "Design", ""),
    (FIRST_WALL, HEATING, "Design", ""),
    (FIRST_WALL, FUELING, "Design", ""),

    # Divertor
    (DIVERTOR, VACUUM_VESSEL, "Design", ""),
    (DIVERTOR, FIRST_WALL, "Design", ""),
    (DIVERTOR, PORTS, "Design", ""),
    (DIVERTOR, COOLING_BLANKET, "Design", ""),
    (DIVERTOR, PUMPING, "Design", ""),
    (DIVERTOR, TF_COILS, "Design", ""),
    (DIVERTOR, STAB_COILS, "Design", ""),

    # Heating system
    (HEATING, PORTS, "Design", ""),
    (HEATING, VACUUM_VESSEL, "Design", ""),
    (HEATING, FIRST_WALL, "Design", ""),
    (HEATING, PLASMA, "Design", ""),

    # Fueling system
    (FUELING, PORTS, "Design", ""),
    (FUELING, VACUUM_VESSEL, "Design", ""),
    (FUELING, FIRST_WALL, "Design", ""),
    (FUELING, DIVERTOR, "Design", ""),
    (FUELING, PLASMA, "Design", ""),

    # Pumping system
    (PUMPING, PORTS, "Design", ""),
    (PUMPING, VACUUM_VESSEL, "Design", ""),
    (PUMPING, DIVERTOR, "Design", ""),
    (PUMPING, CRYOSTAT, "Design", ""),

    # Cryostat
    (CRYOSTAT, TF_COILS, "Design", ""),
    (CRYOSTAT, PF_COILS, "Design", ""),
    (CRYOSTAT, CENTRAL_SOLENOID, "Design", ""),
    (CRYOSTAT, PORTS, "Design", ""),
    (CRYOSTAT, VACUUM_VESSEL, "Design", ""),
    (CRYOSTAT, PUMPING, "Design", ""),

    # Cooling blanket system
    (COOLING_BLANKET, FIRST_WALL, "Design", ""),
    (COOLING_BLANKET, DIVERTOR, "Design", ""),
    (COOLING_BLANKET, VACUUM_VESSEL, "Design", ""),
    (COOLING_BLANKET, PORTS, "Design", ""),

    # Plasma
    (PLASMA, FIRST_WALL, "Design", ""),
    (PLASMA, DIVERTOR, "Design", ""),
    (PLASMA, HEATING, "Design", ""),
    (PLASMA, FUELING, "Design", ""),
]


# EDGES = [
#     (DIAGNOSTICS, PLASMA_CONTROL, "Information", "sensor data"),
#     (PLASMA_CONTROL, PF_COILS, "Function", "shape control"),
#     (PLASMA_CONTROL, TF_COILS, "Function", "field request"),
#     (TF_COILS, CRYO, "Function", "superconducting load"),
#     (CRYO, TF_COILS, "Function", "cooling supply"),
#     (VACUUM_VESSEL, BLANKET, "Design", "mounting envelope"),
#     (VACUUM_VESSEL, DIVERTOR, "Design", "interface geometry"),
#     (BLANKET, COOLING, "Function", "heat removal"),
#     (DIVERTOR, COOLING, "Function", "peak heat removal"),
#     (COOLING, POWER, "Function", "steam / heat input"),
#     (BLANKET, DIAGNOSTICS, "Design", "port allocation"),
#     (DIAGNOSTICS, VACUUM_VESSEL, "Design", "penetrations"),
#     (PF_COILS, VACUUM_VESSEL, "Design", "support loads"),
#     (TF_COILS, VACUUM_VESSEL, "Design", "structural clearance"),
#     (POWER, PLASMA_CONTROL, "Information", "available power status"),
#     (COOLING, BLANKET, "Information", "coolant temperature"),
#     (COOLING, DIVERTOR, "Information", "flow feedback"),
#     (BLANKET, POWER, "Function", "thermal output"),
# ]
EDGES = DESIGN_EDGES

TYPE_STYLE = {
    "Information": {"fill": 1, "text": "I", "color": "#4C78A8"},
    "Design": {"fill": 2, "text": "D", "color": "#F58518"},
    "Function": {"fill": 3, "text": "F", "color": "#54A24B"},
    "Mixed": {"fill": 4, "text": "M", "color": "#B279A2"},
}


GROUP_BLOCKS = [
    # {"row_start": 0, "row_end": 2, "col_start": 0, "col_end": 2, "label": "Magnet / control", "color": "rgba(0, 100, 255, 0.10)"},
    # {"row_start": 3, "row_end": 5, "col_start": 3, "col_end": 5, "label": "In-vessel", "color": "rgba(255, 140, 0, 0.10)"},
    # {"row_start": 6, "row_end": 9, "col_start": 6, "col_end": 9, "label": "Balance of plant", "color": "rgba(0, 180, 120, 0.10)"},
]


def build_matrix(nodes: list[str], edges: list[tuple[str, str, str, str]]):
    """Create DSM z-matrix plus per-cell text annotations."""
    index = {name: i for i, name in enumerate(nodes)}
    n = len(nodes)

    z = [[0 for _ in range(n)] for _ in range(n)]
    text = [["" for _ in range(n)] for _ in range(n)]
    hover = [["" for _ in range(n)] for _ in range(n)]
    cell_types = [[set() for _ in range(n)] for _ in range(n)]
    cell_notes = [[[] for _ in range(n)] for _ in range(n)]

    for source, target, dep_type, label in edges:
        i = index[source]
        j = index[target]
        cell_types[i][j].add(dep_type)
        cell_notes[i][j].append(f"{dep_type}: {label}")

    for i in range(n):
        for j in range(n):
            if i == j:
                text[i][j] = "—"
                hover[i][j] = f"{nodes[i]} → {nodes[j]}<br>Same component"
                continue

            types_here = cell_types[i][j]
            if not types_here:
                text[i][j] = ""
                hover[i][j] = f"{nodes[i]} → {nodes[j]}<br>No dependency entered"
                continue

            if len(types_here) == 1:
                dep_type = next(iter(types_here))
                z[i][j] = TYPE_STYLE[dep_type]["fill"]
                text[i][j] = TYPE_STYLE[dep_type]["text"]
            else:
                z[i][j] = TYPE_STYLE["Mixed"]["fill"]
                ordered = [t for t in ("Information", "Design", "Function") if t in types_here]
                text[i][j] = "/".join(TYPE_STYLE[t]["text"] for t in ordered)

            hover[i][j] = (
                f"{nodes[i]} → {nodes[j]}"
                + "<br>"
                + "<br>".join(cell_notes[i][j])
            )

    return z, text, hover


def add_blocks(fig: go.Figure, blocks: list[dict], n_nodes: int) -> None:
    """Overlay lightly colored blocks on the DSM."""
    shapes = []
    annotations = []

    for block in blocks:
        r0, r1 = block["row_start"], block["row_end"]
        c0, c1 = block["col_start"], block["col_end"]

        shapes.append(
            go.layout.Shape(
                type="rect",
                x0=c0 - 0.5,
                x1=c1 + 0.5,
                y0=r0 - 0.5,
                y1=r1 + 0.5,
                line=dict(color="rgba(40,40,40,0.35)", width=1),
                fillcolor=block["color"],
                layer="below",
            )
        )

        annotations.append(
            go.layout.Annotation(
                x=(c0 + c1) / 2,
                y=r0 - 0.7,
                text=block["label"],
                showarrow=False,
                font=dict(size=11),
            )
        )

    fig.update_layout(shapes=shapes, annotations=annotations)


def export_csv(nodes: list[str], edges: list[tuple[str, str, str, str]]) -> None:
    nodes_path = OUTPUT_DIR / "fusion_system_nodes.csv"
    edges_path = OUTPUT_DIR / "fusion_system_edges.csv"

    with nodes_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "component"])
        for idx, node in enumerate(nodes, start=1):
            writer.writerow([idx, node])

    with edges_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "dependency_type", "label"])
        for row in edges:
            writer.writerow(row)

    print(f"Saved {nodes_path}")
    print(f"Saved {edges_path}")


def build_figure(nodes: list[str], edges: list[tuple[str, str, str, str]]) -> go.Figure:
    z, text, hover = build_matrix(nodes, edges)

    colorscale = [
        [0.00, "#FFFFFF"],
        [0.24, "#FFFFFF"],
        [0.25, TYPE_STYLE["Information"]["color"]],
        [0.49, TYPE_STYLE["Information"]["color"]],
        [0.50, TYPE_STYLE["Design"]["color"]],
        [0.74, TYPE_STYLE["Design"]["color"]],
        [0.75, TYPE_STYLE["Function"]["color"]],
        [0.99, TYPE_STYLE["Function"]["color"]],
        [1.00, TYPE_STYLE["Mixed"]["color"]],
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=nodes,
            y=nodes,
            text=text,
            texttemplate="%{text}",
            textfont={"size": 12},
            hovertemplate="%{customdata}<extra></extra>",
            customdata=hover,
            colorscale=colorscale,
            zmin=0,
            zmax=4,
            showscale=False,
            xgap=1,
            ygap=1,
        )
    )

    add_blocks(fig, GROUP_BLOCKS, len(nodes))

    legend_items = [
        ("I = Information", TYPE_STYLE["Information"]["color"]),
        ("D = Design", TYPE_STYLE["Design"]["color"]),
        ("F = Function", TYPE_STYLE["Function"]["color"]),
        # ("M = Mixed", TYPE_STYLE["Mixed"]["color"]),
    ]

    for name, color in legend_items:
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=12, color=color, symbol="square"),
                name=name,
                showlegend=True,
                hoverinfo="skip",
            )
        )

    # fig.update_layout(
    #     # title="Fusion System DSM (sample self-contained script)",
    #     width=1100,
    #     height=900,
    #     template="plotly_white",
    #     xaxis=dict(side="top", tickangle=-45),
    #     yaxis=dict(autorange="reversed"),
    #     # legend=dict(
    #     #     orientation="h",
    #     #     yanchor="bottom",
    #     #     y=1.06,
    #     #     xanchor="left",
    #     #     x=0.0,
    #     # ),
    #     margin=dict(l=170, r=40, t=120, b=100),
    # )

    # fig.update_layout(
    #     margin=dict(l=120, r=20, t=60, b=60),  # 👈 reduce left margin
    # )
    # fig.update_xaxes(
    #     tickangle=-45,
    #     tickfont=dict(size=10),
    #     automargin=False  # 👈 prevents extra padding
    # )

    # fig.update_yaxes(
    #     tickfont=dict(size=11),
    #     automargin=False  # 👈 tighter to matrix
    # )
    fig.update_layout(
        title="Fusion System DSM",
        margin=dict(
            l=180,   # more room for y labels
            r=40,
            t=140,   # more room for rotated top labels
            b=60
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            side="top",
            domain=[0.12, 0.98],   # keep matrix wide but not flush to edge
        ),
    )

    fig.update_xaxes(
        tickangle=-45,
        tickfont=dict(size=16),
        automargin=True,          # important: prevents top labels getting cut
        ticklabelposition="outside top",
    )

    fig.update_yaxes(
        tickfont=dict(size=16),
        automargin=True,          # important: prevents left labels getting cut
    )

    return fig


def main():
    fig = build_figure(NODES, EDGES)

    html_path = OUTPUT_DIR / "fusion_system_dsm.html"
    fig.write_html(html_path, include_plotlyjs="cdn")
    export_csv(NODES, EDGES)

    print(f"Saved {html_path}")
    fig.show()


if __name__ == "__main__":
    main()
