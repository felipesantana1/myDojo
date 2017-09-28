from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

DATE_REGEX = re.compile(r'[a-zA-Z], [0-9], [0-9]')

def index(request):
    return render(request, 'dojo_project/index.html')

def trips(request):
    context = {

        'user': Users.objects.get(id=request.session['id']).username,
        'mydest': Destinations.objects.filter(trip=Trips.objects.filter(user=Users.objects.filter(id=request.session['id']))),
        'myTrips': Trips.objects.filter(user=Users.objects.get(id=request.session['id'])),
        'trips': Trips.objects.all(),
        'where': Destinations.objects.all(),
        'users': Users.objects.all()

    }
    return render(request, 'dojo_project/success.html', context)

def plan(request):
    return render(request, 'dojo_project/plan.html')

def display(request, id):
    context = {

        'dest' : Destinations.objects.get(id=id)

    }
    return render(request, 'dojo_project/destination.html', context)

def create(request):
    errors = Users.objects.regValidator(request.POST)
    if len(errors):
        for reg, error in errors.iteritems():
            messages.error(request, error, extra_tags=reg)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = Users.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashed_pw)
        request.session['id'] = user.id
        request.session['status'] = 'logged in'
    return redirect('/trips')

def login(request):
    errors = Users.objects.logValidator(request.POST)
    if errors:
        for log, error in errors.iteritems():
            messages.error(request, error, extra_tags=log)
        return redirect('/')
    else:
        request.session['id'] = Users.objects.get(username=request.POST['username']).id
        request.session['status'] = 'logged in'
    return redirect('/trips')

def addTrip(request):
    # time = datetime.now()
    if len(request.POST['name']) < 1:
        messages.error(request, 'Destination title must be at least 2 characters')
    if len(request.POST['plan']) < 4:
        messages.error(request, 'Description must be at least 5 characters')
    else:
         trip = Trips.objects.create(plan=request.POST['plan'], start=request.POST['start'], end=request.POST['end'], user=Users.objects.get(id=request.session['id']))
         Destinations.objects.create(name=request.POST['name'], trip=Trips.objects.get(id=trip.id), user=Users.objects.get(id=request.session['id']))
    return redirect('/trips')
    
def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    return redirect('/trips')