from django.db import models

class LostItem(models.Model):

    item_name = models.CharField(max_length=200)
    description = models.TextField()
    location_lost = models.CharField(max_length=200)
    date_lost = models.DateField()
    reward = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="lost_items/", blank=True, null=True)

    def __str__(self):
        return self.item_name


class FoundItem(models.Model):

    item_name = models.CharField(max_length=200)
    description = models.TextField()
    location_found = models.CharField(max_length=200)
    date_found = models.DateField()
    image = models.ImageField(upload_to="found_items/", blank=True, null=True)

    def __str__(self):
        return self.item_name