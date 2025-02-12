from django.db import models


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    image = models.URLField()

    def __str__(self):
        return self.title


