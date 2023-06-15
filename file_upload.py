import boto3
import os
from dotenv import load_dotenv
from models import ResponseModel


load_dotenv()

s3_client = boto3.client("s3", region_name=os.getenv("AWS.REGION"), aws_access_key_id=os.getenv("AWS.KEY"), aws_secret_access_key=os.getenv("AWS.SECRET"))
def upload_to_s3(file_path: str, file_name: str):
    s3_client.upload_fileobj(file_path, os.getenv("BUCKET"), file_name)
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': os.getenv("BUCKET"), 'Key': file_name},
        ExpiresIn=36000
    )
    print(f"Url: {url}")
    return ResponseModel(code="00", message="Successful", data={"file_url": url, "file_name": file_name})
