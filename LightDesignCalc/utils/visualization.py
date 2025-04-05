import plotly.graph_objects as go
import numpy as np

def create_room_visualization(length, width, height, fixture_positions=None, 
                            wall_color='#FFFFFF', ceiling_color='#FFFFFF',
                            mounting_type="Ceiling Mounted"):
    """Create an enhanced 3D visualization of the room using Plotly."""
    fig = go.Figure()

    # Add room surfaces with improved materials
    surfaces = [
        # Floor with wood texture
        go.Surface(
            x=[[0, length], [0, length]],
            y=[[0, 0], [width, width]],
            z=[[0, 0], [0, 0]],
            colorscale=[[0, '#8B4513'], [1, '#DEB887']],
            showscale=False
        ),
        # Ceiling
        go.Surface(
            x=[[0, length], [0, length]],
            y=[[0, 0], [width, width]],
            z=[[height, height], [height, height]],
            colorscale=[[0, ceiling_color], [1, ceiling_color]],
            showscale=False
        ),
        # Walls
        go.Surface(
            x=[[0, length], [0, length]],
            y=[[0, 0], [0, 0]],
            z=[[0, 0], [height, height]],
            colorscale=[[0, wall_color], [1, wall_color]],
            showscale=False
        ),
        go.Surface(
            x=[[length, length], [length, length]],
            y=[[0, width], [0, width]],
            z=[[0, 0], [height, height]],
            colorscale=[[0, wall_color], [1, wall_color]],
            showscale=False
        ),
        go.Surface(
            x=[[0, 0], [0, 0]],
            y=[[0, width], [0, width]],
            z=[[0, 0], [height, height]],
            colorscale=[[0, wall_color], [1, wall_color]],
            showscale=False
        ),
        go.Surface(
            x=[[0, length], [0, length]],
            y=[[width, width], [width, width]],
            z=[[0, 0], [height, height]],
            colorscale=[[0, wall_color], [1, wall_color]],
            showscale=False
        )
    ]

    for surface in surfaces:
        fig.add_trace(surface)

    # Add light fixtures with improved visualization
    if fixture_positions:
        for pos in fixture_positions:
            # Add fixture symbol based on mounting type
            if "Ceiling" in mounting_type:
                z_pos = height
                symbol = "diamond"  # Changed from "star" as it's not supported in 3D
            elif "Wall" in mounting_type:
                z_pos = height * 0.8
                symbol = "diamond"
            else:  # Pendant or other types
                z_pos = height * 0.9
                symbol = "circle"

            # Add fixture
            fig.add_trace(go.Scatter3d(
                x=[pos['x']], y=[pos['y']], z=[z_pos],
                mode='markers',
                marker=dict(
                    size=12,
                    color='yellow',
                    symbol=symbol,
                    line=dict(color='orange', width=2)
                ),
                name='Light Fixture'
            ))

            # Add light cone or beam visualization
            if "Ceiling" in mounting_type or "Pendant" in mounting_type:
                # Create cone for downlights
                theta = np.linspace(0, 2*np.pi, 30)
                r = np.linspace(0, 1.2, 20)
                theta, r = np.meshgrid(theta, r)

                x = pos['x'] + r * np.cos(theta) * (z_pos)
                y = pos['y'] + r * np.sin(theta) * (z_pos)
                z = z_pos - r * z_pos

                fig.add_trace(go.Scatter3d(
                    x=x.flatten(), y=y.flatten(), z=z.flatten(),
                    mode='markers',
                    marker=dict(
                        size=2,
                        color='yellow',
                        opacity=0.1
                    ),
                    name='Light Distribution'
                ))
            elif "Wall" in mounting_type:
                # Create beam for wall lights
                y_beam = np.linspace(-1, 1, 20)
                z_beam = np.linspace(-0.5, 0.5, 20)
                y_beam, z_beam = np.meshgrid(y_beam, z_beam)

                x_beam = np.full_like(y_beam, pos['x'] + 0.5)
                y_beam = pos['y'] + y_beam
                z_beam = z_pos + z_beam

                fig.add_trace(go.Scatter3d(
                    x=x_beam.flatten(),
                    y=y_beam.flatten(),
                    z=z_beam.flatten(),
                    mode='markers',
                    marker=dict(
                        size=2,
                        color='yellow',
                        opacity=0.1
                    ),
                    name='Wall Light Beam'
                ))

    # Update layout with improved camera angle and styling
    fig.update_layout(
        scene=dict(
            aspectmode='data',
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.8, y=1.8, z=1.5)
            ),
            xaxis=dict(title="Length (m)"),
            yaxis=dict(title="Width (m)"),
            zaxis=dict(title="Height (m)")
        ),
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig
