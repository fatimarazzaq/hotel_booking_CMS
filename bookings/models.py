from django.db import models
from ContentUploader.models import MarriageHall
from users.models import Customer

# Create your models here.


class Booking(models.Model):
    marriagehall = models.ForeignKey(MarriageHall, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.marriagehall.title} is booked from {self.check_in} to {self.check_out}'
