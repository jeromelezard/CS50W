# create listing form
from django import forms
from .models import *

class NewListingForm(forms.Form):
    title = forms.CharField(label="Listing Title", widget=forms.TextInput(attrs={'class' : 'listingInput', 'size' : '80', 'placeholder' : 'Title...', 'autocomplete' : 'off', 'autofocus': 'autofocus'}))
    image_url = forms.CharField(label="Image URL", required=False, widget=forms.TextInput(attrs={'size' : '80', 'placeholder' : 'Ex: https://i.imgur.com/...', 'autocomplete' : 'off'}))
    description = forms.CharField(label="Listing Description", required=False, widget=forms.Textarea(attrs={'class' : 'listingDescription', 'rows' : '4', 'cols': '82', 'autocomplete' : 'off', 'placeholder' : 'Tell us about your listing...'}))
    starting_price = forms.DecimalField(label="Starting Price: £", label_suffix="", max_digits=8, min_value=0.01)
    category = forms.ModelChoiceField(required=False, queryset=Categories.objects.all())

class NewBidForm(forms.Form):
    bid_amount = forms.DecimalField(label="£", label_suffix="", max_digits=8, min_value=0.01)
    

class CloseListing(forms.Form):
    close_listing = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class AddToWatchlist(forms.Form):
    watchlist = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class RemoveFromWatchlist(forms.Form):
    remove = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class MakeComment(forms.Form):
    comment = forms.CharField(label="Make a comment", widget=forms.Textarea(attrs={'class' : 'makeComment', 'autocomplete' : 'off'}))
    is_comment = forms.BooleanField(widget=forms.HiddenInput, initial=True)