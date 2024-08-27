from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    nickname = models.CharField(max_length=50)
    email = models.EmailField()

    status_choices = (('Pro', 'Pro'), ('Simple', 'Simple'),)
    status = models.CharField(max_length=10, choices=status_choices)

    def __str__(self):
        return self.nickname


class Country(models.Model):
    country_name = models.CharField(max_length=50)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=50)
    bio = models.TextField()
    age = models.IntegerField()
    director_image = models.ImageField(upload_to='director_images/')

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=50)
    bio = models.TextField()
    age = models.IntegerField()
    actor_image = models.ImageField(upload_to='actor_images/')

    def __str__(self):
        return self.actor_name


class Janre(models.Model):
    janre_name = models.CharField(max_length=50)

    def __str__(self):
        return self.janre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    date_published = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actor = models.ManyToManyField(Actor)
    janre = models.ManyToManyField(Janre)
    type_choices = (('144', '144p'), ('360', '360p'), ('480', '480p'), ('720', '720p'), ('1080', '1080p'),
                    ('1080 Ultra', '1080p Ultra'),)
    type = models.CharField(max_length=10, choices=type_choices)
    movie_time = models.IntegerField()
    description = models.TextField()
    movie_trailer = models.FileField(verbose_name='video', null=True, blank=True)
    movie_image = models.ImageField(upload_to='movie_images/')
    status_choices = (('Pro', 'Pro'), ('Simple', 'Simple'),)
    status = models.CharField(max_length=10, choices=status_choices)

    def __str__(self):
        return f'{self.movie_name}-{self.country}-{self.janre}'

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=zip(range(1, 11), range(1, 11)))

    def __str__(self):
        return f'{self.user}-{self.stars}'


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.movie}'


class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.nickname} - {self.movie.movie_name}"
