from b2sdk.v2 import InMemoryAccountInfo, B2Api
from concurrent.futures import ThreadPoolExecutor

import os

executor = ThreadPoolExecutor(max_workers=5)  

APP_KEY_ID = os.getenv('APP_KEY_ID')
APP_KEY = os.getenv('APP_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
AWS_S3_ENDPOINT = os.getenv('AWS_S3_ENDPOINT')

info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", APP_KEY_ID, APP_KEY)



bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

def upload_to_b2(img_byte_arr, file_name_on_b2):
    try:
        bucket.upload_bytes(img_byte_arr.read(), file_name_on_b2)
        return AWS_S3_ENDPOINT + "/" + BUCKET_NAME + "/" + file_name_on_b2
    except Exception as e:
        raise Exception("Error upload to b2 " + str(e))

def saveToB2(img_byte_arr, file_name_on_b2):
    # https://s3.us-west-000.backblazeb2.com/tebprint-test/file/artworks/2024-12-03/cyN91Wm9VHlAZ33oQzW-R.webp
    future = executor.submit(upload_to_b2, img_byte_arr, file_name_on_b2)
    try:
        return future.result()
    except Exception as e:
        raise e