from django.db import models
from django.conf import settings 
from django.contrib.auth.models import Group

from PIL import Image


# Custom functions
def group_icon_upload_location(instance, filename):
    file_extension = filename.split('.')[-1]
    return f"chartgroup_icons/{instance.name.lower()}.{file_extension}"

# Create your models here.
class Profile (models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'profile')
    status = models.BooleanField(default = False)

    def __str__ (self):
        return f"Profile of {self.user.username}"
        

class ChatGroup(Group):
    """ extend Group model to add extra info"""
    description = models.TextField(blank=True, help_text="description of the group")
    mute_notifications = models.BooleanField(default=False, help_text="disable notification if true")
    icon = models.ImageField(help_text="Group icon", blank=True, upload_to=group_icon_upload_location)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('chat:room', args=[str(self.id)])

    def __str__(self):
        return f'Public Chat Group: {self.name.title()}'
    
    def save(self, *args, **kwargs):
        if self.id:
            try:
                old_intance = ChatGroup.objects.get(id=self.id)
                if self.icon != old_intance.logo:
                    old_intance.icon.delete(False)
            except Exception as e:
                print(e)

        if self.icon:
            super().save(*args, **kwargs)
            img = Image.open(self.icon.path)
            print(img, img.height, img.width)
            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
            img.save(self.icon.path, optimize=True, quality=80)
            
        else:
            return super(ChatGroup, self).save(*args, **kwargs)

