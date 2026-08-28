from django import forms
from django.contrib.auth.models import User
from .models import Project, Task, Comment

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=["username","email","password"]
    def clean(self):
        data=super().clean()
        if data.get("password") != data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return data

class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=["name","description","start_date","deadline","status","members"]
        widgets={"start_date":forms.DateInput(attrs={"type":"date"}),"deadline":forms.DateInput(attrs={"type":"date"})}

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=["title","description","project","assigned_to","priority","status","start_date","due_date"]
        widgets={"start_date":forms.DateInput(attrs={"type":"date"}),"due_date":forms.DateInput(attrs={"type":"date"})}

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["body"]
        widgets={"body":forms.Textarea(attrs={"rows":3,"placeholder":"Write a comment..."})}
