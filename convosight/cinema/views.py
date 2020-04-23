import json
import coreapi

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework.schemas import AutoSchema
from convosight.cinema.models import (
    CinemaShow, Cinema
)
from convosight.cinema.serializers import (
    CinemaSerializer, CinemaShowSerializer
)


# Create your views here.
class CinemaViweSchema(AutoSchema):
    """
        docstring for CinemaViweSchema
        Thid is defined due to Swagger Documentation
    """

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field(
                    name='name',
                    required=True)
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class CinemaShowViweSchema(AutoSchema):
    """
        docstring for CinemaShowViweSchema
        Thid is defined due to Swagger Documentation
    """

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field(
                    'cinema', 'movie', 'show_date', 'show_start',
                    'show_end', 'seat_available', 'ticket_price'
                )
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class CinemaAPIView(APIView):
    """
    docstring for Cinema API View
    """

    schema = CinemaViweSchema()
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data

        cinema_serializer = CinemaSerializer(data=data)
        if not cinema_serializer.is_valid():
            return Response({
                'error': cinema_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        cinema_serializer.save()
        return Response({
            'success': 'Cinema added successfully',
            'data': cinema_serializer.data
        }, status=status.HTTP_201_CREATED)


class CinemaShowAPIView(APIView):
    """docstring for Cinema Show API View"""

    schema = CinemaShowViweSchema()
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data

        cinema_show_serializer = CinemaShowSerializer(data=data)
        if not cinema_show_serializer.is_valid():
            return Response({
                'error': cinema_show_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        cinema_show_serializer.save()
        return Response({
            'success': 'Cinema Show added successfully',
            'data': cinema_show_serializer.data
        }, status=status.HTTP_201_CREATED)


class CinemaList(generics.ListAPIView):
    model = Cinema
    permission_classes = (AllowAny,)
    serializer_class = CinemaSerializer

    def get_queryset(self):
        return Cinema.objects.all()


class FilterCinemaShowList(generics.ListAPIView):
    model = CinemaShow
    permission_classes = (AllowAny,)
    serializer_class = CinemaShowSerializer

    def get_queryset(self):
        data = CinemaShow.objects.all()

        try:
            city = self.request.GET.get('city')
            movie = self.request.GET.get('movie')

            if city:
                data = data.filter(cinema__address__city=city)

            if movie:
                data = data.filter(movie__name=city)
        except (TypeError, ValueError):
            data = data.none()

        return data
