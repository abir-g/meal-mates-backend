from django.db import models

# Create your models here.
class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.ManyToManyField('Ingredient', related_name='meals', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='meals/')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)

    def __str__(self):
        return self.name
