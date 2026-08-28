from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, ProjectForm, TaskForm, CommentForm
from .models import Project, Task

def register(request):
    if request.user.is_authenticated: return redirect("dashboard")
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(username=form.cleaned_data["username"],email=form.cleaned_data["email"],password=form.cleaned_data["password"])
            login(request,user)
            return redirect("dashboard")
    else: form=RegisterForm()
    return render(request,"registration/register.html",{"form":form})

@login_required
def dashboard(request):
    tasks=Task.objects.filter(Q(created_by=request.user)|Q(assigned_to=request.user)).distinct()
    return render(request,"tasks/dashboard.html",{
        "projects":Project.objects.filter(Q(owner=request.user)|Q(members=request.user)).distinct()[:6],
        "total":tasks.count(),"todo":tasks.filter(status="TODO").count(),
        "progress":tasks.filter(status="PROGRESS").count(),"done":tasks.filter(status="DONE").count(),
        "overdue":tasks.filter(due_date__lt=__import__("datetime").date.today()).exclude(status="DONE").count(),
        "recent_tasks":tasks.order_by("-updated_at")[:8], "today": __import__("datetime").date.today(),
    })

@login_required
def project_list(request):
    projects=Project.objects.filter(Q(owner=request.user)|Q(members=request.user)).distinct()
    return render(request,"tasks/project_list.html",{"projects":projects})

@login_required
def project_create(request):
    form=ProjectForm(request.POST or None)
    if form.is_valid():
        p=form.save(commit=False); p.owner=request.user; p.save(); form.save_m2m(); p.members.add(request.user)
        messages.success(request,"Project created successfully."); return redirect("project_detail",p.pk)
    return render(request,"tasks/form.html",{"form":form,"title":"Create Project"})

@login_required
def project_detail(request,pk):
    p=get_object_or_404(Project,pk=pk)
    tasks=p.tasks.all().order_by("-created_at")
    return render(request,"tasks/project_detail.html",{"project":p,"tasks":tasks})

@login_required
def project_edit(request,pk):
    p=get_object_or_404(Project,pk=pk,owner=request.user)
    form=ProjectForm(request.POST or None,instance=p)
    if form.is_valid(): form.save(); return redirect("project_detail",p.pk)
    return render(request,"tasks/form.html",{"form":form,"title":"Edit Project"})

@login_required
def project_delete(request,pk):
    p=get_object_or_404(Project,pk=pk,owner=request.user)
    if request.method=="POST": p.delete(); return redirect("project_list")
    return render(request,"tasks/confirm.html",{"object":p,"type":"project"})

@login_required
def task_create(request):
    form=TaskForm(request.POST or None)
    form.fields["project"].queryset=Project.objects.filter(Q(owner=request.user)|Q(members=request.user)).distinct()
    form.fields["assigned_to"].queryset=User.objects.all()
    if form.is_valid():
        t=form.save(commit=False); t.created_by=request.user; t.save()
        messages.success(request,"Task created successfully."); return redirect("project_detail",t.project.pk)
    return render(request,"tasks/form.html",{"form":form,"title":"Create Task"})

@login_required
def task_edit(request,pk):
    t=get_object_or_404(Task,pk=pk)
    form=TaskForm(request.POST or None,instance=t)
    if form.is_valid(): form.save(); return redirect("project_detail",t.project.pk)
    return render(request,"tasks/form.html",{"form":form,"title":"Edit Task"})

@login_required
def task_delete(request,pk):
    t=get_object_or_404(Task,pk=pk)
    project=t.project
    if request.method=="POST": t.delete(); return redirect("project_detail",project.pk)
    return render(request,"tasks/confirm.html",{"object":t,"type":"task"})

@login_required
def add_comment(request,pk):
    t=get_object_or_404(Task,pk=pk)
    form=CommentForm(request.POST or None)
    if form.is_valid():
        c=form.save(commit=False); c.task=t; c.user=request.user; c.save()
    return redirect("project_detail",t.project.pk)
