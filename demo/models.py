from django.db import models

# Create your models here.


class Demo(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_time', )
