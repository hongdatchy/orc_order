import pika
import json
import os
import time

from orcUtil.readPSFile import extract_thumbnail_from_psd, extract_thumbnail_from_ai
from logService import log_file, timeToDay
from b2Service import saveToB2
from teleBot import send_tele_message
from nanoid import generate

# Kết nối đến RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

channel = connection.channel()

result = channel.queue_declare(queue='file_thumnail', durable=True)

# Hàm callback xử lý tin nhắn khi nhận được
def callback(ch, method, properties, body):
    message = json.loads(body)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    try:
        start_time = time.time()
        
        file_path = message["filePath"]
        file_name = os.path.basename(file_path)
        # file_name_no_ext = os.path.splitext(file_name)[0]
        file_ext = os.path.splitext(file_name)[1]

        size = None
        if (file_ext == ".ai"):
            size, img_byte_arr = extract_thumbnail_from_ai(file_path)
        elif file_ext == ".psd":
            size, img_byte_arr = extract_thumbnail_from_psd(file_path)
        else:
            messsageJson = {
                "error": "file photoshop không đúng định dạng",
                "message": message
            }
            messsageStr = str(messsageJson)
            send_tele_message(messsageStr)
        if(size != None):
            end_time = time.time()  # End time in seconds
            log_file(file_name, size, start_time, end_time, message)
            image_name = generate()
            #  file/artworks/2024/11/27/UIqPhVKIu_6DZbF92nos.wepb
            print(image_name)
            saveToB2(img_byte_arr, "file/artworks/" + timeToDay(start_time), image_name + ".webp", message)
            
    except Exception as e:
        messsageJson = {
            "error": str(e),
            "message": message
        }
        messsageStr = str(messsageJson)
        send_tele_message(messsageStr)

# Đăng ký callback để nhận tin nhắn
channel.basic_consume(queue='file_thumnail', on_message_callback=callback, auto_ack=False)

channel.start_consuming()
