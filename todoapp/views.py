from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def home(request):
    # Render lists of active and completed tasks
    tasks = Task.objects.filter(completed=False).order_by("-created_at")
    completed_tasks = Task.objects.filter(completed=True).order_by("-created_at")
    form = TaskForm()
    return render(request, "index.html", {"tasks": tasks, "completed_tasks": completed_tasks, "form": form})


def addTask(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("home")


def mark_as_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = True
    task.save()
    return redirect("home")


def mark_as_undone(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = False
    task.save()
    return redirect("home")


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("home")


def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TaskForm(instance=task)
    return render(request, "edit_task.html", {"form": form, "task": task})
