from django.conf import settings
from rest_framework import serializers

from convosight.movie.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    ''' docstring for Movie Serializer '''
    release_date = serializers.DateTimeField(
        format=settings.GLOBAL_DATE_FORMAT,
        input_formats=settings.INPUT_DATE_FORMATS
    )

    class Meta:
        model = Movie
        fields = (
            'id', 'name', 'release_date'
        )

    def create(self, validate_data):
        movie = Movie.objects.create(
            **validate_data
        )
        return movie

    def update(self, instance, validated_data):
        movie = super(Movie, self).update(
            instance, validated_data)
        return movie
