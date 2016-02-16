from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from encurtar.models import User, Url
from encurtar.serializers import UserSerializer, UrlSerializer

@api_view(['GET', 'POST'])
def user_list(request):
	
	if request.method == 'GET':

		user = User.objects.all()
		serializer = UserSerializer(user, many=True)

		return Response(serializer.data)

	if request.method == 'POST':

		serializer = UserSerializer(data=request.data)

		if serializer.is_valid():

			serializer.save()
			
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def user_operations(request, pk):
	
	try:

	    user = User.objects.get(pk=pk)
	except User.DoesNotExist:
	    return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'DELETE':

		user.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)
