from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# CORS setup to allow React frontend to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Check for valid file extensions
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
        else:
            return {"error": "Unsupported file format. Please upload a CSV or XLSX file."}
        
        # Returning basic information for demonstration
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "columns": df.columns.tolist(),
        }
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
