from django.core import validators
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.core.validators import MinLengthValidator 

# Create your models here.
class Tag(models.Model):
    caption= models.CharField(max_length=10)
    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address=models.EmailField()
    def __str__(self):
        return self.first_name + self.last_name



class post(models.Model):
    title = models.CharField(max_length= 100)
    image=models.ImageField(upload_to = 'posts', null = True)
    excerpt=models.CharField(max_length= 100)
    date = models.DateField(auto_now= True)
    slug=models.SlugField(unique= True, db_index= True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author= models.ForeignKey(Author, on_delete=models.SET_NULL, related_name= "posts", null= True)
    tag= models.ManyToManyField(Tag)
    def __str__(self):
        return self.title
class comments(models.Model):
    username = models.CharField(max_length = 50)
    email = models.EmailField()
    text = models.TextField(max_length = 400)
    post = models.ForeignKey(post,on_delete = CASCADE, related_name = 'comments')