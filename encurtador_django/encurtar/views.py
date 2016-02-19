import random
import string

import short_url
from django.db.models.aggregates import Count, Sum
from django.http.response import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.utils.baseconv import base62
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from encurtar.models import User, Url
from encurtar.serializers import UserSerializer, UrlSerializer

"""
	Generate short url
"""
def get_short_code(str_site, str):

    length = 6

    char = string.ascii_uppercase + string.digits + string.ascii_lowercase

    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Url.objects.get(pk=str_site+short_id)
        except:
            return str_site+short_id





"""
	GET: List all users with your urls
		Path: /api/users
"""
@api_view(['GET'])
def users_list(request):

	user = User.objects.all()

	serialize = UserSerializer(user, many=True)

	return Response(serialize.data)





"""
	POST: Create a user by your name from request post
		Post Data: {name: username_here}
		Path: /api/user
"""
@api_view(['POST'])
def user_list(request):

	serializer = UserSerializer(data={"name": request.POST['id']})

	if serializer.is_valid():

		serializer.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





"""
	GET: Show a user with your urls
	DELETE: Delete a user by user_id from request data
	Path: /api/user/:user_id
"""
@api_view(['GET', 'DELETE'])
def user_operation(request, pk):

	if request.method == 'GET':

		try:

			user = User.objects.get(pk=pk)

			serializer = UserSerializer(user)

			return Response(serializer.data, status.HTTP_302_FOUND)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'DELETE':

		try:

			user = User.objects.get(pk=pk)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		user.delete()

		return Response(status=status.HTTP_200_OK)





@api_view(['POST', 'GET', 'DELETE'])
@csrf_exempt
def url_operation(request, pk):

	if request.method == 'GET':
		try:

			url = Url.objects.get(pk=pk)

			url.hits = url.hits + 1
			url.save()

			return HttpResponseRedirect(url.url)
		except Url.DoesNotExist:
			return HttpResponseNotFound('<h1>Page not found</h1>')

	if request.method == 'POST':

		try:
			user = User.objects.get(pk=pk)

			url = request.POST['url']
			shortUrl = get_short_code(request.scheme + "://" + request.META['HTTP_HOST'] + "/api/url/", url)

			serializer = UrlSerializer(data={"url": request.POST['url'], 'shortUrl': shortUrl})

			if serializer.is_valid():

				data =  serializer.data
				dataAux = serializer.data

				data['user'] = user

				url = Url.objects.create(**data)

				dataAux['id'] = url.id
				dataAux['hits'] = url.hits

				return Response(dataAux, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'DELETE':

		try:

			url = Url.objects.get(pk=pk)
		except Url.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		url.delete()

		return Response(status=status.HTTP_200_OK)





@api_view(['GET'])
def url_stats(request, pk):

	try:
		url = Url.objects.get(pk=pk)

		serialize = UrlSerializer(url)

		return Response(serialize.data, status=status.HTTP_302_FOUND)
	except Url.DoesNotExist:
		Response(status=status.HTTP_404_NOT_FOUND)





@api_view(['GET'])
def user_stats(request, pk):

	try:

		user = User.objects.get(pk=pk)
		urls = user.urls.order_by('-hits')

		serializer = UrlSerializer(urls, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)
	except User.DoesNotExist:
		Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def global_stats(request):

	users = User.objects.all()
	parseUsers = users.annotate(s_hits=Sum('urls__hits'))

	url = Url.objects.all()
	ordenedUrl = url.order_by('-hits')[:10]

	serializer = UrlSerializer(ordenedUrl, many=True)

	countHits = 0
	for user in parseUsers:
		countHits += user.s_hits

	data = {
		'hits': countHits,
		'urlCount': url.count(),
		'topUrls': serializer.data
	}

	return Response(data, status=status.HTTP_200_OK)

def url_short(request, short):

	try:

		url = Url.objects.filter(shortUrl__contains=short)[0]

		url.hits = url.hits + 1
		url.save()

		return HttpResponseRedirect(url.url)
	except Url.DoesNotExist:
		return HttpResponseNotFound('<h1>Page not found</h1>')