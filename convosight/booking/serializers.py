from rest_framework import serializers
from convosight.accounts.models import User
from convosight.booking.models import Booking
from convosight.cinema.models import CinemaShow

from convosight.accounts.serializers import UserSerializer
from convosight.cinema.serializers import CinemaShowSerializer


class BookingSerializer(serializers.ModelSerializer):
    ''' docstring for booking serializer '''

    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all()
    )
    show = serializers.SlugRelatedField(
        slug_field='id',
        queryset=CinemaShow.objects.all()
    )

    class Meta:
        model = Booking
        fields = (
            'id', 'user', 'show', 'seat_selected', 'status'
        )

    def create(self, validate_data):
        booking = Booking.objects.create(
            **validate_data
        )
        return booking

    def update(self, instance, validated_data):
        booking = super(Booking, self).update(
            instance, validated_data)
        return booking

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.user:
            ret['user_details'] = UserSerializer(instance.user).data
        if instance.show:
            ret['show_details'] = CinemaShowSerializer(instance.show).data

        return ret
