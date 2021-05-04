# Django & Python
from django.shortcuts import render, redirect
from django.http import request
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

# Arango 
from arango import ArangoClient
from arango_orm import Database

# My Functions
from DjangoArango.UserModel import User, valid_username

# connect
client = ArangoClient(hosts='http://localhost:8529')
sys_db = client.db("_system", username="root", password="Abcd@123")
test_db = client.db('test', username='root', password='Abcd@123')
db = Database(test_db)

# Create your views here.


def interface(request):
    users = db.query(User).sort("_key DESC").all()

    context = {
        'users': users,
        'num_users': db.query(User).count(),
    }
    return render(request, 'home/interface.html', context)


def addCollection(request):
    if not sys_db.has_database('test'):
        sys_db.create_database('test')
    # connect db
    if not db.has_collection(User):
        db.create_collection(User)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        is_superuser = request.POST.get('superuser')
        if is_superuser == None:
            is_superuser = False
        else:
            is_superuser = True

        # hash password
        password_hash = make_password(password)
        if valid_username(username):
            new_user = User(username=username, password=password_hash, email=email , is_superuser=is_superuser, dob=datetime.now())
            db.add(new_user)
        else:
            # do somethings
            return redirect('home:interface')

        return redirect('home:interface')

    context = {
        
    }

    return render(request, 'home/addColl.html', context)

def editCollection(request, key):
    getUser = db.query(User).by_key(key)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        is_superuser = request.POST.get('superuser')

        if is_superuser == None:
            is_superuser = False
        else:
            is_superuser = True

        getUser.username=username
        getUser.password=password
        getUser.email=email 
        getUser.is_superuser=is_superuser

        db.update(getUser)

        return redirect('home:interface')

    context = {
        'user': getUser
    }
    return render(request, 'home/editColl.html', context)

def delCollection(request, key):
    # u = db.query(User).by_key(key)
    u = db.query(User).filter("_key==@_key", _key=key)
    u.delete()

    return redirect('home:interface')


def Mylogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        



        print(username, password)


    context = {
       
    }
    return render(request, 'home/login.html', context)

