from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime


# Create your models here.
User = get_user_model()

class Board(models.Model):  
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

   
    def __unicode__(self):
        return u'Profile of user: %s' % self.title

class List(models.Model):
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="lists")
    title = models.CharField(max_length=255, blank=False, null=False)
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Card(models.Model):
    list = models.ForeignKey(
        List, on_delete=models.CASCADE, related_name="lists")
    title = models.CharField(max_length=255, blank=False, null=False)
    due_date =  models.DateField(default=datetime.date.today,blank=True, null=True)
    attachments = models.FileField(upload_to='attachments',blank=False, null=False)
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

   