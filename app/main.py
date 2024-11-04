import uvicorn
from fastapi import FastAPI, UploadFile, File
from parsers.pdf_marker import parse_with_pdf_marker

app = FastAPI()

@app.post("/pdf-marker")
async def pdf_marker(file: UploadFile = File(...)):
    return await parse_with_pdf_marker(file)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
