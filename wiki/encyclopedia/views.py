from django.shortcuts import render, redirect
from django.http import Http404
from markdown2 import Markdown
from random import choice 
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert_md(title):
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def entry(request, title):
    entry_content = convert_md(title)
    if entry_content == None:
        return render(request, "encyclopedia/error.html",{
            "message": "This entry page does not exist..."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entry_content
        })

def random(request):
    entries = util.list_entries()
    if not entries:
        raise Http404("No entries available")
    
    random_title = choice(entries)
    random_content = util.get_entry(random_title)

    return render(request, "encyclopedia/entry.html",{
        "title": random_title,
        "content": markdowner.convert(random_content)
    })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        contents = convert_md(entry_search)

        if contents:
            return render(request, "encyclopedia/entry.html",{
                "title": entry_search,
                "content": contents
            })
        else:
            all_entries = util.list_entries()
            str_entries = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    str_entries.append(entry)
            if str_entries:
                return render(request, "encyclopedia/search.html",{
                    "suggestion": str_entries
                })
            else:
                return render(request, "encyclopedia/index.html",{
                    "error_message": "There were no results matching the query.",
                    "entries": util.list_entries()
                })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html",{
                "message": "the page is already existed."
            })
        else:
            util.save_entry(title, content)
            content = convert_md(title)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "content": content
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        convert_content = convert_md(title)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": convert_content
        })