from django.urls import path

from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('employees/', views.employee_index, name='employee-index'),
     path('employees/<int:employee_id>/', views.employee_detail, name='employee-detail'),
]