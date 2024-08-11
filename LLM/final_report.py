import requests
from dotenv import load_dotenv
import os
from fpdf import FPDF
import sys
import json
from flask import Flask

load_dotenv('.env')

hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {hugging_face_api_key}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def report_generator(input_text):
    output = query({
        "inputs": "Generate a concise report based strictly on the provided data without adding extra information: " + input_text,
        "parameters": {
            "return_full_text": False
        }
    })
    if isinstance(output, list) and len(output) > 0:
        return output[0].get('generated_text', '')
    return ''

def summarize_section(title, details):
    summary = f"{title}:\n"
    
    if title == "Header":
        summary += (f"Model: {details['truck_model']}\n"
                    f"Serial Number: {details['truck_serial_number']}\n"
                    f"Inspection ID: {details['inspection_id']}\n"
                    f"Inspector: {details['inspector_name']}\n"
                    f"Date: {details['date_time']}\n"
                    f"Location: {details['location']}\n"
                    f"Service Meter: {details['service_meter_hours']}\n")
    
    elif title == "Tires":
        summary += (f"Left Front Tire: {details['left_front_pressure']} - {details['left_front_condition']}\n"
                    f"Right Front Tire: {details['right_front_pressure']} - {details['right_front_condition']}\n"
                    f"Left Rear Tire: {details['left_rear_pressure']} - {details['left_rear_condition']}\n"
                    f"Right Rear Tire: {details['right_rear_pressure']} - {details['right_rear_condition']}\n")
    
    elif title == "Battery":
        summary += (f"Make: {details['make']}\n"
                    f"Voltage: {details['voltage']}\n"
                    f"Water Level: {details['water_level']}\n"
                    f"Condition: No leaks or rust.\n")
    
    elif title == "Exterior":
        summary += "Condition: No major damage or oil leaks.\n"
    
    elif title == "Brakes":
        summary += (f"Fluid Level: {details['fluid_level']}\n"
                    f"Front Condition: {details['front_condition']}\n"
                    f"Rear Condition: {details['rear_condition']}\n"
                    f"Emergency Brake: {details['emergency_brake']}\n")
    
    elif title == "Engine":
        summary += (f"Oil Condition: {details['oil_condition']} - {details['oil_color']}\n"
                    f"Brake Fluid Condition: {details['brake_fluid_condition']} - {details['brake_fluid_color']}\n"
                    f"Condition: No major damage or leaks.\n")
    
    elif title == "Customer Feedback":
        summary += f"Feedback: {details['feedback']}\n"
    
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
        final_report_parts.append(f"--- {title} ---\n{section_summary}\n")
    
    final_report = "\n".join(final_report_parts)
    return final_report

def save_report_as_pdf(report_text, output_filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'Technician Service Report', ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, report_text)

    pdf.output(output_filename)

# Sample JSON data
data = {
    "header": {
        "truck_serial_number": "7301234",
        "truck_model": "730",
        "inspection_id": "12345",
        "inspector_name": "John Doe",
        "inspection_employee_id": "5678",
        "date_time": "2024-08-10",
        "location": "XYZ",
        "geo_coordinates": "N/A",
        "service_meter_hours": "1234 hrs",
        "inspector_signature": "John Doe",
        "customer_name": "ABC Corp",
        "cat_customer_id": "CUST123",
        "images": ["header_image_1.jpg", "header_image_2.jpg"]
    },
    "tires": {
        "left_front_pressure": "30psi",
        "right_front_pressure": "32psi",
        "left_front_condition": "Good",
        "right_front_condition": "Ok",
        "left_rear_pressure": "30psi",
        "right_rear_pressure": "32psi",
        "left_rear_condition": "Needs Replacement",
        "right_rear_condition": "Good",
        "images": ["tire_image_1.jpg", "tire_image_2.jpg", "tire_image_3.jpg", "tire_image_4.jpg"]
    },
    "battery": {
        "make": "CAT",
        "replacement_date": "2023-01-01",
        "voltage": "12V",
        "water_level": "Good",
        "condition_damage": "N",
        "leak_rust": "N",
        "images": ["battery_image_1.jpg"]
    },
    "exterior": {
        "rust_dent_damage": "N",
        "oil_leak_suspension": "N",
        "images": ["exterior_image_1.jpg"]
    },
    "brakes": {
        "fluid_level": "Ok",
        "front_condition": "Good",
        "rear_condition": "Needs Replacement",
        "emergency_brake": "Good",
        "images": ["brakes_image_1.jpg"]
    },
    "engine": {
        "rust_dent_damage": "N",
        "oil_condition": "Good",
        "oil_color": "Clean",
        "brake_fluid_condition": "Good",
        "brake_fluid_color": "Clean",
        "oil_leak": "N",
        "images": ["engine_image_1.jpg"]
    },
    "customer_feedback": {
        "feedback": "Satisfied with service.",
        "images": ["customer_feedback_image_1.jpg"]
    }
}

# Call this function
def report_generation(data):
    final_report = generate_final_report(data)  
    save_report_as_pdf(final_report, "technician_service_report.pdf")
    print("PDF report generated successfully.")
    return

report = json.loads(sys.argv[1])
report_generation(report)