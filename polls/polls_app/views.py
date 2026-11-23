from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError  
import logging

# Create your views here.

from .models import Input
logger = logging.getLogger(__name__)

@login_required
def index(request):
    user_id = request.user.id
    user = request.user
    search = request.GET.get('search', '').strip()
    with connection.cursor() as cursor: # remove lines 21-23, remove comment / activate on line 24 for injection fix
                cursor.execute(f"SELECT id, question_text FROM polls_app_input WHERE owner_id='{user_id}' AND question_text LIKE '%{search}%'")
                query = cursor.fetchall()
    #query = Input.objects.filter(owner=user, question_text=search)
    inputs = Input.objects.all() # remove line 25, remove comment / activate line 26 for fix
    #inputs = Input.objects.filter(owner=user)
    return render(request, "polls_app/index.html", {"inputs" : inputs.values(), 'queries' : query}) # remove this, activate line under with lines 21-23 removed and line 24 activated to work
    #return render(request, "polls_app/index.html", {'inputs' : inputs.values(), 'queries' : query.values()}) # activate this when fixing injection flaw

@login_required
def add_input(request):
    if request.method == "POST":
        
        ip = request.POST.get('input', '').strip()
        secret_answer = request.POST.get('secret_answer', '').strip()
        user = request.user
        Input.objects.create(owner=user, question_text=ip, secret_answer_text=secret_answer) # fix remove this line
        # fix is the line below, activate to work
        #Input.objects.create(owner=user, question_text=ip, secret_answer_text=make_password(secret_answer))

    return redirect("/")

@login_required
def delete_input(request):

    if request.method == "POST":
        user = request.user
        Input.objects.filter(owner=user).delete()
    return redirect("/")
        

def add_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username == password:
            #logger.warning("Password and username too similar!") #-> remove comment to activate
            return redirect("/")
        try:
            #validate_password(password=password) #-> remove comment to activate
            User.objects.create_user(username=username, password=password)
            return redirect("/")
            
        except ValidationError:
            logger.warning("Password too weak, create a stronger one.")
            return redirect("/")
        

    return render(request, "polls_app/register.html")

    

