import os
import json
from datetime import datetime, timedelta, timezone

def log_file(file_name, file_size, start_time, end_time, mesage):
    # Đường dẫn thư mục và tệp
    folder_path = "log/log-" + timeToDay(start_time)
    file_path = os.path.join(folder_path, "log.txt")

    # Kiểm tra xem thư mục có tồn tại hay không
    if not os.path.exists(folder_path):
        print("Thư mục chưa tồn tại, sẽ được tạo.")
        os.makedirs(folder_path)
    
    # Tạo tệp trong thư mục
    with open(file_path, "a", encoding="utf-8") as file:

        file.write(json.dumps({
            "file_name": file_name,
            "file_size": file_size,
            "start_time": timeToTime(start_time),
            "process_time": (end_time - start_time) * 1000,
            "mesage": mesage
        }, ensure_ascii=False) + "\n")


def timeToDay(date):
    tz = timezone(offset=timedelta(hours=7))
    return datetime.fromtimestamp(date, tz).date().strftime("%Y-%m-%d")

from datetime import datetime, timezone

def timeToTime(date):
    tz = timezone(offset=timedelta(hours=7))
    return datetime.fromtimestamp(date, tz).time().strftime("%H:%M:%S")

