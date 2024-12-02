import pika
import json
import os

# Kết nối đến RabbitMQ server
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Kết nối đến RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='192.168.240.174',  # Địa chỉ của RabbitMQ container, có thể dùng tên service trong docker-compose
        credentials=pika.PlainCredentials("admin", "12345678")  # Sử dụng username và password từ môi trường
    )
)

channel = connection.channel()
# channel.exchange_declare(exchange='tebprint-test.direct',
#                          exchange_type='direct', durable=True)

index = 0
# Gửi tin nhắn vào queue
while True:
    index = index + 1
    if(index > 10): break
    message = {
        "orderId": 'xyz',
        "taskId": 'fsdaf',
        "fileId": 'abc',
        "filePath": "inputFolder/1234.pdf" if index % 2 != 0 else 
        ("inputFolder/File cut gửi anh Tính.ai" if index % 4 == 0 else "inputFolder/Gửi Đức 21-12 Dương.psd"),
        # "filePath": "inputFolder/test.txt" if index % 2 != 0 else 
        # ("inputFolder/File cut gửi anh Tính.ai" if index % 4 == 0 else "inputFolder/test.txt"),
        "type": "tebprint-test.direct.ocr_label" if index % 2 != 0 else "tebprint-test.direct.file_thumnail"
    }
    channel.basic_publish(exchange='tebprint-test.direct',
                      routing_key = message["type"],
                      body=json.dumps(message))
    
    print(" [x] Sent " + str(index))

# Đóng kết nối
connection.close()
