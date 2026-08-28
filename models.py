from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES=[("ACTIVE","Active"),("ON_HOLD","On Hold"),("COMPLETED","Completed")]
    name=models.CharField(max_length=150)
    description=models.TextField(blank=True)
    start_date=models.DateField(null=True,blank=True)
    deadline=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="ACTIVE")
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="owned_projects")
    members=models.ManyToManyField(User,related_name="projects",blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Task(models.Model):
    PRIORITY_CHOICES=[("LOW","Low"),("MEDIUM","Medium"),("HIGH","High"),("CRITICAL","Critical")]
    STATUS_CHOICES=[("TODO","To Do"),("PROGRESS","In Progress"),("REVIEW","Review"),("DONE","Completed")]
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="tasks")
    assigned_to=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="assigned_tasks")
    priority=models.CharField(max_length=10,choices=PRIORITY_CHOICES,default="MEDIUM")
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default="TODO")
    start_date=models.DateField(null=True,blank=True)
    due_date=models.DateField(null=True,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="created_tasks")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.title

class Comment(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE,related_name="comments")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["created_at"]
