from django.db import models

# Create your models here.


class UpdateList(models.Model):
    objects = None
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Item(models.Model):
    updatelist = models.ForeignKey(UpdateList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text
