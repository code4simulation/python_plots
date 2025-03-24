import numpy as np
import plotly.graph_objects as go

# 1. Generate random composition data and normalize (sum = 1)
num_points = 500
raw_compositions = np.random.random((num_points, 3))
compositions = raw_compositions / np.sum(raw_compositions, axis=1, keepdims=True)

# 2. Coordinate transformation function
def projection(composition, vertices):
    return np.dot(composition, vertices)

# 3. Define triangle vertices for the ternary plot
vertices = [[0, 0],                  # A (pure A)
            [1, 0],                  # B (pure B)
            [0.5, np.sqrt(3)/2]      # C (pure C)
]

# Convert compositions to Cartesian coordinates
coordinates = np.array([projection(comp, vertices) for comp in compositions])

# Define edges of the triangle
edges = [(0, 1), (1, 2), (2, 0)]

# Create Plotly figure
fig = go.Figure()

# Add data points to the plot
fig.add_trace(go.Scatter(
    x=coordinates[:, 0],
    y=coordinates[:, 1],
    mode='markers',
    marker=dict(
        size=8,
        color=compositions[:, 2],  # Use C component for color scale
        colorscale='Viridis',
        opacity=0.8,
        line=dict(width=0.5, color='DarkSlateGrey')
    ),
    name='Data Points'
))

# Add triangle edges to the plot
for start, end in edges:
    fig.add_trace(go.Scatter(
        x=[vertices[start][0], vertices[end][0]],
        y=[vertices[start][1], vertices[end][1]],
        mode='lines',
        line=dict(color='black', width=2),
        showlegend=False
    ))

# Add labels to the vertices
labels = ['A', 'B', 'C']
for i, vertex in enumerate(vertices):
    fig.add_trace(go.Scatter(
        x=[vertex[0]],
        y=[vertex[1]],
        mode='text',
        text=[labels[i]],
        textfont=dict(size=16),
        showlegend=False
    ))

# Configure layout for an equilateral triangle appearance with fixed aspect ratio
fig.update_layout(
    title="Ternary Composition Plot",
    xaxis=dict(
        range=[-0.1, 1.1],   # Set x-axis range to ensure triangle fits well
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        scaleanchor="y"      # Lock aspect ratio with y-axis
    ),
    yaxis=dict(
        range=[-0.1, np.sqrt(3)/2 + 0.1],  # Set y-axis range for equilateral triangle
        showgrid=False,
        zeroline=False,
        showticklabels=False,
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=40, t=40, b=40),
)

fig.show()
