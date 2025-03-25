from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Employee, Role
from .forms import TaskForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

def employee_index(request):
    employees = Employee.objects.all()
    return render(request, 'employees/index.html', {'employees': employees})


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    task_form = TaskForm()
    
    available_roles = Role.objects.exclude(id__in=employee.roles.all().values_list('id'))
    
    return render(request, 'employees/detail.html', { 
        'employee': employee,
        'task_form': task_form,
        'available_roles': available_roles
    })


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
    form = TaskForm(request.POST)
    if form.is_valid():
        new_task = form.save(commit=False)
        new_task.employee_id = employee_id
        new_task.save()
        return redirect('employee-detail', employee_id=employee_id)

class RoleCreate(CreateView):
    model = Role
    fields= '__all__'

class RoleList(ListView):
    model = Role

class RoleDetail(DetailView):
    model = Role

class RoleUpdate(UpdateView):
    model = Role
    fields = ['name']
    
class RoleDelete(DeleteView):
    model = Role
    success_url = '/roles/'

def associate_role(request, employee_id, role_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    role = get_object_or_404(Role, pk=role_id)
    employee.roles.add(role)
    return redirect('employee-detail', employee_id=employee.id)

def remove_role(request, employee_id, role_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    role = get_object_or_404(Role, pk=role_id)
    employee.roles.remove(role)
    return redirect('employee-detail', employee_id=employee.id)

