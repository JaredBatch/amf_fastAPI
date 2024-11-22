from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel, HttpUrl
from uuid import UUID
import requests

app = FastAPI()

class PrintJob(BaseModel):
    material_slot: int
    printer_id: UUID
    gcode: HttpUrl
    additional_info: Optional[dict] = None

@app.post("/send-print-job")
async def send_print_job(job: PrintJob):
    # Extract material_slot and printer_id
    data_to_send = {
        "material_slot": job.material_slot,
        "printer_id": str(job.printer_id)  # Convert UUID to string for JSON serialization
    }

    # Send the data to Raspberry Pi
    raspberry_pi_url = "http://10.50.114.22:5001/receive-job"  # Replace with the Pi's IP
    try:
        response = requests.post(raspberry_pi_url, json=data_to_send)
        if response.status_code == 200:
            pi_response = response.json()
            return {"status": "success", "message": "Data forwarded to Raspberry Pi", "pi_response": pi_response}
        else:
            return {"status": "error", "message": "Failed to forward data to Raspberry Pi", "pi_response": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}