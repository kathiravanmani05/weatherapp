from django.shortcuts import render ,redirect
from .forms import CityForm
from .models import City
import requests
from django.contrib import messages


def home(request):
    url  = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=fedce7e8e88fa1f26797e9c5d77e03bd&units=metric'
    if request.method =="POST":
        form = CityForm(request.POST)
        if form.is_valid():
            NCity = form.cleaned_data['name']

            print("NCity")
            CCity = City.objects.filter(name = NCity).count()

            if CCity ==0:
                res = requests.get(url.format(NCity)).json()
                print(res)
                if res['cod'] == 200:
                    form.save()
                    messages.success(request, " "+NCity+" Added Sucessfully ..!")
                else:
                    messages.error(request , "City Dose Not Exist")
            
            else:
                messages.error(request , "City Already Exist")
              

    form = CityForm()

    cities = City.objects.all()
    data = []
    for city in cities:
        res = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city,
            'temperature': res['main']['temp'],
            'description': res['weather'][0]['description'],
            'country': res['sys']['country'],
            'icon': res['weather'][0]['icon'],
        }
        data.append(city_weather)
    return render (request , 'weatherapp.html',{'form':form,'datas':data})

def delete_city(request,Cname):
    City.objects.get(name= Cname).delete()
    messages.success(request, " "+Cname+" Removed Sucessfully ..!")
    return redirect('home')
