import jwt
import logging
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.signals import user_logged_in

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from convosight.accounts.models import User

log = logging.getLogger(__name__)


class CreateUserAPIView(APIView):
    """
    docstring for CreateUserAPIView

    Create User API:
    :params first_name
    :params last_name
    :params email
    :params password
    :return response with token (auto-login)
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data

        try:
            user = User.objects.create_user(
                first_name=user.get('first_name'),
                last_name=user.get('last_name'),
                email=user.get('email').lower(),
                password=user.get('password')
            )

            # host_name = request.get_host()
            log.info(str(user.email) + " - has signed up")

            user_details = get_token(user, user.email, request)

            return Response(user_details, status=status.HTTP_200_OK)

        except IntegrityError:
            error_msg = 'Email already exist'
            log.error(str(user.get('email').lower()) + " - " + error_msg)
            return Response({
                'status': 'error', 'message': error_msg
            }, status=status.HTTP_403_FORBIDDEN)


class AuthenticateUserAPIView(APIView):
    """
    docstring for AuthenticateUserAPIView

    Login User API:
    :params email
    :params password
    :return response with token
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        if not ('email' in request.data and 'password' in request.data):
            error_msg = 'please provide a email and a password'
            log.error(str(request.data.get('email')) + " - " + error_msg)
            res = {'error': error_msg}
            return Response(res)
        email = request.data['email'].lower()
        password = request.data['password']
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            error_msg = 'Email or password is incorrect'
            log.error(str(email) + " - " + error_msg)
            res = {'error': error_msg}
            return Response(res, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            error_msg = 'Authentication Failed due to unmatched credentials'
            log.error(str(email) + " - " + error_msg)
            res = {'error': error_msg}
            return Response(res, status=status.HTTP_403_FORBIDDEN)

        user_details = get_token(user, email, request)

        return Response(user_details, status=status.HTTP_200_OK)


def get_token(user, email, request):
    '''
    docstring for get_token

    :params user
    :params email
    :params request
    :return token and user object deetails
    '''

    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    user_details = {}
    name = user.get_full_name()
    user_details['uuid'] = user.id
    user_details['full_name'] = name
    user_details['email'] = user.email
    user_details['token'] = token
    msg = 'User Logged In'
    log.info(str(email) + " - " + msg)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return user_details
