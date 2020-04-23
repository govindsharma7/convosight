from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from convosight.booking.models import Booking
from convosight.payment.constants import PaymentStatus
from convosight.booking.constants import BookingStatus
from convosight.booking.serializers import BookingSerializer
from convosight.payment.serializers import PaymentSerializer


# Create your views here.
class BookingAPIView(APIView):
    '''docstring for Booking API View'''

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id

        booking_serializer = BookingSerializer(data=data)
        if not booking_serializer.is_valid():
            return Response({
                'error': booking_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        booking_serializer.save()

        booking_data = booking_serializer.data

        amount = data.get('seat_selected') * booking_data.get(
            'show_details').get('ticket_price')

        payment_data = {
            'booking': booking_data.get('id'),
            'status': PaymentStatus.SUCCESS,
            'amount': amount
        }

        payment_serializer = PaymentSerializer(data=payment_data)
        if not payment_serializer.is_valid():
            return Response({
                'error': payment_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        payment_serializer.save()

        booking_obj = Booking.objects.filter(id=booking_data.get('id'))
        booking_obj.update(status=BookingStatus.CONFIRM)

        booking_detail = BookingSerializer(booking_obj.first()).data

        return Response({
            'success': 'Booked successfully',
            'data': booking_detail
        }, status=status.HTTP_201_CREATED)


class BookingListAPIView(generics.ListAPIView):
    """docstring for Movies List"""
    model = Booking
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
