import pika
import time

# Kết nối đến RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

# result = channel.queue_declare(queue='orc-order', durable=True)
result = channel.queue_declare(queue='', durable=True, exclusive=True)
channel.queue_bind(exchange='logs',
                   queue=result.method.queue)
# Hàm callback xử lý tin nhắn khi nhận được
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    ch.basic_ack(delivery_tag = method.delivery_tag)
    time.sleep(2)

# Đăng ký callback để nhận tin nhắn
channel.basic_consume(queue='orc-order', on_message_callback=callback, auto_ack=False)

channel.start_consuming()
