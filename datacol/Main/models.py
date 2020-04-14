from datetime import datetime
from django.db import models
import django
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Language(models.Model):
    language = models.CharField(unique=True, max_length=20)
    date_time = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.language

class Error(models.Model):
    time = models.DateTimeField(default=datetime.utcnow())
    error_types = (
        ('Timeout', 'Timeout'),
        ('Privacy Issue', 'Privacy')
    )
    error_type = models.TextField(choices=error_types)
    error_checked = models.BooleanField(default=False)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return f'{self.error_type}---{self.time}'


class Reported(models.Model):
    pass
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(null=True, blank=True)
    posted_by = models.IntegerField(null=True, blank=True)
    date_posted = models.DateTimeField(default=django.utils.timezone.now())

    class Meta:
        ordering = ['date_posted']

    def __str__(self):
        return f"{self.title}"