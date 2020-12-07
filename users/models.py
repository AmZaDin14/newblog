from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from os.path import basename, splitext


UPLOAD_TO = 'img/profile_pics'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='img/profile_pics/default.webp ', upload_to=UPLOAD_TO)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if splitext(basename(self.image.path)) != '.webp':
            img = Image.open(self.image.path)
            img = img.convert('RGB')
            img_path = splitext(self.image.path)[0]
            img_base = basename(self.image.path)
            img.save(img_path + '.webp', 'webp')
            self.image = UPLOAD_TO + '/' + splitext(img_base)[0] + '.webp'

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
