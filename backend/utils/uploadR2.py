import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv



load_dotenv()


def upload_to_r2(file_name, email):
    """
    Uploads a local file to Cloudflare R2 with a renamed file based on the candidate's email.

    :param file_name: Path to the local file to upload.
    :param email: Email of the candidate to create a unique file name.
    :return: URL of the uploaded file or None if upload failed.
    """
    access_key_id = os.getenv("R2_ACCESS_KEY_ID")
    secret_access_key = os.getenv("R2_SECRET_ACCESS_KEY")
    endpoint_url = os.getenv("R2_ENDPOINT_URL")
    bucket_name = os.getenv("R2_BUCKET_NAME")

    object_name = f"{email}.pdf"

    s3_client = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        # Return the public URL
        return f"https://pub-bd4a6e96fbe74d0d85b3ad6a30670258.r2.dev/{object_name}"
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

# if __name__ == "__main__":
#     local_file = "test.pdf"  # Local file name
#     bucket_name = "resume"  # Your R2 bucket name
#     email = "john.doe@example.com"  # Candidate's email
#     uploaded_file_url = upload_to_r2(local_file, email)
#     if uploaded_file_url:
#         print(f"Uploaded file URL: {uploaded_file_url}")
