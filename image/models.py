from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from slugify import slugify


def user_directory_path(instance, filename):
    return "courses/user_{0}/{1}".format(instance.user.id, filename)

class Image(models.Model):
    user = models.ForeignKey(User, related_name="images",on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    # url = models.URLField()
    slug = models.SlugField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    image = models.ImageField(upload_to=user_directory_path)
    users_like = models.ManyToManyField(User,related_name="images_like",blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) :
        self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
