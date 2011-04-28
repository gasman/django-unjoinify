from django.db import models

class Festival(models.Model):
	name = models.CharField(max_length = 200)

class Award(models.Model):
	name = models.CharField(max_length = 200)
	festival = models.ForeignKey('Festival', related_name = 'awards')

class Movie(models.Model):
	name = models.CharField(max_length = 200)

class Nomination(models.Model):
	movie = models.ForeignKey('Movie', related_name = 'nominations')
	award = models.ForeignKey('Award', related_name = 'nominations')
