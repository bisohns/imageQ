from django.contrib.postgres.fields import JSONField 
from django.db import models

class Predictions(models.Model):
    """ A model for storing prediction data 
    The stored data can the be furthere used to make further optimizations
    """
    
    image = models.ImageField()
    predictions = JSONField()
    date_stored = models.DateTimeField(auto_add_now=True)

