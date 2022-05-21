from io import BytesIO
from PIL import Image
from django.template.defaultfilters import slugify
from django.core.files import File
from django.db import models
from unidecode import unidecode
from datetime import datetime, timedelta


class Tag(models.Model):
    tagname = models.CharField(max_length=100)

    def __str__(self):
        return self.tagname


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, )
        super().save(*args, **kwargs)


class Post(models.Model):
    category = models.ForeignKey(
        Category, related_name='posts', on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(Tag)
    title = models.CharField(max_length=240)
    text = models.TextField()
    image = models.ImageField(upload_to='news/static/news/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='news/static/news/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    view_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
       return self.title

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(285, 160)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def get_date(self):

        if datetime.now() - timedelta(hours=24) < \
                self.date_added < datetime.now():
            return f"Сегодня, {self.date_added.strftime('%H:%M')}"
        elif datetime.now() > self.date_added > \
                datetime.now() - timedelta(hours=24):
            return f"Вчера, {self.date_added.strftime('%H:%M')}"
        else:
            return self.date_added.strftime('%d.%b.%Y %H:%M')

    def save(self, *args, **kwargs):
        value = unidecode(self.title)
        self.slug = slugify(value)
        super().save(*args, **kwargs)


class PostImage(models.Model):
    post = models.ForeignKey(
        Post, related_name='image_for_post', on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='news/static/news/', blank=True, null=True)

    def save(self):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 695 or img.width > 926:
            output_size = (695, 926)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=False)
    owner = models.ForeignKey(
        'auth.User', related_name='comments', on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Комментарии пользователя {self.owner} ' \
               f'c id номер {self.owner.id} для поста {self.post.id}'

