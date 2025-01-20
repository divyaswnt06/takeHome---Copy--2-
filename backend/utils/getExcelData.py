import os
import pandas as pd
import boto3
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")
R2_BUCKET_NAME = "data"  

r2_client = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT_URL,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
)

def get_excel_data():
    try:
        file_obj = r2_client.get_object(Bucket=R2_BUCKET_NAME, Key="cv_tracking.xlsx")
        file_content = file_obj["Body"].read()
        df = pd.read_excel(BytesIO(file_content))
        data = df.to_dict(orient="records")

        return data
    except r2_client.exceptions.NoSuchKey:
        raise Exception("Excel file not found in R2")
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")
