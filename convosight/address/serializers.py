from rest_framework import serializers
from convosight.address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """ docstring for Address Serializer """

    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validate_data):
        return Address.objects.create(
            **validate_data
        )

    def update(self, instance, validate_data):
        loc = super(AddressSerializer, self).update(instance, validate_data)
        return loc
