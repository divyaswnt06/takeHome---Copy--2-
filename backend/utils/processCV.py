import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import httpx
import base64
import json
import os
from dotenv import load_dotenv


load_dotenv()

def parsingCV(pdf_url):
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    doc_data = base64.standard_b64encode(
        httpx.get(pdf_url).content).decode("utf-8")

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type=content.Type.OBJECT,
            enum=[],
            required=["FirstName", "LastName", "Email", "Education", "Skills"],
            properties={
                "FirstName": content.Schema(type=content.Type.STRING),
                "LastName": content.Schema(type=content.Type.STRING),
                "Email": content.Schema(type=content.Type.STRING),
                "Education": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                "Skills": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
                "Links": content.Schema(type=content.Type.ARRAY, items=content.Schema(type=content.Type.STRING)),
            },
        ),
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    prompt = "Summarize this document"
    response = model.generate_content(
        [{'mime_type': 'application/pdf', 'data': doc_data}, prompt])

    # Parsing response to json fomrat
    jsonResponse = json.loads(response.text)
    return jsonResponse

# pdf_url = "https://pub-bd4a6e96fbe74d0d85b3ad6a30670258.r2.dev/john.doe@example.com.pdf"
# response = parsingCV(pdf_url)
# print(response)
