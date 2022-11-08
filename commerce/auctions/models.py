from django.contrib.auth.models import AbstractUser
from django.db import models
#from django.db.models import Sum
#from django.db.models import Count

class User(AbstractUser):
    pass
class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"
        
class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True, null=True)
    starting_price = models.DecimalField(max_digits=9, decimal_places=2)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey(Categories,on_delete=models.CASCADE, blank=True, null=True)
    url = models.CharField(max_length=128, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=True)
    def __str__(self):
        return f"{self.title}: £{self.starting_price}, created on: {self.date_created}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    bid_amount = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bid amount: £{self.bid_amount}, by {self.user}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")
    comment = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment: '{self.comment}'"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"User {self.user} is watching {self.listing}"


