from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    # Send a simple HTML response
        return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def employee_index(request):
    employees=Employee,objects.all()
    return render(request, 'employees/index.html', {'employees': employees})

def employee_detail(request, employee_id):
    employee=Employee.objects.get(id=employee_id)
    return render(request, 'employees/detail.html', {'employee': employee})