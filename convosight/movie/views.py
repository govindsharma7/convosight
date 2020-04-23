from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from convosight.movie.models import Movie
from convosight.movie.serializers import MovieSerializer


# Create your views here.
class MovieAPIView(APIView):
    """docstring for Movie API View"""

    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data

        movie_serializer = MovieSerializer(data=data)
        if not movie_serializer.is_valid():
            return Response({
                'error': movie_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        movie_serializer.save()
        return Response({
            'success': 'Cinema added successfully',
            'data': movie_serializer.data
        }, status=status.HTTP_201_CREATED)


class MoviesList(generics.ListAPIView):
    """docstring for Movies List"""
    model = Movie
    permission_classes = (AllowAny,)
    serializer_class = MovieSerializer

    def get_queryset(self):
        return Movie.objects.all()
