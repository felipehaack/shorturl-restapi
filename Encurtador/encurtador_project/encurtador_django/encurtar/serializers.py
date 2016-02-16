from rest_framework import serializers
from encurtar.models import User, Url

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'name')

class UrlSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Url;
		fields = ('id', 'url', 'shorturl', 'hint')