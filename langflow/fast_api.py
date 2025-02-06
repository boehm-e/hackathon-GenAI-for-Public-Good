import uvicorn
import uuid
import torch
import os
import json
from transformers import AutoProcessor, AutoModelForCausalLM 
from PIL import Image
from pdf2image import convert_from_path
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from prompt import get_classification_prompt
from ollama import chat
from ollama import ChatResponse


model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-base", trust_remote_code=True, torch_dtype=torch.float16).to(torch.cuda.current_device())
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-base", trust_remote_code=True)

def run_ocr(image):
    task = "<OCR>"
    response = run_florence_2(image, task, text_input="")
    return response.get(task, "")

def run_florence_2(image, task_prompt, text_input=None):
    if text_input is None:
        prompt = task_prompt
    else:
        prompt = task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(torch.cuda.current_device(), dtype=torch.float16)
    generated_ids = model.generate(
      input_ids=inputs["input_ids"],
      pixel_values=inputs["pixel_values"],
      max_new_tokens=128,
      num_beams=1
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

    parsed_answer = processor.post_process_generation(generated_text, task=task_prompt, image_size=(image.width, image.height))
    return parsed_answer

def parse_llm_output(text):
    try:
        parsed_text = json.loads(text)
        return parsed_text
    except json.JSONDecodeError:
        try:
            cleaned_text = text.replace("`", '')
            cleaned_text = cleaned_text.replace("json", '')
            parsed_text = json.loads(cleaned_text)
            return parsed_text
        except json.JSONDecodeError:
            return None

def run_ocr_on_document(document_path: str):
    captions = []
    if document_path.endswith('.pdf'):
        images = convert_from_path(document_path)
        for i, img in enumerate(images):
            path = 'page'+ str(i) +'.jpg'
            img.save(path, 'JPEG')
            image = Image.open(path)
            caption = run_ocr(image)
            captions.append(caption)
            os.remove(path)
    else:
        image = Image.open(document_path)
        caption = run_ocr(image)
        captions.append(caption)
        
    ocr_output = "\n".join(captions)
    return ocr_output


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the file or process it as needed
    file_content = await file.read()
    
    uid = str(uuid.uuid4())
    
    file_path = f"{uid}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file_content)

    document_text = run_ocr_on_document(file_path)
    prompt = get_classification_prompt(document_text)
    llm_response: ChatResponse = chat(model='llama3.1:8b', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    response = parse_llm_output(llm_response.message.content)
    print("RESPONSE", response)
    
    return {"message": "ok", "category": response.get('category'), "filename": file.filename, "uid": uid}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
