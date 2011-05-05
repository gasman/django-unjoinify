from django.test import TestCase

from unjoinify.tests.models import Festival, Award, Presenter
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
				actor.surname AS nominations__movie__actors__surname,
				tests_presenter.id AS presenter__id,
				tests_presenter.name AS presenter__name
			FROM
				tests_award
				LEFT JOIN tests_nomination ON (tests_award.id = tests_nomination.award_id)
				LEFT JOIN tests_movie ON (tests_nomination.movie_id = tests_movie.id)
				LEFT JOIN tests_movie_producers ON (tests_movie.id = tests_movie_producers.movie_id)
				LEFT JOIN tests_person AS producer ON (tests_movie_producers.person_id = producer.id)
				LEFT JOIN tests_person_movies_acted_in ON (tests_person_movies_acted_in.movie_id = tests_movie.id)
				LEFT JOIN tests_person AS actor ON (tests_person_movies_acted_in.person_id = actor.id)
				LEFT JOIN tests_presenter ON (tests_award.presenter_id = tests_presenter.id)
			WHERE
				tests_award.festival_id = %s
			ORDER BY
				tests_award.name,
				tests_nomination.ranking,
				producer.surname,
				actor.surname
		""", (1,))
		
		(award, nominations, presenter) = awards[0]
		self.assertEquals("Best Director", award.name)
		self.assertEquals(3, len(nominations))
		self.assertEquals(None, presenter)
		
		(nomination, movie, producers, actors) = nominations[0]
		self.assertEquals(1, nomination.ranking)
		self.assertEquals("The King's Speech", movie.title)
		self.assertEquals(3, len(producers))
		self.assertEquals("Canning", producers[0].surname)
		self.assertEquals(2, len(actors))
		self.assertEquals("Firth", actors[0].surname)
		
		(award, nominations, presenter) = awards[1]
		self.assertEquals("Best Picture", award.name)
		self.assertEquals("Steven Spielberg", presenter.name)
	
	def test_reverse_one_to_one_relation(self):
		presenters = unjoinify(Presenter, """
			SELECT
				tests_presenter.id,
				tests_presenter.name,
				tests_award.id AS award__id,
				tests_award.name AS award__name
			FROM
				tests_presenter
				LEFT JOIN tests_award ON (tests_presenter.id = tests_award.presenter_id)
		""")
		
		(presenter, award) = presenters[0]
		self.assertEquals("Steven Spielberg", presenter.name)
		self.assertEquals("Best Picture", award.name)
