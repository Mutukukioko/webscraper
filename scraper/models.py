from django.db import models

# Create your models here.
class Email(models.Model):
        url = models.URLField()
        email = models.EmailField()

        def __str__(self) -> str:
                return self.email