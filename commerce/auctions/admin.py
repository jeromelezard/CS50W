from django.contrib import admin
from .models import User, Listing, Bid, Comments, Watchlist, Categories
# Register your models here.


admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(Watchlist)
admin.site.register(Categories)

