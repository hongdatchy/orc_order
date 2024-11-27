from b2sdk.v2 import InMemoryAccountInfo, B2Api
from concurrent.futures import ThreadPoolExecutor
from teleBot import send_tele_message
import json

executor = ThreadPoolExecutor(max_workers=5)  

APP_KEY_ID = "000c16b6f8f311b0000000006"  # KeyID của bạn
APP_KEY = "K000VVtXQv+Ngvs5F6b/LbeGl8v+AaQ"  # ApplicationKey của bạn
BUCKET_NAME = "tebprint-test"  # Bucket của bạn

# Khởi tạo B2 API
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", APP_KEY_ID, APP_KEY)

# Lấy Bucket
bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

# Khởi tạo client S3

def upload_to_b2(img_byte_arr, file_name_on_b2, messsageJson):
    """ Hàm đồng bộ upload file lên B2 """
    try:
        bucket.upload_bytes(img_byte_arr.read(), file_name_on_b2)
        print(f"Upload file '{file_name_on_b2}' thành công")
    except Exception as e:
        print(f"Lỗi khi upload file")
        messsageJson["error"] = str(e)
        messsageStr = str(messsageJson)
        send_tele_message(messsageStr)

def saveToB2(img_byte_arr, file_name, messsageJson, folder_name_b2="thbumbail"):
    """ Hàm bất đồng bộ để upload file lên B2 """
    file_name_on_b2 = folder_name_b2 + "/" + file_name  # Tên file trên bucket
    
    # Sử dụng ThreadPoolExecutor để chạy hàm upload trong luồng con
    executor.submit(upload_to_b2, img_byte_arr, file_name_on_b2, messsageJson)


# saveToB2("outputFolder/psd/Gửi Đức 21-12 Dương.png", "Gửi Đức 21-12 Dương.png")