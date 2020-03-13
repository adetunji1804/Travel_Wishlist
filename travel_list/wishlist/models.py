from django.db import models

#class model with 2 attributes

class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}, visited {self.visited}"

