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
				tests_person.id AS nominations__movie__producers__id,
				tests_person.first_name AS nominations__movie__producers__first_name,
				tests_person.surname AS nominations__movie__producers__surname
			FROM
				tests_award
				LEFT JOIN tests_nomination ON (tests_award.id = tests_nomination.award_id)
				LEFT JOIN tests_movie ON (tests_nomination.movie_id = tests_movie.id)
				LEFT JOIN tests_movie_producers ON (tests_movie.id = tests_movie_producers.movie_id)
				LEFT JOIN tests_person ON (tests_movie_producers.person_id = tests_person.id)
			WHERE
				tests_award.festival_id = %s
			ORDER BY
				tests_award.name,
				tests_nomination.ranking
		""", (1,))
		
		(award, nominations) = awards[0]
		self.assertEquals("Best Director", award.name)
		self.assertEquals(3, len(nominations))
		
		(nomination, movie, producers) = nominations[0]
		self.assertEquals(1, nomination.ranking)
		self.assertEquals("The King's Speech", movie.title)
		self.assertEquals(3, len(producers))
		