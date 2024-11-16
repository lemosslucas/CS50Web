from django.shortcuts import render
from . import util
import markdown2
import random

def convert_md_to_html(title):
    contents = util.get_entry(title)
    if contents is None:
        return None
    else :
        return markdown2.markdown(contents)
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    if request.method == 'POST':
        entry_search = request.POST['q']
        content = convert_md_to_html(entry_search)

        if content is not None:
            return render(request, 'encyclopedia/entry.html', {
            'title': entry_search,
            'content': content 
            })
        else :
            recomedation = []
            entries = util.list_entries()

            for entry in entries: 
                if entry_search.lower() in entry.lower():
                    recomedation.append(entry)
            return render(request, "encyclopedia/search.html", { 
                "recomedation": recomedation
            })

def add_new_page(request):
    if request.method == "GET":
        return render(request, 'encyclopedia/add.html')
    else:
        title = request.POST['title']
        content = request.POST['md_content']
        titleValid = util.get_entry(title)
        if titleValid is not None:
            return render(request, 'encyclopedia/error.html', {
                'message': 'This page already exists'
            })
        else :
            util.save_entry(title, content)
            content = convert_md_to_html(title)
            return render(request, 'encyclopedia/entry.html', {
                'title': title,
                'content': content
            })

def entry(request, title):
    content = convert_md_to_html(title)
    if content is None:
        return render(request, 'encyclopedia/error.html', {
            'message': 'Error 404 this not exist'
        })
    else:
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'content': content 
        })
    

def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            'title': title,
            'content': content
        })
    
def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        
        html_content = convert_md_to_html(title)
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'content': html_content
        })


def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    print(random_entry)
    html_content = convert_md_to_html(random_entry)
    return render(request, 'encyclopedia/entry.html', {
        'title': random_entry,
        'content': html_content  
    }) 
