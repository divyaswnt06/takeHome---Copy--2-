from utils.getExcelData import get_excel_data
from utils.processCV import parsingCV
from utils.updateExcel import update_excel
from utils.uploadR2 import upload_to_r2
from fastapi.responses import JSONResponse
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "Welcome to the CV upload and processing API!"}


@app.post('/api/upload_cv')
async def upload_cv(file: UploadFile = File(...)):
    try:
        # temp file
        local_file_path = f"./{file.filename}"
        with open(local_file_path, "wb") as f:
            f.write(await file.read())

        # R2 upload
        email = file.filename.split('.')[0]
        uploaded_url = upload_to_r2(local_file_path, f"{email}.pdf")

        # gemini processing the uploaded cv
        if uploaded_url:
            cv_summary = parsingCV(uploaded_url)
            update_excel(
                email=cv_summary["Email"],
                first_name=cv_summary["FirstName"],
                last_name=cv_summary["LastName"],
                education=cv_summary["Education"],
                skills=cv_summary["Skills"],
                links=cv_summary["Links"],
                cv_link=uploaded_url
            )
            return JSONResponse(content={"message": "CV uploaded and processed successfully", "cv_summary": cv_summary})

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing file: {str(e)}")


@app.get('/api/get_details')
async def get_details():
    try:
        # Get all data from Excel using the utility function
        data = get_excel_data()

        return JSONResponse(content={"data": data})

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching data: {str(e)}")
