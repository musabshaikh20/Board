from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class UserProfile(models.Model):  
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    user_type = models.CharField(max_length=140,null=False,blank=False)  
   
    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username
