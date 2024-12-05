from bson import ObjectId
import pika
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

from Constant import ORDER_STATUS
from orcUtil.readPSFile import extract_thumbnail_from_psd, extract_thumbnail_from_ai
from logService import log_file, timeToDay
from b2Service import saveToB2
from teleBot import send_tele_message
from mongoService import find, update_one

EXCHANGE_NAME = os.getenv('EXCHANGE_NAME')
EXCHANGE_TYPE = os.getenv('EXCHANGE_TYPE')
QUEUE_NAME_FILE_THUMBNAIL = os.getenv('QUEUE_NAME_FILE_THUMBNAIL')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
max_workers = 5

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

result = channel.queue_declare(queue=QUEUE_NAME_FILE_THUMBNAIL, durable=True)
channel.queue_bind(queue=QUEUE_NAME_FILE_THUMBNAIL, exchange=EXCHANGE_NAME, routing_key=QUEUE_NAME_FILE_THUMBNAIL)

def download_and_save_file(url, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    file_name = os.path.basename(url)
    file_path = os.path.join(save_folder, file_name)
    
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Error downloading file: {url}, status code: {response.status_code}")
    return file_path

def process_file (frontArtworkUrl, message, item):
    try:
        file_path = download_and_save_file(frontArtworkUrl, "inputTemp")
        start_time = time.time()
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1]
        img_ext = ".webp"
        size = None
        if (file_ext == ".ai"):
            size, img_byte_arr = extract_thumbnail_from_ai(file_path, img_ext)
        elif file_ext == ".psd":
            print(file_path)
            size, img_byte_arr = extract_thumbnail_from_psd(file_path, img_ext)
        else:
            raise Exception("photoshop file is invalid")
        if(size != None):
            end_time = time.time()  # End time in seconds
            log_file(file_name, size, start_time, end_time, message)
            image_name = item["id"]
            file_name_on_b2 = "file/artworks/" + timeToDay(start_time) + "/" + image_name + img_ext
            return saveToB2(img_byte_arr, file_name_on_b2)
    except Exception as e:
        raise e
        

def callback(ch, method, properties, body):
    message = json.loads(body)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    futures = []  

    all_successful = True
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i, item in enumerate(message['items']):
            frontArtworkUrl = item["frontArtworkUrl"]
            if(frontArtworkUrl == None):
                continue
            future = executor.submit(process_file, frontArtworkUrl, message, item)
            futures.append(future)
        for future in futures:
            try:
                #  update artwork link in order item collection
                url_on_b2 = future.result()
                print(url_on_b2)
                update_one("orderItems", {'order':ObjectId(message["orderId"])}, {"frontArtworkUrl": url_on_b2})
            except Exception as e:
                update_one("orderItems", {'order':ObjectId(message["orderId"])}, {"status": ORDER_STATUS["PROCESSING"]})
                all_successful = False
                messsageJson = {
                    "error": str(e),
                    "message": message
                }
                messsageStr = str(messsageJson)
                send_tele_message(messsageStr)
    if all_successful:
        # Update artwork status in order collection
        update_one("orders", {'_id':message["orderId"]}, {"status": ORDER_STATUS["PROCESSING"]})
    else:
        update_one("orders", {'_id':message["orderId"]}, {"status": ORDER_STATUS["ARTWORK_ERROR"]})

channel.basic_consume(queue=QUEUE_NAME_FILE_THUMBNAIL, on_message_callback=callback, auto_ack=False)

channel.start_consuming()
