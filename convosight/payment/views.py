from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from convosight.Payment.serializers import PaymentSerializer


# Create your views here.
class PaymentAPIView(APIView):
    """docstring for Payment API View"""

    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data

        payment_serializer = PaymentSerializer(data=data)
        if not payment_serializer.is_valid():
            return Response({
                'error': PaymentSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        payment_serializer.save()
        return Response({
            'success': 'Payment done successfully',
            'data': payment_serializer.data
        }, status=status.HTTP_201_CREATED)
