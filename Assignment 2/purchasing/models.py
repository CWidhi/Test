from django.db import models
from django.utils.timezone import now

class PurchaseHeader(models.Model):
    code = models.CharField(max_length=10, unique=True)
    date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    def soft_delete(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()
            
            for detail in self.details.all():
                detail.soft_delete()
                
    def restore(self):
        if self.is_deleted:
            self.is_deleted = False
            self.save()
            
            for detail in self.details.all():
                detail.restore()
                
class PurchaseDetail(models.Model):
    item_code = models.ForeignKey('items.Items', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    header_code = models.ForeignKey(PurchaseHeader, related_name='details', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    def delete(self):
        if not self.is_deleted:
            item = self.item_code
            item.stock -= self.quantity
            item.balance -= self.unit_price * self.quantity
            item.save()

        self.is_deleted = True
        self.save()
        
    def restore(self):
        if self.is_deleted:
            item = self.item_code
            item.stock += self.quantity
            item.balance += self.unit_price * self.quantity
            item.save()

        self.is_deleted = False
        self.save()