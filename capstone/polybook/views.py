from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
import json 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import fitz
from django.core.files.base import ContentFile

from .models import User, Book, Words


def index(request):
    return render(request, "polybook/index.html")

# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "polybook/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "polybook/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "polybook/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "polybook/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "polybook/register.html")

def search_book(request):
    number_books_in_page = 3
    books = Book.objects.all().order_by("id").reverse() 

    if request.method == 'POST':
        book_name = request.POST.get('book_name')

        books_found = []
        for book in books:
            if book_name.lower() in book.name.lower():
                books_found.append(book)

            paginator = Paginator(books_found, number_books_in_page)
            number_page = request.GET.get("page")
            books_in_the_page = paginator.get_page(number_page)

        response = requests.get(f'https://www.google.com/search?q={book_name} pdf')
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links_download = [] 
            dominios = []
            
            for div in soup.find_all('div'):
                title = div.find('h3')
                if title and 'pdf' in title.text.lower():
                    link_tag = div.find('a')
                    if link_tag:
                        raw_link = link_tag['href']

                        if raw_link.startswith('/url?q='):
                            clean_link = raw_link.split('/url?q=')[1]
                            clean_link = clean_link.split('&')[0]

                            parsed_link = urlparse(clean_link)
                            dominio = parsed_link.netloc
                            
                            if dominio not in dominios:
                                links_download.append(clean_link)
                                dominios.append(dominio)

            #remove the search url
            links_download.pop(0)
            
            return render(request, 'polybook/search.html', {
                'links': links_download,
                'name': book_name,
                'books_in_the_page': books_in_the_page
            })
        
    paginator = Paginator(books, number_books_in_page)
    number_page = request.GET.get("page")
    books_in_the_page = paginator.get_page(number_page)
    

    return render(request, "polybook/search.html", {
        "books": books, 
        "books_in_the_page": books_in_the_page,
    })

def upload_book(request):
    if request.method == 'POST':
        name = request.POST.get('book_name')
        gender = request.POST.get('gender')
        user = request.user
        language = request.POST.get('language')
        pdf_file = request.FILES.get('pdf_file')

        new_book = Book(
            name = name, 
            gender = gender,
            user = user,
            language = language,
            pdf_file = pdf_file
        )

        new_book.save()

        #save the cover of book
        pdf_path = new_book.pdf_file.path
        with fitz.open(pdf_path) as pdf:
            page = pdf.load_page(0)
            pixels = page.get_pixmap() 
            img_content = ContentFile(pixels.tobytes("jpeg"), f"{new_book.id}_cover.jpg")

            new_book.cover_image.save(f"{new_book.id}_cover.jpg", img_content)
            new_book.save()

        return HttpResponseRedirect(reverse("index"))

def read_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    pdf_file = book.pdf_file
    words_save = Words.objects.filter(user=request.user.id)

    #print(words_save)
    paginator = Paginator(words_save, 20)
    number_page = request.GET.get("page")
    words_save_in_the_page = paginator.get_page(number_page)

    return render(request, "polybook/read.html", {
        "pdf_file": pdf_file, 
        "book": book,
        "words": words_save,
        'words_save_in_the_page':words_save_in_the_page,
    })

def save_word(request):
    if request.method == "POST":
        data = json.loads(request.body)

        new_word = Words(
            user = request.user,
            source_language = data.get("source_language"),
            target_language = data.get("target_language"),
            word_source = data.get("word_source"), 
            word_target = data.get("target_word"),
        )
        new_word.save()

        return JsonResponse({"word_id": new_word.id})

