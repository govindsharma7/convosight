from django.test import TestCase
from convosight.address.models import Address


class AddressTestCase(TestCase):
    """docstring for AddressTestCase"""

    def setUp(self):
        Address.objects.create(
            city='dehradun',
            state='uttarakhand',
            country='india',
            zipcode='248001',
            address1='Dalanwala'
        )

    def test_login(self):
        """docstring for user login"""

        address = Address.objects.get(
            city="dehradun")
        self.assertEqual(address.city, 'dehradun')
