import requests
from dotenv import load_dotenv
import os
from fpdf import FPDF

load_dotenv('.env')

hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {hugging_face_api_key}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def report_generator(input_text):
    output = query({
        "inputs": "Generate a detailed report based on the following content: " + input_text,
        "parameters": {
            "return_full_text": False
        }
    })
    if isinstance(output, list) and len(output) > 0:
        return output[0].get('generated_text', '')
    return ''

def summarize_section(title, details):
    summary = f"{title}: "
    
    if title == "Header":
        summary += f"Model {details['truck_model']}, Serial {details['truck_serial_number']}, ID {details['inspection_id']}, Inspector {details['inspector_name']}, Date {details['date_time']}, Location {details['location']}, Service Meter {details['service_meter_hours']}."
    
    elif title == "Tires":
        summary += f"LF: {details['left_front_pressure']}, {details['left_front_condition']}, RF: {details['right_front_pressure']}, {details['right_front_condition']}, LR: {details['left_rear_pressure']}, {details['left_rear_condition']}, RR: {details['right_rear_pressure']}, {details['right_rear_condition']}."
    
    elif title == "Battery":
        summary += f"Make {details['make']}, Voltage {details['voltage']}, Water Level {details['water_level']}, No leaks or rust."
    
    elif title == "Exterior":
        summary += f"No major damage or oil leaks."
    
    elif title == "Brakes":
        summary += f"Fluid Level {details['fluid_level']}, Front {details['front_condition']}, Rear {details['rear_condition']}, Emergency Brake {details['emergency_brake']}."
    
    elif title == "Engine":
        summary += f"No major damage, Oil {details['oil_condition']}, Color {details['oil_color']}, Brake Fluid {details['brake_fluid_condition']}, Color {details['brake_fluid_color']}, No leaks."
    
    elif title == "Customer Feedback":
        summary += f"Feedback: {details['feedback']}."
    return summary

def generate_section_summary(title, details):
    section_summary = summarize_section(title, details)
    summary_text = report_generator(section_summary)
    
    images_text = "\n".join([f"Attached Image: {img}" for img in details.get('images', [])])
    
    return f"{summary_text}\n{images_text}"

def generate_final_report(data):
    sections = [
        ("Header", data['header']),
        ("Tires", data['tires']),
        ("Battery", data['battery']),
        ("Exterior", data['exterior']),
        ("Brakes", data['brakes']),
        ("Engine", data['engine']),
        ("Customer Feedback", data['customer_feedback'])
    ]
    
    final_report_parts = []
    
    for title, details in sections:
        section_summary = generate_section_summary(title, details)
        final_report_parts.append(section_summary)
    
    final_report = "\n\n".join(final_report_parts)
    return final_report

def save_report_as_pdf(report_text, output_filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, report_text)

    pdf.output(output_filename)

#Call this function
def report_generation(data):
    final_report = generate_final_report(data)  
    save_report_as_pdf(final_report, "technician_service_report.pdf")
    print("PDF report generated successfully.")
    return