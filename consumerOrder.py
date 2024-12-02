import pika
import json
import time
import os

from logService import log_file
from orcUtil.readOrderMultithead import print_PDF
from teleBot import send_tele_message

# Kết nối đến RabbitMQ server
# connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
rabbitmq_user = os.getenv('RABBITMQ_USER', 'default_user')  # 'default_user' là giá trị mặc định
rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'default_password')  # 'default_password' là giá trị mặc định
queue_name = 'tebprint-test.direct.ocr_label'

# Kết nối đến RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq',  # Địa chỉ của RabbitMQ container, có thể dùng tên service trong docker-compose
        credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password)  # Sử dụng username và password từ môi trường
    )
)

channel = connection.channel()

result = channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(queue=queue_name, exchange='tebprint-test.direct', routing_key=queue_name)

# Hàm callback xử lý tin nhắn khi nhận được
def callback(ch, method, properties, body):
    message = json.loads(body)
    print(message)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    try:
        # print(body)
        start_time = time.time()
        file_path = message["filePath"]
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1]
        if file_ext == ".pdf":
            results, pdf_size = print_PDF(message["filePath"])
            end_time = time.time()  # End time in seconds
            log_file(file_name, pdf_size, start_time, end_time, message)
        else:
            messsageJson = {
                "error": "file pdf không đúng định dạng",
                "message": message
            }
            messsageStr = str(messsageJson)
            send_tele_message(messsageStr)
    except Exception as e:
        messsageJson = {
            "error": str(e),
            "message": message
        }
        messsageStr = str(messsageJson)
        send_tele_message(messsageStr)

# Đăng ký callback để nhận tin nhắn
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

channel.start_consuming()
