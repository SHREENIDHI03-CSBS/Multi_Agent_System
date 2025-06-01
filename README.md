# 🧠 Multi-Agent AI System with Format & Intent Classification

A multi-agent AI backend built using **FastAPI** and **Redis** that classifies and routes inputs in different formats (PDF, JSON, Email) to specialized agents. The system maintains a shared memory to preserve conversation context, extracted fields, and routing history.

---

## 📌 Features

- 🔍 **Classifier Agent**:
  - Detects input format (`PDF`, `JSON`, or `Email`)
  - Classifies intent (`Invoice`, `RFQ`, `Complaint`, `Regulation`, etc.)
  - Routes the input to the corresponding agent

- 📄 **PDF/Document Agent** *(To be added)*

- 📨 **Email Agent**:
  - Extracts sender, subject, urgency, and content summary
  - Formats data for CRM-style systems

- 🔧 **JSON Agent**:
  - Parses and validates structured JSON
  - Extracts values and flags anomalies

- 🧠 **Shared Memory Module**:
  - Powered by Redis
  - Stores source, format, timestamp, extracted info, conversation ID

---

## 🏗️ Architecture

┌──────────────┐
│ /classify/ │◄── Receives input (file + source)
└──────┬───────┘
▼
┌────────────────┐
│ ClassifierAgent│──► Detects format + intent
└──────┬─────────┘
▼
┌────────┐ ┌───────────┐ ┌────────────┐
│EmailAgent│◄──┤PDFAgent(*)│◄───▶│JSONAgent │
└────────┘ └───────────┘ └────────────┘
│
▼
🧠 SharedMemory (Redis)

2. Install dependencies

python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

3. Start Redis (if not running)
Install Redis from https://redis.io.

Start Redis locally:
redis-server

4. Run the FastAPI server
uvicorn main:app --reload

5. Test with curl
curl -X POST "http://127.0.0.1:8000/classify/" ^
  -F "file=@C:/path/to/email.txt" ^
  -F "source=test_source"

🧪 API Endpoints
POST /classify/
Accepts any file (.pdf, .json, .txt) and source name.
Request:
file: UploadFile (via multipart/form-data)
source: Source name

Response:
json
{
  "convo_id": "UUID",
  "format": "Email",
  "intent": "Invoice",
  "result": {
    "sender": "user@example.com",
    "intent": "invoice",
    "urgency": "normal",
    "summary": "Invoice #123..."
  }
}

🧠 Redis Memory Structure
Each classified input is logged like:

json
{
  "source": "test_source",
  "format": "Email",
  "intent": "Invoice",
  "timestamp": "2025-06-01T12:00:00Z",
  "extracted": {
    "sender": "user@example.com",
    "summary": "...."
  }
}

🛠 Future Work
Add PDF Agent for OCR/NER-based field extraction
Plug-in LLMs for deeper summarization
Build frontend for agent visualization
Add authentication and session handling

📂 Repo Structure
bash
Copy
Edit
backend/
├── main.py                 
├── memory.py               
├── agents/
│   ├── classifier.py
│   ├── email_agent.py
│   └── json_agent.py
├── requirements.txt
└── README.md

🤝 License
MIT License. Free to use, fork, and modify!

