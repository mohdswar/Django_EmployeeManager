from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Employee, Role
from .forms import TaskForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

@login_required
def employee_index(request):
    employees = Employee.objects.filter(user=request.user)
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


class EmployeeCreate(LoginRequiredMixin,CreateView):
    model = Employee
    fields = '__all__'
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class EmployeeUpdate(LoginRequiredMixin,UpdateView):
    model = Employee
    fields = ['name', 'description', 'age']

class EmployeeDelete(LoginRequiredMixin,DeleteView):
    model = Employee
    success_url = '/employees/'

def add_task(request, employee_id):
    form = TaskForm(request.POST)
    if form.is_valid():
        new_task = form.save(commit=False)
        new_task.employee_id = employee_id
        new_task.save()
        return redirect('employee-detail', employee_id=employee_id)

class RoleCreate(LoginRequiredMixin,CreateView):
    model = Role
    fields= '__all__'

class RoleList(LoginRequiredMixin,ListView):
    model = Role

class RoleDetail(LoginRequiredMixin,DetailView):
    model = Role

class RoleUpdate(LoginRequiredMixin,UpdateView):
    model = Role
    fields = ['name']
    
class RoleDelete(LoginRequiredMixin,DeleteView):
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

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('employee-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )