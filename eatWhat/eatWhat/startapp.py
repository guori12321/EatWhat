from django.db import models

class Resraurants(models.Model):
	name = models.Charfield(max_length=50)
	address = models.Charfield(max_length=100)
	city = models.Charfield(max_length=30)
	province = models.Charfield(max_length=30)
	country = models.Charfield(max_length=30)
	website = models.URLfield(max_length=150)
class menu(models.Model):
	series = models.Charfield(max_length=50)
	tastes = models.Charfield(max_length=100)

