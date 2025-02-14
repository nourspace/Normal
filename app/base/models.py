from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_quill.fields import QuillField

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="default_avatar.svg")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, verbose_name="Post Title")
    slug = models.SlugField(null=True, blank=True, unique=True)
    content = QuillField()
    is_published = models.BooleanField(null=False, default=True)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_like_url(self):
        return reverse(
            "post:like-toggle",
            kwargs={"slug": self.slug},
        )

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} - {self.content[:16]}"
