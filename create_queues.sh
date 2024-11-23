#!/bin/sh

# Đảm bảo RabbitMQ đã sẵn sàng
echo "Waiting for RabbitMQ to be ready..."
sleep 10

# Tạo queue ocr_label
rabbitmqadmin declare queue name=ocr_label durable=true

# Tạo queue file_thumbnail
rabbitmqadmin declare queue name=file_thumbnail durable=true

echo "Queues created!"
