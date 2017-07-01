from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField()
    likes = models.IntegerField()
    
    def __unicode__(self):
        return self.name
    
class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    view = models.IntegerField()
    
    def __unicode__(self):
        return self.title
    