from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Tag
from .forms import TaskForm, TagForm


def index(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})


def toggle_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.toggle_status()
    return redirect('index')



def add_task(request):
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('index')

    return render(request, 'task_form.html', {'title': 'Add Task', 'form': form})


def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(request.POST or None, instance=task)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('index')

    return render(request, 'task_form.html', {'title': 'Update Task', 'form': form})


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
    return redirect('index')



def list_tags(request):
    return render(request, 'tag_list.html', {'tags': Tag.objects.all()})


def add_tag(request):
    form = TagForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_tags')
    return render(request, 'tag_form.html', {'title': 'Add Tag', 'form': form})


def update_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    form = TagForm(request.POST or None, instance=tag)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_tags')
    return render(request, 'tag_form.html', {'title': 'Update Tag', 'form': form})


def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        tag.delete()
    return redirect('list_tags')
