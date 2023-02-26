from ast import Return
import boto3

s3 = boto3.client("s3")
with open("./sky.jpg", "rb") as buffer:
    ret = s3.upload_fileobj(buffer, "job-book-image", "sky.jpg")
    print(ret)
