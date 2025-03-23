from django.db import models
from django.utils.timezone import now

class SellHeader(models.Model):
    code = models.CharField(max_length=10, unique=True)
    date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    

class SellDetail(models.Model):
    item_code = models.ForeignKey('items.Items', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    header_code = models.ForeignKey(SellHeader, related_name='details', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)