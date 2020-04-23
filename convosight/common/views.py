from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from convosight.accounts.models import User

log = logging.getLogger(__name__)


class PopulateDemmyDataAPIView(APIView):
    """
    docstring for PopulateDemmyDataAPIView

    Populating Dummy Data to all tables

    """
    permission_classes = (AllowAny,)

    def get(self, request):
        pass
