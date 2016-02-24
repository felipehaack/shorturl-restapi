from rest_framework import serializers
from shorturl.models import User, Url

class UrlSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Url;
		fields = ('id', 'hits', 'url', 'shortUrl', 'created_at')

class UserSerializer(serializers.HyperlinkedModelSerializer):

	urls = UrlSerializer(many=True, read_only=True)

	class Meta:
		model = User
		fields = ('id', 'name', 'urls')