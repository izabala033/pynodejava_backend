from functools import reduce
from django.shortcuts import render
from django.utils import translation
from django.utils.timezone import now
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.shortcuts import  redirect
from django.db.models import Q
from django.core.cache import cache
from django.http import HttpResponse
from django.db import connection

import requests

from location.models import Location, SherpaUser
from location.serializers import LocationSerializer


class LocationViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        return LocationSerializer

    def get_queryset(self):
        return Location.objects.all()
    
    @action(detail=False, methods=['get'])
    def register(self, request):
        name = request.GET.get('name', None)
        cp = request.GET.get('cp', None)
        cc = request.GET.get('countryCode', None)
        
        if cp == None or name == None or cp == "" or name == "":
            content = {'Error': 'name or cp parameter not found'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)        
        
        geo_api = "http://api.geonames.org/postalCodeSearchJSON"

        # parameters to send along with REST API Endpoint
        payload = {'postalcode': cp, 'username': name}
        
        #optional parameter
        if cc != None and cc != "":
            payload["countryCode"]=cc

        # make a requests call using GET (including parameters)
        r = requests.get(geo_api, params=payload)
        
        # get the returns json data
        json_data = r.json()
        
        #check geoname response is valid
        if r.status_code != 200:
            return Response(json_data, status=r.status_code)
        
        if not ("postalCodes" in json_data):
            content = {'Error': 'something failed'}
            print(json_data)
            return Response(json_data, status=status.HTTP_400_BAD_REQUEST)
        
        #when invalid / non existent cp is used
        if json_data["postalCodes"] == []:
            content = {'Error': 'city not found, check that data is correct'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        first_place = json_data["postalCodes"][0]["placeName"]
        
        #just in case
        if first_place == "":
            content = {'Error': 'Unexpected error'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        newUser = SherpaUser()
        newUser.name = name
        newUser.save()
        
        location = Location()
        location.cp = cp
        location.city = first_place
        location.name = newUser
        location.save()
        
        

        content = {'Success': f'City {first_place} is now saved with current username'}
        return Response(content, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def getLocations(self, request):
        return Response(LocationSerializer(self.get_queryset(), many=True, context={'request': request}).data, status=status.HTTP_200_OK)
    
    
    