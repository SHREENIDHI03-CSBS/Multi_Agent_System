from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Any, Dict
from shared_memory import save_context, get_context
from classifier_agent import detect_format, detect_intent
from json_agent import process_json
from email_agent import extract_email_info
import uuid
import datetime

app = FastAPI()

# Pydantic response model for consistent output
class ProcessResponse(BaseModel):
    conversation_id: str
    context: Dict[str, Any]

# Custom HTML frontend
@app.get("/", response_class=HTMLResponse)
async def custom_form():
    return """
    <html>
        <head>
            <title>Multi-Agent AI System</title>
            <style>
                body { font-family: Arial, sans-serif; background: #f9f9f9; padding: 2em; }
                .container { background: #fff; padding: 2em; border-radius: 8px; max-width: 500px; margin: auto; box-shadow: 0 2px 8px #ccc;}
                h2 { color: #2d5be3; }
                label { margin-top: 1em; display: block; }
                input, textarea { width: 100%; margin-top: 0.5em; padding: 0.5em; }
                button { margin-top: 1em; background: #2d5be3; color: #fff; border: none; padding: 0.75em 1.5em; border-radius: 4px; cursor: pointer; }
                #response { margin-top: 2em; white-space: pre-wrap; background: #f4f4f4; padding: 1em; border-radius: 4px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Upload File or Paste Email/JSON</h2>
                <form id="uploadForm" enctype="multipart/form-data">
                    <label for="file">Choose file (PDF/JSON):</label>
                    <input type="file" id="file" name="file">
                    <label for="text">Or paste email/JSON here:</label>
                    <textarea id="text" name="text" rows="6"></textarea>
                    <button type="submit">Submit</button>
                </form>
                <div id="response"></div>
            </div>
            <script>
                document.getElementById('uploadForm').onsubmit = async function(e) {
                    e.preventDefault();
                    const formData = new FormData();
                    const fileInput = document.getElementById('file');
                    const textInput = document.getElementById('text').value;
                    if (fileInput.files.length > 0) {
                        formData.append('file', fileInput.files[0]);
                    }
                    if (textInput.trim() !== "") {
                        formData.append('text', textInput);
                    }
                    const res = await fetch('/process/', {
                        method: 'POST',
                        body: formData
                    });
                    let data;
                    try {
                        data = await res.json();
                    } catch {
                        data = { error: "Invalid server response." };
                    }
                    document.getElementById('response').innerText = JSON.stringify(data, null, 2);
                }
            </script>
        </body>
    </html>
    """

# The main processing endpoint
@app.post("/process/", response_model=ProcessResponse)
async def process_input(file: UploadFile = File(None), text: str = Form(None)):
    # Read file or text input
    if file:
        content = await file.read()
        filename = file.filename
    else:
        content = text
        filename = None

    # Detect format and intent
    fmt = detect_format(content, filename)
    if isinstance(content, bytes):
        content_str = content.decode(errors="ignore")
    else:
        content_str = content
    intent = detect_intent(content_str)

    # Generate conversation ID and timestamp
    conversation_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()

    # Route to the correct agent
    if fmt == "JSON":
        result = process_json(content)
    elif fmt == "EMAIL":
        result = extract_email_info(content_str)
    elif fmt == "PDF":
        result = {"message": "PDF processing not implemented in this demo."}
    else:
        result = {"error": "Unknown format"}

    # Build and save context
    context = {
        "source": fmt,
        "type": intent,
        "timestamp": timestamp,
        "extracted": result
    }
    save_context(conversation_id, context)
    return ProcessResponse(conversation_id=conversation_id, context=context)
