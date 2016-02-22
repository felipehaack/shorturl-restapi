import random
import string

from django.db.models.aggregates import Sum
from django.http.response import HttpResponseRedirect, HttpResponseNotFound
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shortcut.settings import PATH_URL_SHORT
from shorturl.models import User, Url
from shorturl.serializers import UserSerializer, UrlSerializer

"""
	Generate short url
"""
def get_short_code():

    length = 8

    char = string.ascii_uppercase + string.digits + string.ascii_lowercase

    while True:

        short_id = ''.join(random.choice(char) for x in range(length))

        try:

			temp = Url.objects.get(shortUrl__contains=short_id)
        except:
            return short_id





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
	GET: Show a user with your urls
		Path: /api/user/:user_id
	DELETE: Delete a user by user_id from request data
		Path: /api/user/:user_id
	POST: Create a user by your name from request pos
		Post Data: {id: username}
		Path: /api/user
"""
@api_view(['POST'])
def user_store(request):

	print request.POST

	if request.POST.get('id'):

		serializer = UserSerializer(data={"name": request.POST.get('id')})

		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def user_operations(request, pk):

	if request.method == 'GET':

		try:

			user = User.objects.get(pk=pk)

			serializer = UserSerializer(user)

			return Response(serializer.data, status.HTTP_200_OK)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)


	if request.method == 'DELETE':

		try:

			user = User.objects.get(pk=pk)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		user.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)




"""
	GET: Get URL from url path and redirect it
		Path: /api/url/:url_id
	POST: Create an URL by user_id from url path with url website by request post
		Post Data: {url: url_website}
		Path: /api/user
	DELETE: Delete an URL from url path
		Path: /api/url/:url_id
"""
@api_view(['GET', 'POST', 'DELETE'])
def url_operations(request, pk):

	if request.method == 'GET':

		try:

			url = Url.objects.get(pk=pk)

			url.hits = url.hits + 1
			url.save()

			return HttpResponseRedirect(url.url)
		except Url.DoesNotExist:
			return HttpResponseNotFound('<h1>Page not found</h1>')


	if request.method == 'POST':

		if request.POST.get('url'):

			try:

				user = User.objects.get(pk=pk)

				url = request.POST['url']

				shortUrl = request.scheme + "://" + request.META['HTTP_HOST'] + PATH_URL_SHORT + get_short_code()

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
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)


	if request.method == 'DELETE':

		try:

			url = Url.objects.get(pk=pk)
		except Url.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		url.delete()

		return Response(status=status.HTTP_200_OK)




"""
	GET: return URL struct by url_id from url path
		Path: /api/stats/:url_id
"""
@api_view(['GET'])
def url_stats(request, pk):

	try:
		url = Url.objects.get(pk=pk)

		serialize = UrlSerializer(url)

		return Response(serialize.data, status=status.HTTP_302_FOUND)
	except Url.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)




"""
	GET: return ALL URLs from user by user_id from url path ordened by hits
		Path: /api/user/:user_id/stats
"""
@api_view(['GET'])
def user_stats(request, pk):

	try:

		user = User.objects.get(pk=pk)

		urls = user.urls.order_by('-hits')

		serializer = UrlSerializer(urls, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)
	except User.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)




"""
	GET: generate a JSON with all count hits and url stored, and the five top url most accessed
		Path: /api/stats/
"""
@api_view(['GET'])
def global_stats(request):

	users = User.objects.all()

	if(users.count() > 0):

		url = Url.objects.all()

		if url.count() > 0:

			ordenedUrl = url.order_by('-hits')[:10]

			serializer = UrlSerializer(ordenedUrl, many=True)

			countHits = 0
			parseUsers = users.annotate(s_hits=Sum('urls__hits'))
			for user in parseUsers:
				countHits += user.s_hits

			data = {
				'hits': countHits,
				'urlCount': url.count(),
				'topUrls': serializer.data
			}

			return Response(data, status=status.HTTP_200_OK)

	return Response(status=status.HTTP_204_NO_CONTENT)




"""
	Redirect URL by shortUrl from url path
"""
def url_redirect_by_short_code(request, short):

	try:

		url = Url.objects.filter(shortUrl__contains=short)[0]

		url.hits = url.hits + 1
		url.save()

		return HttpResponseRedirect(url.url)
	except Url.DoesNotExist:
		return HttpResponseNotFound('<h1>Page not found</h1>')