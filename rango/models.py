from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        # Ensure views is non-negative
        if self.views < 0:
            self.views = 0

        # Create slug from name
        self.slug = slugify(self.name)

        # Override save() method
        # super() previously super(Category, self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    first_visit = models.DateTimeField(default=datetime.now)
    last_visit = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # Link user profile to user model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
