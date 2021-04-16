from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'homepage.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')

        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )
        request.session['logged_user'] = user.id
        return redirect('/books')

    return redirect('/')

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email'])

        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/books')
        messages.error(request, "Email or password are incorrect.")
            
    return redirect("/")

def mainpage(request):
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
        'all_books' : Book.objects.all()
    }
    return render(request, 'mainpage.html', context)

def addbook(request):
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/books')

        user = User.objects.get(id=request.session['logged_user'])
        book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by = user
        )
        book.users_who_like.add(user)

        request.session['book_id'] = book.id
    
    return redirect('/books')

def bookinfo(request, book_id):
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
        'current_book' : Book.objects.get(id=book_id),
        'user_who_favorited' : Book.objects.get(id=book_id).users_who_like.all()
    }
    return render(request, "bookinfo.html", context)

def editbook(request, book_id):
    if "logged_user" not in request.session:
        return redirect('/')

    current_book = Book.objects.get(id=book_id)
    current_book.desc = request.POST['desc']
    current_book.save()

    return redirect('/books')

def delete(request, book_id):
    if "logged_user" not in request.session:
        return redirect('/')
    
    delete_current_book = Book.objects.get(id=book_id)
    delete_current_book.delete()
    return redirect('/books')

def favebook(request, book_id):
    if "logged_user" not in request.session:
        return redirect('/')

    fave_book = Book.objects.get(id=book_id)
    current_user = User.objects.get(id=request.session['logged_user'])

    fave_book.users_who_like.add(current_user)
    return redirect(f'/books/{book_id}')

def unfavebook(request, book_id):
    if "logged_user" not in request.session:
        return redirect('/')

    fave_book = Book.objects.get(id=book_id)
    current_user = User.objects.get(id=request.session['logged_user'])

    fave_book.users_who_like.remove(current_user)
    return redirect(f'/books/{book_id}')


def logout(request):
    request.session.flush()
    return redirect('/')