from django.test import TestCase
from convosight.movie.models import Movie


class MovieTestCase(TestCase):
    """docstring for MovieTestCase"""

    def setUp(self):

        Movie.objects.create(
            name='Happy New Year',
            release_date='01/10/2019'
        )
        Movie.objects.create(
            name='Happy New Year 2',
            release_date='01/10/2020'
        )

    def test_movie(self):
        """docstring for Get Movie"""

        movie = Movie.objects.get(
            name='Happy New Year'
        )
        self.assertEqual(movie.name, 'Happy New Year')
