# products/tasks.py

from celery import shared_task
from products.models import Products  # Import your Django model

# Task to process product creation
@shared_task(bind=True, max_retries=3)
def process_create(self, data):
    try:
        # Create a new product
        product = Products.objects.create(
            id=data['id'],
            title=data['title'],
            image=data['image']
        )
        print(f"Created product: {data}")
    except Exception as e:
        print(f"Error creating product: {e}")
        self.retry(exc=e, countdown=2 ** self.request.retries)

# Task to process product update
@shared_task(bind=True, max_retries=3)
def process_update(self, data):
    try:
        product = Products.objects.get(id=data['id'])
        if not product:
            raise ValueError(f"Product with ID {data['id']} not found")
        product.title = data.get('title', product.title)
        product.image = data.get('image', product.image)
        product.save()
        print(f"Updated product: {data}")
    except Exception as e:
        print(f"Error updating product: {e}")
        self.retry(exc=e, countdown=2 ** self.request.retries)

# Task to process product deletion
@shared_task(bind=True, max_retries=3)
def process_delete(self, data):
    try:
        product = Products.objects.get(id=data['id'])
        if not product:
            raise ValueError(f"Product with ID {data['id']} not found")
        product.delete()
        print(f"Deleted product: {data['id']}")
    except Exception as e:
        print(f"Error deleting product: {e}")
        self.retry(exc=e, countdown=2 ** self.request.retries)