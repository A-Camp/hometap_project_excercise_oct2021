# views.py
# Create your views here.
from .models import Home
from .serializers import HomeSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrSuperUser
from septic_api import serializers

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsOwnerOrSuperUser])
def home(request, format=None):
    """
    Allow user to create a new home and view ones they have.

    Why create? In order to limit how often we access the 3rd party API we should call it as little as possible. 
    So I've decided to put the API check in the create function (see: `septic_api/serialzers.py`)

    Why get? For ease of use with the browsable API and when testing other portions of this API.
    In reality this endpoint or something similar might already exist in a larger codebase.
    """
    if request.method == 'GET':
        homes = Home.objects.filter(owner=request.user)
        serializer = HomeSerializer(homes, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = HomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated, IsOwnerOrSuperUser])
def home_by_id(request, pk, format=None):
    """
    Read, or update a home by id/primary_key.

    Why read? So that the front-end can check if the home has a septic tank. 
    Allows the front-end checking of septic-tank status to be un-coupled from the create action.
    
    Why update? So that a user who has a septic tank can provide extra information.
    """
    try:
        home = Home.objects.get(id=pk)
    except Home.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HomeSerializer(home)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = HomeSerializer(home, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




