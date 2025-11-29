import plotly.graph_objects as go
import numpy as np

# -------------------------------------
# 1. Synthetic performance data (REALISTIC)
# -------------------------------------

states = np.arange(1, 51)

# More realistic curves (based on ClimateSpark paper)
def spark_global(n): return 1 + 0.02 * n
def spark_regional(n): return 1 + 0.02 * n  # Spark barely changes

def scispark_global(n): return 1.5 + 0.0005 * (n ** 2.3)
def scispark_regional(n): return 1.8 + 0.0008 * (n ** 2.35)  # worse regionally

def climatespark_global(n):
    return 0.7 + 0.006 * (n ** 1.55)

def climatespark_regional(n):
    return 0.6 + 0.004 * (n ** 1.45)  # significantly faster


datasets = {
    "Global": {
        "Spark": spark_global(states),
        "SciSpark": scispark_global(states),
        "ClimateSpark": climatespark_global(states)
    },
    "Regional": {
        "Spark": spark_regional(states),
        "SciSpark": scispark_regional(states),
        "ClimateSpark": climatespark_regional(states)
    }
}


# -------------------------------------
# 2. Create figure
# -------------------------------------

initial_type = "Global"
initial_data = datasets[initial_type]

fig = go.Figure()

# Define styles for better visibility
styles = {
    "Spark": {"color": "#1f77b4", "size": 9, "dash": "solid"},
    "SciSpark": {"color": "#d62728", "size": 9, "dash": "dot"},
    "ClimateSpark": {"color": "#2ca02c", "size": 9, "dash": "dash"}
}

for name in ["Spark", "SciSpark", "ClimateSpark"]:
    fig.add_trace(go.Scatter(
        x=states,
        y=initial_data[name],
        mode="lines+markers",
        name=name,
        marker=dict(size=styles[name]["size"]),
        line=dict(width=3, dash=styles[name]["dash"], color=styles[name]["color"])
    ))


# -------------------------------------
# 3. Slider
# -------------------------------------

steps = []
for i in range(len(states)):
    step = dict(
        method="update",
        args=[
            {"x": [states[:i+1]] * 3,
             "y": [
                 initial_data["Spark"][:i+1],
                 initial_data["SciSpark"][:i+1],
                 initial_data["ClimateSpark"][:i+1]
             ]
            },
            {"title": f"Performance up to {states[i]} States"}
        ]
    )
    steps.append(step)

sliders = [dict(
    active=0,
    pad={"t": 50},
    steps=steps,
    currentvalue={"prefix": "Queried states: "}
)]


# -------------------------------------
# 4. Dropdown (Global / Regional)
# -------------------------------------

fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                dict(
                    label="Global",
                    method="update",
                    args=[
                        {"y": [
                            datasets["Global"]["Spark"],
                            datasets["Global"]["SciSpark"],
                            datasets["Global"]["ClimateSpark"]
                        ]},
                        {"title": "Performance Comparison — Global Query"}
                    ]
                ),
                dict(
                    label="Regional",
                    method="update",
                    args=[
                        {"y": [
                            datasets["Regional"]["Spark"],
                            datasets["Regional"]["SciSpark"],
                            datasets["Regional"]["ClimateSpark"]
                        ]},
                        {"title": "Performance Comparison — Regional Query"}
                    ]
                )
            ],
            direction="down",
            showactive=True,
            x=1.15, y=1.15
        )
    ]
)


# -------------------------------------
# 5. Layout (high-contrast, log scale)
# -------------------------------------

fig.update_layout(
    sliders=sliders,
    title="Performance Comparison: Spark vs SciSpark vs ClimateSpark",
    xaxis_title="Number of Queried States",
    yaxis_title="Execution Time (log scale)",
    yaxis_type="log",
    width=1100,
    height=700,
    template="plotly_white",
    font=dict(size=16),
    legend=dict(x=0.7, y=1.12, bgcolor="rgba(255,255,255,0.8)")
)

fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")

# Export HTML for QR-code sharing
fig.write_html("climatespark_interactive_performance.html")


