from rest_framework.generics import GenericAPIView
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from utils import choices as choices_

from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, 
    RetrieveModelMixin, UpdateModelMixin, 
    DestroyModelMixin
    )

@api_view(['GET'])
@api_view([IsAuthenticated])
def get_season_choices(request):
    season_choices=[{"key": item.value, "label": item.label} for item in choices_.SeasonChoices]
    return response.Response(season_choices, status=status.HTTP_200_OK)

