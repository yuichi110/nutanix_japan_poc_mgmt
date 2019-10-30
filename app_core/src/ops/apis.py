from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from .models import Asset

from uuid import UUID
import json

