from pydoc import pager
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.calculations import (
    calculate_room_area,
    calculate_room_volume,
    calculate_window_area,
    calculate_natural_light,
    calculate_average_reflectance,
    calculate_required_lumens,
    get_fixture_recommendations,
    calculate_fixture_positions
)
from utils.constants import ROOM_ILLUMINANCE, FIXTURE_TYPES
from fpdf import FPDF
import io
import base64

# --- utils ---
# utils/calculator.py
def create_room_visualization(length, width, height, fixture_positions=None, wall_color='#FFFFFF', ceiling_color='#FFFFFF'):
    """Create a 3D visualization of the room using Plotly."""
    # Create the room box
    fig = go.Figure()

    # Add walls
    walls = [
        # Floor
        go.Mesh3d(x=[0,length,length,0], y=[0,0,width,width], z=[0,0,0,0],
                  color='#CCCCCC', opacity=0.7),
        # Ceiling
        go.Mesh3d(x=[0,length,length,0], y=[0,0,width,width], z=[height,height,height,height],
                  color=ceiling_color, opacity=0.7),
        # Walls
        go.Mesh3d(x=[0,length,length,0], y=[0,0,0,0], z=[0,0,height,height],
                  color=wall_color, opacity=0.7),
        go.Mesh3d(x=[length,length,length,length], y=[0,width,width,0], z=[0,0,height,height],
                  color=wall_color, opacity=0.7),
        go.Mesh3d(x=[0,0,0,0], y=[0,width,width,0], z=[0,0,height,height],
                  color=wall_color, opacity=0.7),
        go.Mesh3d(x=[0,length,length,0], y=[width,width,width,width], z=[0,0,height,height],
                  color=wall_color, opacity=0.7),
    ]

    for wall in walls:
        fig.add_trace(wall)

    # Add light fixtures
    if fixture_positions:
        for pos in fixture_positions:
            fig.add_trace(go.Scatter3d(
                x=[pos['x']], y=[pos['y']], z=[pos['z']],
                mode='markers',
                marker=dict(size=10, color='yellow', symbol='star'),
                name='Light Fixture'
            ))

            # Add light cone visualization
            theta = np.linspace(0, 2*np.pi, 20)
            r = np.linspace(0, 1, 10)
            theta, r = np.meshgrid(theta, r)

            x = pos['x'] + r * np.cos(theta) * (height - pos['z'])
            y = pos['y'] + r * np.sin(theta) * (height - pos['z'])
            z = pos['z'] - r * (height - pos['z'])

            fig.add_trace(go.Scatter3d(
                x=x.flatten(), y=y.flatten(), z=z.flatten(),
                mode='markers',
                marker=dict(size=2, color='yellow', opacity=0.1),
                name='Light Distribution'
            ))

    # Update layout
    fig.update_layout(
        scene=dict(
            aspectmode='data',
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        showlegend=False
    )

    return fig

def create_pdf_report(room_data, recommendations, fig):
    """Create a PDF report with room analysis and recommendations."""
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Room Illumination Analysis Report', ln=True, align='C')

    # Room specifications
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Room Specifications:', ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"Dimensions: {room_data['length']}m x {room_data['width']}m x {room_data['height']}m", ln=True)
    pdf.cell(0, 10, f"Room Type: {room_data['room_type']}", ln=True)
    pdf.cell(0, 10, f"Total Area: {room_data['area']:.1f} m²", ln=True)

    # Lighting Analysis
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Lighting Analysis:', ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"Required Illuminance: {room_data['required_illuminance']} lux", ln=True)
    pdf.cell(0, 10, f"Natural Light Contribution: {room_data['natural_light_factor']*100:.1f}%", ln=True)

    # Recommendations
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Recommended Lighting Solutions:', ln=True)
    pdf.set_font('Arial', '', 10)

    for fixture_type, data in recommendations.items():
        pdf.cell(0, 10, f"\n{data['description']}", ln=True)
        pdf.cell(0, 10, f"Initial Cost: ${data['energy_metrics']['initial_cost']:.2f}", ln=True)
        pdf.cell(0, 10, f"Annual Energy Cost: ${data['energy_metrics']['annual_cost']:.2f}", ln=True)
        pdf.cell(0, 10, f"Energy Efficiency: {data['specs']['efficacy']} lumens/watt", ln=True)
        pdf.cell(0, 10, '', ln=True)

    return pdf.output(dest='S').encode('latin1')

# --- Main App ---
import streamlit as st
from utils import calculator

# Set Streamlit page configuration
st.set_page_config(
    page_title="Interior Lighting Estimator",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)
calculator.show()