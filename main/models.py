from django.db import models

class LostItem(models.Model):

    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location_lost = models.CharField(max_length=100)
    date_lost = models.DateField()

    image = models.ImageField(upload_to='lost_items/', null=True, blank=True)

    def __str__(self):
        return self.item_name


class FoundItem(models.Model):

    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location_found = models.CharField(max_length=100)
    date_found = models.DateField()

    image = models.ImageField(upload_to='found_items/', null=True, blank=True)

    def __str__(self):
        return self.item_name