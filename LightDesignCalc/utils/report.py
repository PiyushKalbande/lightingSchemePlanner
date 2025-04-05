from fpdf import FPDF
import io

class RoomReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Room Illumination Analysis Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(room_data, recommendations, fig):
    """Create an enhanced PDF report with room analysis and recommendations."""
    pdf = RoomReport()
    pdf.add_page()

    # Room specifications
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Room Specifications:', ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"Dimensions: {room_data['length']}m x {room_data['width']}m x {room_data['height']}m", ln=True)
    pdf.cell(0, 10, f"Room Type: {room_data['room_type']}", ln=True)
    pdf.cell(0, 10, f"Total Area: {room_data['area']:.1f} m²", ln=True)
    pdf.cell(0, 10, f"Mounting Type: {room_data['mounting_type']}", ln=True)

    # Lighting Analysis
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Lighting Analysis:', ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"Required Illuminance: {room_data['required_illuminance']} lux", ln=True)
    pdf.cell(0, 10, f"Required Artificial Light: {room_data['required_lumens']:.0f} lumens", ln=True)
    pdf.cell(0, 10, f"Natural Light Contribution: {room_data['natural_light_factor']*100:.1f}%", ln=True)

    # Recommendations
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Recommended Lighting Solutions:', ln=True)
    pdf.set_font('Arial', '', 10)

    for fixture_type, data in recommendations.items():
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, fixture_type, ln=True)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, f"Configuration: {data['description']}", ln=True)
        pdf.cell(0, 10, f"Initial Cost: Rs. {data['energy_metrics']['initial_cost']:,.2f}", ln=True)
        pdf.cell(0, 10, f"Installation Cost: Rs. {data['count'] * data['specs']['installation_cost']:,.2f}", ln=True)
        pdf.cell(0, 10, f"Annual Energy Consumption: {data['energy_metrics']['annual_energy_kwh']:.1f} kWh", ln=True)
        pdf.cell(0, 10, f"Annual Energy Cost: Rs. {data['energy_metrics']['annual_cost']:,.2f}", ln=True)
        pdf.cell(0, 10, f"Energy Efficiency: {data['specs']['efficacy']} lumens/watt", ln=True)
        pdf.cell(0, 10, f"Expected Lifetime: {data['energy_metrics']['lifetime_years']:.1f} years", ln=True)
        pdf.cell(0, 10, f"Total Cost of Ownership: Rs. {data['energy_metrics']['total_cost']:,.2f}", ln=True)

    return pdf.output(dest='S').encode('latin1')
