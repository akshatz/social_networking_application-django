from django.db import models
from PIL import Image
from django_project.settings import AUTH_USER_MODEL


class Profile(models.Model):
    """Updating profile of particular user """
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    friends = models.ManyToManyField("Profile", blank=True)
    image = models.ImageField(default='default.jpg', upload_to="profile_pics", null=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    dateofbirth = models.DateField(null=True)

    def __str__(self):
        return str(self.user.username)

    def __str__(self):
        msg = '{} Profile'.format(self.user.username)
        return msg


def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    img = Image.open(self.image.path)

    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)


class FriendRequest(models.Model):
    """Model has 3 fields:
    sending to user
    recieve form user
    and timestamp
    """
    to_user = models.ForeignKey(AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

