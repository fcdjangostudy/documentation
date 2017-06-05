from django.db import models


class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'small'),
        ('M', 'medium'),
        ('L', 'large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)