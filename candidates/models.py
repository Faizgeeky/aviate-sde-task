from django.db import models

# Create your models here.

class Candidate(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
        ordering = ['name']

    def __str__(self):
        return self.name
