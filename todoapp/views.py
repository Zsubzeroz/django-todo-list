from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Tag
from django.utils import timezone
import datetime


# --- Task Views ---

def index(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})


def toggle_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.toggle_status()
    return redirect('index')


def add_task(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        deadline_str = request.POST.get('deadline')
        tag_ids = request.POST.getlist('tags')

        deadline = None
        if deadline_str:
            try:
                dt_obj = datetime.datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
                deadline = timezone.make_aware(dt_obj)
            except ValueError:
                pass

        task = Task.objects.create(content=content, deadline=deadline)
        task.tags.set(tag_ids)
        return redirect('index')

    tags = Tag.objects.all()
    # Note: Passamos 'tags' direto, ajuste seu template task_form.html
    # de {% for tag in context.tags %} para {% for tag in tags %}
    return render(request, 'task_form.html', {
        'title': 'Add Task',
        'tags': tags
    })


def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.content = request.POST.get('content')
        deadline_str = request.POST.get('deadline')

        if deadline_str:
            dt_obj = datetime.datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            task.deadline = timezone.make_aware(dt_obj)
        else:
            task.deadline = None

        task.tags.set(request.POST.getlist('tags'))
        task.save()
        return redirect('index')

    tags = Tag.objects.all()
    formatted_deadline = task.deadline.strftime('%Y-%m-%dT%H:%M') if task.deadline else ""

    return render(request, 'task_form.html', {
        'title': 'Update Task',
        'task': task,
        'tags': tags,
        'formatted_deadline': formatted_deadline,
        'task_tags': task.tags.values_list('id', flat=True)
    })


def delete_task(request, task_id):
    # Recomendado: aceitar apenas POST para deletar
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
    return redirect('index')


# --- Tag Views ---

def list_tags(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html', {'tags': tags})


def add_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Tag.objects.create(name=name)
            return redirect('list_tags')
    return render(request, 'tag_form.html', {'title': 'Add Tag'})


def update_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        tag.name = request.POST.get('name')
        tag.save()
        return redirect('list_tags')
    return render(request, 'tag_form.html', {'title': 'Update Tag', 'tag': tag})


def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        tag.delete()
    return redirect('list_tags')
