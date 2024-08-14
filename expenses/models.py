from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.amount} - {self.category.name} ({self.user.username})"
    
class Transfer(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transfers', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transfers', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Transfer from {self.sender} to {self.receiver} - {self.amount}"