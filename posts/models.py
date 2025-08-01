from django.db import models
from django.contrib.auth.models import User


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Post(AbstractModel):
    title = models.CharField(max_length=50)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Comment(AbstractModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'comment by {self.author} on {self.post}'