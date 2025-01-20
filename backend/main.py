from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.cvRoutes import router as upload_cv_router

app = FastAPI()

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_cv_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the CV upload and processing API!"}
