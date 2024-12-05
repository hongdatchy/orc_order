import pika
import json
import os
from dotenv import load_dotenv

load_dotenv(".env.dev")
EXCHANGE_NAME = os.getenv('EXCHANGE_NAME')
EXCHANGE_TYPE = os.getenv('EXCHANGE_TYPE')
QUEUE_NAME_ORC_LABEL = os.getenv('QUEUE_NAME_ORC_LABEL')
QUEUE_NAME_FILE_THUMBNAIL = os.getenv('QUEUE_NAME_FILE_THUMBNAIL')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')

# connect to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='192.168.240.174',
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    )
)

channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE_NAME,
                         exchange_type=EXCHANGE_TYPE, durable=True)

index = 0

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
        "type": QUEUE_NAME_ORC_LABEL if index % 2 != 0 else QUEUE_NAME_FILE_THUMBNAIL
    }
    channel.basic_publish(exchange=EXCHANGE_NAME,
                      routing_key = message["type"],
                      body=json.dumps(message))
    
    print(" [x] Sent " + str(index))

connection.close()
