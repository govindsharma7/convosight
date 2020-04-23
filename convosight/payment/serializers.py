from rest_framework import serializers

from convosight.booking.models import Booking
from convosight.payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    ''' docstring for Payment Serializer '''
    booking = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Booking.objects.all()
    )

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validate_data):
        payment = Payment.objects.create(
            **validate_data
        )
        return payment

    def update(self, instance, validated_data):
        payment = super(Payment, self).update(
            instance, validated_data)
        return payment
