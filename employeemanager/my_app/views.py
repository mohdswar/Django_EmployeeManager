from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Employee, Role
from .forms import TaskForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
def home(request):
    
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def employee_index(request):
    employees = Employee.objects.all()
    return render(request, 'employees/index.html', {'employees': employees})

def employee_detail(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    task_form = TaskForm()
    return render(request, 'employees/detail.html', { 
        'employee': employee,
        'task_form': task_form })


class EmployeeCreate(CreateView):
    model = Employee
    fields = '__all__'


class EmployeeUpdate(UpdateView):
    model = Employee
    fields = ['name', 'description', 'age']

class EmployeeDelete(DeleteView):
    model = Employee
    success_url = '/employees/'

def add_task(request, employee_id):
    # Create a ModelForm instance using the data in request.POST
    form = TaskForm(request.POST)
    # Validate the form
    if form.is_valid():
        # Save the form to the database
        new_task = form.save(commit=False)
        new_task.employee_id = employee_id
        new_task.save()
        return redirect('employee-detail', employee_id=employee_id)

class RoleCreate(CreateView):
    model = Role
    fields= '__all__'