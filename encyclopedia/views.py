from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
import random

md = Markdown()

class NewSearchForm(forms.Form):
    form = forms.CharField(label="")

class NewPostForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea, max_length=1000)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def wiki(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/wiki.html", {
            "text": md.convert(util.get_entry(title)),
            "title": title,
            "form": NewSearchForm()
        })
    else:
        return render(request, "encyclopedia/wiki.html", {
            "text": "Post not found"
        })

def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data["form"]
            if search_query in util.list_entries():
                return render(request, "encyclopedia/wiki.html", {
                "text": md.convert(util.get_entry(search_query)),
                "form": NewSearchForm()
            })
            #прогнати по кожному елементу search
            else:
                query_list  = []
                for i in range(len(util.list_entries())):
                    if search_query in util.list_entries()[i]:
                        query_list.append(util.list_entries()[i])
                if len(query_list) > 0:
                    return render(request, "encyclopedia/search.html",{
                        "list": query_list,
                        "form": NewSearchForm()
                    })
                else:
                    return render(request, "encyclopedia/search.html",{
                        "text": "Post Not Found",
                        "form": NewSearchForm()
                    })
    else:
        return HttpResponseRedirect(reverse("index"))

def create(request):
    if request.method == "POST":
        post_form = NewPostForm(request.POST)
        if post_form.is_valid():
            title = post_form.cleaned_data["title"]
            text = post_form.cleaned_data["text"]
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'encyclopedia/create.html',{
                "post_form": post_form
            })
    else:
        return render(request, 'encyclopedia/create.html',{
            "post_form": NewPostForm(),
            "form": NewSearchForm()
        })

def random_post(request):
    random_num = random.randint(0,len(util.list_entries())-1)
    return render(request, "encyclopedia/random.html", {
        "text": md.convert(util.get_entry(util.list_entries()[random_num])),
        "form": NewSearchForm()
    })