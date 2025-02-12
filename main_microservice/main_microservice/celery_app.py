
import os
from celery import Celery
from kombu import Queue, Exchange


# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_microservice.settings')
# Initialize Celery app
app = Celery('products_process')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

products_exchange = Exchange('products_exchange',type="topic")

app.conf.task_queues = (
    Queue('products_create_queue', products_exchange, routing_key='products.create'),
    Queue('products_update_queue', products_exchange, routing_key='products.update'),
    Queue('products_delete_queue', products_exchange, routing_key='products.delete'),
)

app.conf.task_routes = {
    'products.tasks.process_create': {'queue': 'products_create_queue', 'routing_key': 'products.create'},
    'products.tasks.process_update': {'queue': 'products_update_queue', 'routing_key': 'products.update'},
    'products.tasks.process_delete': {'queue': 'products_delete_queue', 'routing_key': 'products.delete'},
}

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

