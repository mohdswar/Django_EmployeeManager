from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    # Send a simple HTML response
        return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class Employee:
    def __init__(self, name, description, age):
        self.name = name
        self.description = description
        self.age = age

employees = [
    Employee('Lolo',  'Kinda rude.', 3),
    Employee('Sachi', 'Looks like a turtle.', 0),
    Employee('Fancy', 'Happy fluff ball.', 4),
    Employee('Bonk', 'Meows loudly.', 6)
]

def employee_index(request):
    # Render the employee index template with the list of employees
    return render(request, 'employees/index.html', {'employees': employees})