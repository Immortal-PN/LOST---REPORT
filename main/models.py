from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('electronics','Electronics'),
    ('documents','Documents'),
    ('wallet','Wallet'),
    ('keys','Keys'),
    ('other','Other')
]


class LostItem(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)

    location = models.CharField(max_length=200)

    date_lost = models.DateField()

    image = models.ImageField(upload_to='lost_items/',blank=True,null=True)

    proof_document = models.FileField(upload_to='proof_docs/',blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FoundItem(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    matched_lost_item = models.ForeignKey(
        LostItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matched_found_reports",
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)

    location = models.CharField(max_length=200)

    date_found = models.DateField()

    found_time = models.TimeField(blank=True, null=True)

    handover_location = models.CharField(max_length=200, blank=True)

    image = models.ImageField(upload_to='found_items/',blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):

    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")

    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
    
class ClaimRequest(models.Model):

    item = models.ForeignKey(LostItem,on_delete=models.CASCADE)

    claimant = models.ForeignKey(User,on_delete=models.CASCADE)

    message = models.TextField()

    status = models.CharField(max_length=20,default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.claimant} - {self.item}"
