import os
from langflow.custom import Component
from langflow.io import HandleInput, MessageTextInput, Output, FileInput
from langflow.schema.message import Message
from langflow.schema import Data
from pdf2image import convert_from_path
from langflow.field_typing import Text

import requests
import torch
from transformers import pipeline
from transformers import AutoProcessor, AutoModelForCausalLM 
from PIL import Image

# optimize with fp16 loading
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


class DemarchesSimplifieesOCR(Component):
    display_name = "OCR"
    description = "Convert file to OCR"
    icon = "custom_components"
    name = "DemarchesSimplifieesOCR"

    inputs = [
        FileInput(name="document", display_name="Document", file_types=["pdf", "jpg", "png"]),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Message:
        print(type(self.document), self.document)
        captions = []

        if self.document.lower().endswith('.pdf'):
            images = convert_from_path(self.document)
            for i, img in enumerate(images):
                path = 'page'+ str(i) +'.jpg'
                img.save(path, 'JPEG')
                image = Image.open(path)
                caption = run_ocr(image)
                captions.append(caption)
                os.remove(path)
        else:
            image = Image.open(self.document)
            caption = run_ocr(image)
            captions.append(caption)
            
        ocr_output = "\n".join(captions)
        return Message(
            text=ocr_output,
        )