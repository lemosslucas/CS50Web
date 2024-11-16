from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Book(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    language = models.CharField(max_length=20)
    pdf_file = models.FileField(upload_to='media/pdfs')
    cover_image = models.ImageField(upload_to='covers/', blank=True)
    
    def __str__(self):
        return f'PDF:{self.name} by {self.user}'
    
class Words(models.Model):
    word_source = models.CharField(max_length=255)
    word_target = models.CharField(max_length=255)
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="words")

    def __str__(self):
        return f"@{self.user}: ({self.word_source} ({self.source_language})) -> ({self.word_target} ({self.target_language}))"