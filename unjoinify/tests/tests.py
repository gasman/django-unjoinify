from django.test import TestCase

from unjoinify.tests.models import Festival, Award
from unjoinify import unjoinify

class TestUnjoinify(TestCase):
	fixtures = ['unjoinify_testdata.json']
	
	def test_unjoinify(self):
		awards = unjoinify(Award, """
			SELECT
				tests_award.id,
				tests_award.name,
				tests_nomination.id AS nominations__id,
				tests_nomination.ranking AS nominations__ranking,
				tests_movie.id AS nominations__movie__id,
				tests_movie.title AS nominations__movie__title,
				producer.id AS nominations__movie__producers__id,
				producer.first_name AS nominations__movie__producers__first_name,
				producer.surname AS nominations__movie__producers__surname,
				actor.id AS nominations__movie__actors__id,
				actor.first_name AS nominations__movie__actors__first_name,
				actor.surname AS nominations__movie__actors__surname
			FROM
				tests_award
				LEFT JOIN tests_nomination ON (tests_award.id = tests_nomination.award_id)
				LEFT JOIN tests_movie ON (tests_nomination.movie_id = tests_movie.id)
				LEFT JOIN tests_movie_producers ON (tests_movie.id = tests_movie_producers.movie_id)
				LEFT JOIN tests_person AS producer ON (tests_movie_producers.person_id = producer.id)
				LEFT JOIN tests_person_movies_acted_in ON (tests_person_movies_acted_in.movie_id = tests_movie.id)
				LEFT JOIN tests_person AS actor ON (tests_person_movies_acted_in.person_id = actor.id)
			WHERE
				tests_award.festival_id = %s
			ORDER BY
				tests_award.name,
				tests_nomination.ranking,
				producer.surname,
				actor.surname
		""", (1,))
		
		(award, nominations) = awards[0]
		self.assertEquals("Best Director", award.name)
		self.assertEquals(3, len(nominations))
		
		(nomination, movie, producers, actors) = nominations[0]
		self.assertEquals(1, nomination.ranking)
		self.assertEquals("The King's Speech", movie.title)
		self.assertEquals(3, len(producers))
		self.assertEquals("Canning", producers[0].surname)
		self.assertEquals(2, len(actors))
		self.assertEquals("Firth", actors[0].surname)
