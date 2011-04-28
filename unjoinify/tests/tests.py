from django.test import TestCase

from unjoinify.tests.models import Festival, Award

class TestStuff(TestCase):
	fixtures = ['unjoinify_testdata.json']
	
	def test_thing(self):
		self.assertEquals("83rd Academy Awards", Festival.objects.get(pk=1).name)
