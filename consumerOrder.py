import pika
import json
import time

from readOrderMultitheadKeyValueResult import print_PDF

# Kết nối đến RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

result = channel.queue_declare(queue='ocr_label', durable=True)

# Hàm callback xử lý tin nhắn khi nhận được
def callback(ch, method, properties, body):
    print(body)
    start_time = time.time()
    message = json.loads(body)

    print_PDF(message["filePath"])
    end_time = time.time()  # End time in seconds
    
    elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
    print("Time elapsed: {:.2f} ms".format(elapsed_time))
    ch.basic_ack(delivery_tag = method.delivery_tag)

# Đăng ký callback để nhận tin nhắn
channel.basic_consume(queue='ocr_label', on_message_callback=callback, auto_ack=False)

channel.start_consuming()
