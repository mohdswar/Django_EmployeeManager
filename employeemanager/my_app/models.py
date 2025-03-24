from django.db import models
from django.urls import reverse

PRIORITYS = (
    ('A', 'low'),
    ('B', 'normal'),
    ('C', 'urgent'),
)


class Employee(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'employee_id': self.id})

class Task(models.Model):
    task = models.TextField(max_length=250)
    date = models.DateField('Due date')
    priority = models.CharField(
        max_length=1,
        choices=PRIORITYS,
        default=PRIORITYS[0][0],
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.task} on {self.date} with priority {self.get_priority_display()}"
    class Meta:
        ordering = ['-date']