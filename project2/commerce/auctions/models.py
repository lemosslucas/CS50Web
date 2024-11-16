from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Bid(models.Model):
    new_bid_offer = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="listing", default=None)
    user_own = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.CharField(max_length=64)
    url_img = models.CharField(max_length=3000)
    watchlist = models.ManyToManyField(User, default=False, blank=True, related_name="watch_listings")
    closed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comment')