from django.contrib.postgres.fields import JSONField 
from django.db import models

class Prediction(models.Model):
    """ A model for storing prediction data 
    The stored data can the be furthere used to make further optimizations
    """
    
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    predictions = JSONField(null=True, blank=True)
    errors = models.CharField(max_length=255, null=True, blank=True)
    date_stored = models.DateTimeField(auto_now_add=True)

