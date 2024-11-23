import pika
import json
import os
import time

from readPSFile import extract_thumbnail_from_psd, extract_thumbnail_from_ai

# Kết nối đến RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

result = channel.queue_declare(queue='file_thumnail', durable=True)

# Hàm callback xử lý tin nhắn khi nhận được
def callback(ch, method, properties, body):
    print(body)

    start_time = time.time()
    message = json.loads(body)
    file_path = message["filePath"]
    file_name, file_extension = os.path.splitext(file_path)

    if file_extension == ".ai":
        extract_thumbnail_from_ai(file_path, "outputFolder/ai/" + file_name + ".png")

    else:
        extract_thumbnail_from_psd(file_path, "outputFolder/psd/" + file_name + ".png")

    end_time = time.time()  # End time in seconds

    elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
    print("Time elapsed: {:.2f} ms".format(elapsed_time))
    ch.basic_ack(delivery_tag = method.delivery_tag)

# Đăng ký callback để nhận tin nhắn
channel.basic_consume(queue='file_thumnail', on_message_callback=callback, auto_ack=False)

channel.start_consuming()
