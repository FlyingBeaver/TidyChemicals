from django.test import TestCase, Client
from django.urls import reverse
from chemicals.tests.loader import main
from chemicals.models import Chemical
from profiles.views import logout_invisible


class TestLoader(TestCase):
    def setUp(self):
        client = Client()
        response1 = client.post(
            '/registration/',
            {'username': 'DarthVader',
             'password1': 'doEiusmod1',
             'password2': 'doEiusmod1'}
        )
        response2 = client.get(reverse(logout_invisible))
        response3 = client.post(
            '/registration/',
            {'username': 'BillieEilish',
             'password1': 'temporIncididunt2',
             'password2': 'temporIncididunt2'}
        )
        response4 = client.post(
            '/registration/',
            {'username': 'LarysaHrybalova',
             'password1': 'utLaboreEt3',
             'password2': 'utLaboreEt3'}
        )

    def test_main(self):
        main()
        self.assertEqual(Chemical.objects.all().count(), 7)
