from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class post(models.Model):
    postTitle = models.CharField(max_length=150)
    postImage = models.ImageField(upload_to='image/', blank=True, null=True)
    description = models.TextField()
    createdOn = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.postTitle
    def getTitle(self):
        return self.postTitle
        
    def shordescription(self):
        return self.description[:250]

class postLike(models.Model):
    post = models.OneToOneField(post, on_delete=models.CASCADE)
    totalLike = models.IntegerField(default=0)

    def __str__(self):
        return self.post.postTitle
