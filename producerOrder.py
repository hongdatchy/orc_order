import pika
import json

# Kết nối đến RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
# channel.exchange_declare(exchange='logs',
#                          exchange_type='fanout')

index = 0
# Gửi tin nhắn vào queue
while True:
    index = index + 1
    if(index > 10): break
    message = {
        "orderId": 'xyz',
        "taskId": 'fsdaf',
        "fileId": 'abc',
        "filePath": "inputFoler/1234.pdf" if index % 2 != 0 else 
        ("inputFoler/File cut gửi anh Tính.ai" if index % 4 == 0 else "inputFoler/Gửi Đức 21-12 Dương.psd"),
        # "filePath": "inputFoler/test.txt" if index % 2 != 0 else 
        # ("inputFoler/File cut gửi anh Tính.ai" if index % 4 == 0 else "inputFoler/test.txt"),
        "type": "ocr_label" if index % 2 != 0 else "file_thumnail"
    }
    channel.basic_publish(exchange='',
                      routing_key = message["type"],
                      body=json.dumps(message))
    
    print(" [x] Sent " + str(index))

# Đóng kết nối
connection.close()
