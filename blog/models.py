from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from PIL import Image
from os.path import basename, splitext


UPLOAD_TO = 'img'

STATUS = {
    (0, 'Draft'),
    (1, 'Publish')
}


class Categories(models.TextChoices):
    DESAIN_GRAFIS = 'Desain Grafis'
    MIKROTIK = 'Mikrotik'
    PEMROGRAMAN = 'Pemrograman'
    SISTEM_OPERASI = 'Sistem Operasi'
    LAINNYA = 'Lainnya'


class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    category = models.CharField(max_length=50, choices=Categories.choices, default=Categories.LAINNYA)
    thumbnail = models.ImageField(upload_to=UPLOAD_TO, default='img/default.webp')
    excerpt = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post', null=True)
    content = models.TextField()
    featured = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset = Post.objects.all().filter(slug__iexact=original_slug).count()

        count = 1
        slug = original_slug
        while queryset:
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Post.objects.all().filter(slug__iexact=slug).count()

        self.slug = slug

        if self.featured:
            try:
                self.status = 1
                temp = Post.objects.get(featured=True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except Post.DoesNotExist:
                pass

        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.thumbnail.path)
        img = img.convert('RGB')
        img_path = splitext(self.thumbnail.path)[0]
        img_base = basename(self.thumbnail.path)
        img.save(img_path + '.webp', 'webp')
        self.thumbnail = UPLOAD_TO + '/' + splitext(img_base)[0] + '.webp'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return f'Comment {self.body} by {self.name}'
