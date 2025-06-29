from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10, default='N/A')
    companyName = models.CharField(max_length=255, default='N/A')
    shares = models.IntegerField()
    purchase_date = models.DateField()
    latestPrice = models.FloatField(default=0.0)
    previousClose = models.FloatField(default=0.0)
    marketCap = models.FloatField(null=True, blank=True, default=0.0)
    peRatio = models.FloatField(null=True, blank=True, default=0.0)
    week52High = models.FloatField(null=True, blank=True, default=0.0)
    week52Low = models.FloatField(null=True, blank=True, default=0.0)
    returnYTD = models.FloatField(null=True, blank=True, default=0.0)
    current_value = models.FloatField(default=0.0)
