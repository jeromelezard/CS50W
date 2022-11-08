from dataclasses import fields
from pickletools import markobject
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
from random import choice

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))

class EditForm(forms.Form):
        content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner = Markdown()
    md = util.get_entry(entry)
    if md:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(md),
            "title": entry
        })

    else:
        return render(request, "encyclopedia/notFound.html")


def newEntry(request):
    
    form = NewEntryForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/newEntry.html", {
                "form": form,
                "edit": False,
                "existing": True
                
            })
        else:
            return render(request, "encyclopedia/newEntry.html", {
                "form": form,
                "existing": False,
                "edit": False

            })
    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": NewEntryForm(),
            "edit": False
        })

def edit(request, entry):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid(): 
            text = form.cleaned_data["content"]
            util.save_entry(entry, text)
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': entry}))
        else:
            return render(request, "encyclopedia/newEntry.html", {
            "edit": True,
            "form": form,
            "existing": False
        })

    content = util.get_entry(entry)
    if content is None:
        return render(request, "encyclopedia/notFound.html")
    else:
        form = EditForm(initial={'content': content})
        return render(request, "encyclopedia/newEntry.html", {
            "edit": True,
            "form": form,
            "title": entry,
            "existing": False
        })

def random(request):
    entries = util.list_entries()
    randomPage = choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomPage}))

def search(request):
    
    search = request.POST.get("q")
    if util.get_entry(search) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': search}))
    else: 
        entries = []
        for entry in util.list_entries():
            if search.upper() in entry.upper():
                entries.append(entry)
    
       
        return render(request, "encyclopedia/index.html", {
            "searching": True,
            "entries": entries,
            "search": search
        })