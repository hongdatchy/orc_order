import pika
import json
import time
import os

from logService import log_file
from orcUtil.readOrderMultithead import print_PDF
from teleBot import send_tele_message

EXCHANGE_NAME = os.getenv('EXCHANGE_NAME')
EXCHANGE_TYPE = os.getenv('EXCHANGE_TYPE')
QUEUE_NAME_ORC_LABEL = os.getenv('QUEUE_NAME_ORC_LABEL')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')


# connect to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq',
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    )
)

channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE_NAME,
                         exchange_type=EXCHANGE_TYPE, durable=True)

result = channel.queue_declare(queue=QUEUE_NAME_ORC_LABEL, durable=True)
channel.queue_bind(queue=QUEUE_NAME_ORC_LABEL, exchange=EXCHANGE_NAME, routing_key=QUEUE_NAME_ORC_LABEL)

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
            end_time = time.time()
            log_file(file_name, pdf_size, start_time, end_time, message)
        else:
            messsageJson = {
                "error": "pdf file is invalid",
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

channel.basic_consume(queue=QUEUE_NAME_ORC_LABEL, on_message_callback=callback, auto_ack=False)

channel.start_consuming()
