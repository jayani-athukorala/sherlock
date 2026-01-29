# app/main.py
# Imports...
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# Imports from RAG module
from app.rag import ask_question
import os, shutil


# FastAPI application instance
app = FastAPI()

# Mount URL path
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# Define directory paths for uploads and processed files
UPLOAD_DIR = "data/uploads"
PDF_DIR = "data/pdf"
TXT_DIR = "data/txt"


# Create directories if they do not already exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(TXT_DIR, exist_ok=True)


# Define a route that handles both GET and POST requests at root URL
@app.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
async def home(
    request: Request,                      # Incoming HTTP request object
    action: str | None = Form(None),        # Form field indicating action type (upload / ask)
    file: UploadFile | None = File(None),   # Uploaded file (PDF or TXT)
    question: str | None = Form(None)       # User question input
):
    # If the request method is GET, render the main page
    if request.method == "GET":
        return templates.TemplateResponse("index.html", {"request": request})

    # If POST request is for file upload and a file is provided
    if action == "upload" and file:
        # Call upload handler function
        upload_message = await upload_document(file)

        # Render page with upload status message
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "upload_message": upload_message}
        )

    # If POST request is for asking a question and question exists
    if action == "ask" and question:
        # Call question-answering function
        answer = ask_question(question)
        

        # Render page with generated answer
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "data": {"question": question, "answer": answer}}
        )

    # Default response for invalid requests
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "message": "Invalid request"}
    )


# Asynchronous function to handle file uploads
async def upload_document(file: UploadFile):
    # Create temporary path for uploaded file
    temp_path = os.path.join(UPLOAD_DIR, file.filename)

    # Write uploaded file contents to disk
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Convert filename to lowercase for extension checking
    filename = file.filename.lower()

    # If file is a PDF, move it to PDF directory
    if filename.endswith(".pdf"):
        shutil.move(temp_path, os.path.join(PDF_DIR, file.filename))

    # If file is a TXT file, move it to TXT directory
    elif filename.endswith(".txt"):
        shutil.move(temp_path, os.path.join(TXT_DIR, file.filename))

    # Delete unsupported files
    else:
        os.remove(temp_path)
        return "Only PDF and TXT files are allowed"

    # Return success message after upload
    return "File uploaded successfully!"

