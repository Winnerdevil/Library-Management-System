from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'Login/index.html')


def home(request):
    return redirect('/')


def login(request):
    if request.method == 'POST':
        which_user_name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=which_user_name, password=password)
        user1 = auth.authenticate(email=which_user_name, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        elif user1 is not None:
            auth.login(request, user1)
            return redirect('/')
        else:
            messages.info(request, "Invalid credentials!!!")
            return redirect('login')
    else:
        return render(request, 'Login/index.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username taken!!!")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email taken!!!")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name,
                                                last_name=last_name)

                member = Member.objects.get_or_create(owner_id=user.id, address=address, contact=contact)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Password not Matching!!")
            return redirect('register')

    else:
        return render(request, 'Registration/index.html')
        # return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='login')
def profile(request):
    mem_obj = Member.objects.get(owner_id=request.user.id)
    contact = mem_obj.contact
    address = mem_obj.address
    due = mem_obj.due
    id = request.user.id

    bval = BookDetail.objects.filter(owner_id=id)
    books = [i.book_name for i in bval]
    data = {'contact': contact, 'address': address, 'due': due, 'books': books}
    return render(request, 'profile.html', data)


store = {}


class StoreClass:
    id: int
    book: str


def edit(request, pk, mode, submit):
    mem_obj = Member.objects.get(owner_id=request.user.id)
    publisher_obj = Publisher.objects.get(pk=pk)

    if submit == 1:
        for key in store.keys():
            book_obj = BookDetail.objects.create(owner_id=request.user.id)
            book_obj.book_name = store[key]
            book_obj.save()
        store.clear()
        return redirect('index')

    if mode.lower() == 'plus':
        publisher_obj.number_of_book += 1
        del store[publisher_obj.id]
        publisher_obj.save()

    elif publisher_obj.number_of_book != 0 and mode.lower() == 'sub':
        bookName = publisher_obj.book_name
        if not bookName in store.values():
            store[publisher_obj.id] = bookName
            publisher_obj.number_of_book -= 1
            publisher_obj.save()
    return redirect('allbook')


@login_required(login_url='login')
def allbook(request):
    Field = Publisher.objects.all()
    datas = []
    for key in store.keys():
        obj = StoreClass()
        obj.id = key
        obj.book = store[key]
        datas += [obj]
    return render(request, 'book_display.html', locals())


@login_required(login_url='login')
def return_book(request):
    id = request.user.id
    bval = BookDetail.objects.filter(owner_id=id)
    if request.method == 'POST':
        book = request.POST['book']
        check = False
        for val in bval:
            if val.book_name == book:
                check = True
                break
        if check:
            book_obj = BookDetail.objects.filter(book_name=book)
            num = len(book_obj)
            BookDetail.objects.filter(book_name=book).delete()
            pub_obj = Publisher.objects.get(book_name=book)
            pub_obj.number_of_book += num
            pub_obj.save()
        else:
            messages.info(request, "Enter valid book")
        return redirect('return_book')
    else:
        return render(request, 'return.html')


def manage(request):
    return render(request, 'manage.html')


def admin_page(request):
    return render(request, 'admin.html')
