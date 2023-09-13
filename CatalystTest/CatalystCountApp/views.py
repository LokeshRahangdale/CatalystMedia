

from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
import pandas
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.


def Index(request):
    return render(request, "index.html")


def Register(request):
    context = {}
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['username']
        password = request.POST['password']
        print(first_name, last_name, email, password)
        User.objects.create(
            first_name=first_name, last_name=last_name, username=email, password=password)
        # data = User.objects.all()
        messages.success(request, 'User Added Successfully.',
                         extra_tags='alert')
    return render(request, 'register.html')


def Login(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username__iexact=email, password=password)
        print(user)
        user1 = User.objects.get(username=email)
        print(user1, "user1")
        if user1 is not None:
            login(request, user1)
            return redirect('index')
    return render(request, 'login.html')


def Logout(request):
    user = request.user
    logout(request)
    return redirect('index')


@csrf_exempt
def UploadExcel(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        file = request.FILES.get('file')
        print("file", file)

        imported_data = pandas.read_csv(file)
        data = imported_data.to_dict(orient='records')
        data_to_list = []
        for data1 in data:
            # print(data1)
            value = data_to_list.append(Company(company_id=data1["id"],
                                                company_name=data1['name'],
                                                company_domain=data1['domain'],
                                                year_founded=data1['year founded'],
                                                industry=data1['industry'],
                                                size_range=data1['size range'],
                                                locality=data1['locality'],
                                                country=data1['country'],
                                                linkedin_url=data1['linkedin url'],
                                                current_employee_estimate=data1['current employee estimate'],
                                                total_employee_estimate=data1['total employee estimate'],
                                                ))
            if data_to_list:
                Company.objects.bulk_create(data_to_list)
                length_of_list = len(data_to_list)
                length_of_db = Company.objects.all().count()
                if length_of_list == length_of_db:
                    return JsonResponse({'msg': "Done"})
                else:
                    return JsonResponse({'msg': "Something went to wrong"})
    return render(request, 'upload.html')


def Search(request):
    company = Company.objects.all()
    if request.method == "POST":
        keyword = request.POST['keyword']
        industry = request.POST['industry']
        year_founded = request.POST['year_founded']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        employee_from = request.POST['employee_from']
        employee_to = request.POST['employee_to']
        company = Company.objects.all()
        if keyword:
            keyword_count = company.filter(
                company_name__icontains=keyword).count()
        else:
            keyword_count = 0
        if industry:
            industry_count = company.filter(industry__iexact=industry).count()
        else:
            industry_count = 0
        if year_founded:
            year_founded_count = company.filter(
                year_founded__iexact=year_founded).count()
        else:
            year_founded_count = 0
        if city:
            city_count = company.filter(locality__icontains=city).count()
        else:
            city_count = 0
        if state:
            state_count = company.filter(locality__icontains=state).count()
        else:
            state_count = 0
        if country:
            country_count = company.filter(country__iexact=country).count()
        else:
            country_count = 0
        if employee_from and employee_to:
            employee_count = company.filter(
                year_founded__range=(employee_from, employee_to)).count()
        else:
            employee_count = 0
        total = keyword_count+industry_count+year_founded_count + \
            city_count+state_count+country_count + employee_count
        print(keyword_count, industry_count, year_founded_count,
              city_count, state_count, country_count, employee_count)
        messages.success(request, str(total)+" Records found for the query",
                         extra_tags='alert')

    return render(request, "quirybuilder.html")


def All_user(request):
    context = {}
    context['data'] = User.objects.exclude(username='admin')
    return render(request, "userdata.html", context)
