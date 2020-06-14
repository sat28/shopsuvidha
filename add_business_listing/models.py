from django.db import models


class Business(models.Model):
    business_name = models.CharField(max_length=500)
    street_address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='business/')

    def __str__(self):
        return self.business_name
