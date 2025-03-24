import numpy as np
import plotly.graph_objects as go

# 1. Generate random composition data and normalize (sum = 1)
num_points = 500
raw_compositions = np.random.random((num_points, 4))
compositions = raw_compositions / np.sum(raw_compositions, axis=1, keepdims=True)

# 2. Coordinate transformation function
def projection(composition, vertices):
    """Project 4-component composition into tetrahedron coordinates"""
    return np.dot(composition, vertices)

# Define tetrahedron vertices
vertices = [
    [0, 0, 0],          # A (pure A)
    [1, 0, 0],          # B (pure B)
    [0.5, np.sqrt(3)/2, 0],      # C (pure C)
    [0.5, np.sqrt(3)/6, np.sqrt(6)/3]  # D (pure D)
]

# Transform all compositions into (x, y, z) coordinates
coordinates = np.array([projection(comp, vertices) for comp in compositions])

# Define edges of the tetrahedron
edges = [
    (0, 1), (0, 2), (0, 3),
    (1, 2), (1, 3), (2, 3)
]

# Create Plotly figure
fig = go.Figure()

# Add data points to the plot
fig.add_trace(go.Scatter3d(
    x=coordinates[:, 0],
    y=coordinates[:, 1],
    z=coordinates[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        color=compositions[:,3],  # Use D component for color scale
        colorscale='Viridis',
        opacity=0.8,
        line=dict(width=0.5, color='DarkSlateGrey')
    ),
    name='Data Points'
))

# Add tetrahedron edges to the plot
for start, end in edges:
    fig.add_trace(go.Scatter3d(
        x=[vertices[start][0], vertices[end][0]],
        y=[vertices[start][1], vertices[end][1]],
        z=[vertices[start][2], vertices[end][2]],
        mode='lines',
        line=dict(color='black', width=2),
        showlegend=False
    ))

# Add labels to the vertices
labels = ['A', 'B', 'C', 'D']
for i, vertex in enumerate(vertices):
    fig.add_trace(go.Scatter3d(
        x=[vertex[0]],
        y=[vertex[1]],
        z=[vertex[2]],
        mode='text',
        text=[labels[i]],
        textfont=dict(size=16),
        showlegend=False
    ))

# Configure layout
fig.update_layout(
    title="4-Component Tetrahedron Composition Plot",
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        bgcolor='white'
    ),
    margin=dict(l=0, r=0, b=0, t=50),
)

fig.show()
