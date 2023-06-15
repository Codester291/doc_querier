from fastapi import FastAPI, UploadFile
from query_ai import perform_queries
from file_upload import upload_to_s3
from models import ResponseModel, QueryDTO
from query_ai import perform_queries

app = FastAPI()
types = ['img', 'png', 'PNG', 'jpg', 'JPG']

@app.post("/upload")
def upload(file: UploadFile):
    file_type = file.filename.split('.')[1]
    print(file_type)
    if file_type in types:
        return {"message": "Incompatible file format"}
    return upload_to_s3(file.file, file.filename)
    

@app.post("/query")
def upload(queryDTO: QueryDTO):
    return perform_queries(url=queryDTO.url, query=queryDTO.query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5500)