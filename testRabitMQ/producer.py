import pika
import time

# Kết nối đến RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')


index = 0
# Gửi tin nhắn vào queue
while True:
    if(index > 20): break
    index = index + 1
    channel.basic_publish(exchange='',
                      routing_key='orc-order',
                      body="Hello " + str(index))
    
    channel.basic_publish(exchange='logs',
                      routing_key='',
                      body="Hello " + str(index))
    
    print(" [x] Sent " + str(index))
    time.sleep(0.5)

# Đóng kết nối
connection.close()
