from django.db import models

# Create your models here.

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploaded_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class FileColumn(models.Model):
    file = models.ForeignKey(UploadedFile, related_name='columns', on_delete=models.CASCADE)
    column_name = models.CharField(max_length=255)