from django.conf import settings
from rest_framework import serializers

from convosight.cinema.models import (
    Cinema, CinemaShow
)
from convosight.movie.models import Movie
from convosight.address.models import Address

from convosight.movie.serializers import MovieSerializer
from convosight.address.serializers import AddressSerializer


class CinemaSerializer(serializers.ModelSerializer):
    ''' docstring for Cinema Serializer '''

    address = AddressSerializer()

    class Meta:
        model = Cinema
        fields = '__all__'

    def get_or_create_address(self, address_dict):
        try:
            return Address.objects.get(
                address1=address_dict.get('address1'),
                city=address_dict.get('city'),
                state=address_dict.get('state'),
                country=address_dict.get('country'),
                zipcode=address_dict.get('zipcode'))
        except Address.DoesNotExist:
            return Address.objects.create(**address_dict)

    def create(self, validated_data):
        address_dict = validated_data.get('address')
        address = self.get_or_create_address(address_dict)
        validated_data['address'] = address
        cinema = Cinema.objects.create(
            **validated_data
        )
        return cinema

    def update(self, instance, validated_data):
        validated_data.pop('address')
        cinema = super(Cinema, self).update(
            instance, validated_data)
        return cinema


class CinemaShowSerializer(serializers.ModelSerializer):
    ''' docstring for Cinema Show Serializer '''

    cinema = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Cinema.objects.all()
    )

    movie = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Movie.objects.all()
    )

    show_date = serializers.DateField(
        format=settings.GLOBAL_DATE_FORMAT,
        input_formats=settings.INPUT_DATE_FORMATS
    )
    show_start = serializers.TimeField(
        format=settings.TIME_FORMAT,
        input_formats=settings.INPUT_TIME_FORMAT
    )
    show_end = serializers.TimeField(
        format=settings.TIME_FORMAT,
        input_formats=settings.INPUT_TIME_FORMAT
    )

    class Meta:
        model = CinemaShow
        fields = (
            'id', 'cinema', 'movie', 'show_date',
            'show_start', 'show_end', 'seat_available',
            'ticket_price'
        )

    def create(self, validate_data):
        cinema_show = CinemaShow.objects.create(
            **validate_data
        )
        return cinema_show

    def update(self, instance, validated_data):
        cinema_show = super(CinemaShow, self).update(
            instance, validated_data)
        return cinema_show

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['availability'] = instance.available_seat_count
        if instance.cinema:
            ret['cinema_details'] = CinemaSerializer(instance.cinema).data
        if instance.movie:
            ret['movie_details'] = MovieSerializer(instance.movie).data

        return ret
