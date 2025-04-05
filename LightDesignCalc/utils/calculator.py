import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.calculations import (
    calculate_room_area,
    calculate_window_area,
    calculate_natural_light,
    calculate_average_reflectance,
    calculate_required_lumens,
    get_fixture_recommendations,
    calculate_fixture_positions
)
from utils.constants import (
    ROOM_ILLUMINANCE,
    FIXTURE_TYPES,
    MOUNTING_OPTIONS,
    INR_TO_USD
)
from utils.visualization import create_room_visualization
from utils.report import create_pdf_report

def show():
    st.title("Interior Lighting Estimator")
    
    # Create three columns for better organization
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Room Specifications")
        
        # Room dimensions
        length = st.number_input("Room Length (meters)", min_value=1.0, max_value=20.0, value=4.0)
        width = st.number_input("Room Width (meters)", min_value=1.0, max_value=20.0, value=3.0)
        height = st.number_input("Room Height (meters)", min_value=2.0, max_value=5.0, value=2.4)
        
        # Room type
        room_type = st.selectbox("Room Type", options=list(ROOM_ILLUMINANCE.keys()))
        
        # Colors with color picker
        wall_color = st.color_picker("Wall Color", "#FFFFFF")
        ceiling_color = st.color_picker("Ceiling Color", "#FFFFFF")
        
        # Fixture preferences
        preferred_fixture = st.selectbox("Preferred Fixture Type", options=list(FIXTURE_TYPES.keys()))
        
        # Mounting options based on fixture type
        mounting_type = st.selectbox(
            "Mounting Type",
            options=MOUNTING_OPTIONS[preferred_fixture]
        )
        
        # Windows
        st.subheader("Natural Light Sources")
        num_windows = st.number_input("Number of Windows", min_value=0, max_value=10, value=1)
        
        if num_windows > 0:
            window_width = st.number_input("Window Width (meters)", min_value=0.3, max_value=4.0, value=1.2)
            window_height = st.number_input("Window Height (meters)", min_value=0.3, max_value=3.0, value=1.5)
            orientation = st.selectbox("Window Orientation", options=["North", "South", "East", "West"])
        else:
            window_width = window_height = 0
            orientation = "North"

    # Calculations
    room_area = calculate_room_area(length, width)
    window_area = calculate_window_area(num_windows, window_width, window_height)
    natural_light_factor = calculate_natural_light(window_area, room_area, orientation) if num_windows > 0 else 0
    reflectance = calculate_average_reflectance(wall_color, ceiling_color)
    required_lumens = calculate_required_lumens(
        room_area,
        ROOM_ILLUMINANCE[room_type],
        reflectance,
        natural_light_factor
    )

    # Get recommendations and calculate fixture positions
    recommendations = get_fixture_recommendations(required_lumens)
    fixture_positions = calculate_fixture_positions(
        length, width, height,
        preferred_fixture,
        required_lumens,
        mounting_type
    )

    with col2:
        # Display room visualization
        st.subheader("Room Visualization")
        fig = create_room_visualization(
            length, width, height,
            fixture_positions,
            wall_color,
            ceiling_color,
            mounting_type
        )
        st.plotly_chart(fig, use_container_width=True)

        # Display calculations
        st.subheader("Room Analysis")
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.metric("Room Area", f"{room_area:.1f} m²")
            st.metric("Required Illuminance", f"{ROOM_ILLUMINANCE[room_type]} lux")
            st.metric("Required Artificial Light", f"{required_lumens:.0f} lumens")
            
        with metrics_col2:
            st.metric("Natural Light Contribution", f"{natural_light_factor*100:.1f}%")
            st.metric("Surface Reflectance", f"{reflectance:.2f}")

        # Display energy efficiency table
        st.subheader("Energy Efficiency Comparison")
        efficiency_data = []
        for fixture_type, data in recommendations.items():
            metrics = data['energy_metrics']
            efficiency_data.append({
                "Fixture Type": fixture_type,
                "Quantity": data['count'],
                "Initial Cost (₹)": f"₹{metrics['initial_cost']:,.2f}",
                "Installation Cost (₹)": f"₹{data['count'] * FIXTURE_TYPES[fixture_type]['installation_cost']:,.2f}",
                "Annual Energy (kWh)": f"{metrics['annual_energy_kwh']:.1f}",
                "Annual Cost (₹)": f"₹{metrics['annual_cost']:,.2f}",
                "Lifetime (years)": f"{metrics['lifetime_years']:.1f}",
                "Total Cost (₹)": f"₹{metrics['total_cost']:,.2f}"
            })

        st.table(efficiency_data)

        # Generate PDF Report
        if st.button("Download Detailed Report"):
            room_data = {
                "length": length,
                "width": width,
                "height": height,
                "room_type": room_type,
                "area": room_area,
                "required_illuminance": ROOM_ILLUMINANCE[room_type],
                "required_lumens": required_lumens,
                "natural_light_factor": natural_light_factor,
                "mounting_type": mounting_type
            }

            pdf_bytes = create_pdf_report(room_data, recommendations, fig)
            st.download_button(
                label="Click here to download PDF report",
                data=pdf_bytes,
                file_name="room_illumination_report.pdf",
                mime="application/pdf"
            )






            
