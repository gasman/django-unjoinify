from django.db import models

class Festival(models.Model):
	name = models.CharField(max_length = 200)

class Award(models.Model):
	name = models.CharField(max_length = 200)
	festival = models.ForeignKey('Festival', related_name = 'awards')

class Movie(models.Model):
	title = models.CharField(max_length = 200)
	producers = models.ManyToManyField('Person', related_name = 'movies_produced')

class Nomination(models.Model):
	movie = models.ForeignKey('Movie', related_name = 'nominations')
	award = models.ForeignKey('Award', related_name = 'nominations')
	ranking = models.IntegerField()

class Person(models.Model):
	first_name = models.CharField(max_length = 30)
	surname = models.CharField(max_length = 30)
	movies_acted_in = models.ManyToManyField('Movie', related_name = 'actors')
