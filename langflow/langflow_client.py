import os
import json
from typing import Optional
from langflow.load import upload_file
import requests

LANGFLOW_API_URL = "http://127.0.0.1:7860"

def parse_llm_output(text):
    try:
        # Try parsing as JSON with quotes
        parsed_text = json.loads(text)
        return parsed_text
    except json.JSONDecodeError:
        try:
            # Try parsing as Python dict string
            cleaned_text = text.replace("`", '')
            cleaned_text = cleaned_text.replace("json", '')
            parsed_text = json.loads(cleaned_text)
            return parsed_text
        except json.JSONDecodeError:
            # Return None if parsing fails
            return None


def get_flow(id: str):
    url = f"{LANGFLOW_API_URL}/api/v1/flows/{id}"
    response = requests.get(url)
    return response.json()

def get_node(edges:list[dict], node: str):
    matches = [edge.get('source') for edge in edges if edge.get('source').startswith(node)]
    if len(matches):
        return matches.pop()
    return None


def run_flow(flow_id: str, ocr_file_path:Optional[str]=None):

    payload: dict = {}
    TWEAKS = {
    }
    
    flow = get_flow(flow_id)
    edges = flow.get('data').get('edges')

    ocr_node = get_node(edges, "DemarchesSimplifieesOCR")
    if ocr_node:
        payload_with_file = upload_file(
            file_path=ocr_file_path,
            host=LANGFLOW_API_URL,
            flow_id=flow_id,
            components=["File-ID"],
            tweaks=payload,
        )
        TWEAKS[ocr_node] = {
            "document": payload_with_file.get('File-ID').get('path')
        }

    albert_node = get_node(edges, "AlbertModel")
    if albert_node:
        TWEAKS[albert_node] = {
            "api_key": os.environ.get("ALBERT_API")
        }

    


    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{LANGFLOW_API_URL}/api/v1/run/{flow_id}",
        json={"tweaks": TWEAKS},
        headers=headers
    )
    data = json.loads(response.content)
    try:
        text_content = data['outputs'][0]['outputs'][0]['results']['message']['data']['text']
        parsed_text = parse_llm_output(text_content)
        category = parsed_text.get("category", None)
        return category
    except Exception as e:        
        return "FAILED"



# ALBERT_FLOW = "d3d21488-2924-4f2a-9d03-2e696c48d7cc"
# OLLAMA_FLOW = "f71bcc8b-9cc0-455e-9ddc-15811164b8a3"

# # file_path = "./data/carte_grise.jpg"
# # file_path = "./data/rib_iban_erwan_boehm.pdf"
# file_path = "./data/cni.jpg"


# run_flow(ALBERT_FLOW, file_path)
