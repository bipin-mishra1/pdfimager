from django.db import models


class ImageZipFile(models.Model):
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    size = models.IntegerField()
    uuid = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
