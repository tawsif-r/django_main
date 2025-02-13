import pika
import json

def publish_message(exchange_name, routing_key, data):
    rabbitmq_host = 'rabbitmq'
    rabbitmq_port = 5672
    rabbitmq_user = 'tawsif'
    rabbitmq_password = '123'

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    )
    channel = connection.channel()

    # Declare the exchange
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic',durable=True)

    # Publish the message in Celery's expected format
    task_message = {
        "task": f"products.tasks.process_{routing_key.split('.')[1]}",
        "args": [data],
        "kwargs": {},
        "id": "01"
    }
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=json.dumps(task_message),
        properties=pika.BasicProperties(content_type='application/json')
    )
    print(f" [x] Sent '{routing_key}':'{json.dumps(task_message)}'")
    connection.close()