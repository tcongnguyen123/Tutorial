###########---Views----###########
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from api.models.post import Blog
from api.models.deleted_log import DeletedLog
from api.models.updated_log import LogUpdated
from .serializers import BlogSerializer,DeletedLogSerializer,LogUpdatedSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from .pagination import StandardPagination
from copy import deepcopy