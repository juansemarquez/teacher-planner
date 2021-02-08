from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import School

from .forms import NewSchoolForm

def index(request):
    if request.user.is_authenticated:
        #return HttpResponse('Hello, everyone')
        return render(request, "planner/index.html")
    else:
        return render(request, "planner/login.html")
        #return HttpResponseRedirect(reverse('login'))

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
            return render(request, "planner/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "planner/login.html")
# Create your views here.

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "planner/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "planner/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))            
    else:
        return render(request, "planner/register.html")

@login_required
def logout_view(request):
    logout(request)
    return render(request, "planner/login.html")

### SCHOOLS ###
@login_required
def schools(request):
    if request.method == "POST":
        form = NewSchoolForm(request.POST)
        if form.is_valid():
            school = School()
            school.name = form.cleaned_data["name"]
            if request.POST["level"]:
                school.level = form.cleaned_data["level"]
            school.teacher = request.user
            school.save()
            return schools_index(request, "School successfully created")
        else:
            return schools_create(request)

    elif request.method == "GET":
        return schools_index(request)

@login_required
def schools_index(request, message=None):
    school_list = request.user.schools.order_by('name')
    return render(request, "planner/schools/index.html",
                  {"schools": school_list, "paginated":False})


@login_required
def schools_show(request, school_id):
    school = School.object.filter(school_id).get()
    if not school or school.teacher != request.user:
        return HttpResponse('Permission denied')

    if request.method == "PUT":
        #Validate form and store
        pass
    elif request.method == "GET":
        return render(request, "planner/schools/show.html",{"school": school})

@login_required
def schools_create(request):
    form = NewSchoolForm()
    return render(request, "planner/schools/edit.html", 
                  {"school": None, "form": form})

@login_required
def schools_edit(request,school_id):
    school = School.object.filter(school_id).get()
    if not school or school.teacher != request.user:
        return HttpResponse('Permission denied')
    return render(request, "planner/schools/edit.html", {"school": school})

@login_required
def schools_delete(request, school_id):
    school = School.object.filter(school_id).get()
    if not school or school.teacher != request.user:
        return HttpResponse('Permission denied')
    if request.method == "DELETE":
        school.delete()
        return reverse('schools');
    

