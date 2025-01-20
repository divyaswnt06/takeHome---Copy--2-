from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from utils.uploadR2 import upload_to_r2
from utils.updateExcel import update_excel
from utils.processCV import parsingCV
from utils.getExcelData import get_excel_data
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter(
    prefix='/api',
    tags=['initial']
)
router.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.post('/upload_cv')
async def upload_cv(file: UploadFile = File(...)):
    try:
    #temp file 
        local_file_path = f"./{file.filename}"
        with open(local_file_path, "wb") as f:
            f.write(await file.read())

        #R2 upload
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


@router.get('/get_details')
async def get_details():
    try:
        # Get all data from Excel using the utility function
        data = get_excel_data()

        return JSONResponse(content={"data": data})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")