from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Show, Booking

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Securely save password using Django's hashing
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ShowSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Show
        fields = ['id', 'movie', 'movie_title', 'screen_name', 'date_time', 'total_seats']

class BookingSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='show.movie.title', read_only=True)
    show_time = serializers.DateTimeField(source='show.date_time', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'show', 'movie_title', 'show_time', 'seat_number', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']
