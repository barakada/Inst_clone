from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

def user_directory_path(instance,filename):
    return f"user_{instance.user.id}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path,null=True,default='img/def_avatar.png')
    bio = models.CharField(max_length=200,null=True,blank=True)
    location = models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"



@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(instance,**kwargs):
    Profile.objects.update_or_create(user=instance,defaults={})
