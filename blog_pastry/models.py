from django.db import models
from user.models import User
from django.utils.text import slugify
from .slug import generate_slug

from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self) -> str:
      return self.title
    
    def save(self, *args, **kwargs):
      self.slug = slugify(self.title)
      super(Category, self).save(*args, **kwargs)



class Tag(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self) -> str:
      return self.title
    
    def save(self, *args, **kwargs):
      self.slug = slugify(self.title)
      super(Tag, self).save(*args, **kwargs)

class Article(models.Model):
    user = models.ForeignKey(User, related_name='user_articles', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='user_likes', blank=True)

    title = models.CharField(max_length=255)
    description = RichTextField()
    category = models.ForeignKey(Category, related_name='categorie_aticles', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='tag_articles', blank=True)
    slug = models.SlugField(null=True, blank=True)
    banner = models.ImageField(upload_to='aticle_banners')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def tag_articles(self):
        return ', '.join(tag.title for tag in self.tags.all()) if self.tags.exists() else ''

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)

    article = models.ForeignKey(Article, related_name='article_comments', on_delete=models.CASCADE)

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
      return self.text
    

class Response(models.Model):
    user = models.ForeignKey(User, related_name='user_response', on_delete=models.CASCADE)

    comment = models.ForeignKey(Comment, related_name='comment_response', on_delete=models.CASCADE)

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
      return self.text
    

