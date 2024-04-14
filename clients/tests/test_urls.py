from django.test import SimpleTestCase
from django.urls import reverse, resolve
from clients.views import index

class TestUrls(SimpleTestCase):
	
	def test_list_url_is_resolved(self):
		url = reverse('index')
		self.assertEquals(resolve(url).func, index)

