from django.shortcuts import render, redirect
from .models import Tarefa, Tag
from django.urls import reverse
from django.utils import timezone
import datetime


def index(request):
    tarefas = Tarefa.objects.all()

    context = {
        'tarefas': tarefas,
    }
    return render(request, 'index.html', context)


def toggle_status(request, tarefa_id):
    tarefa = Tarefa.objects.get(pk=tarefa_id)
    tarefa.toggle_status()

    return redirect(reverse('index'))


def list_tags(request):
    tags = Tag.objects.all()
    context = {
        'tags': tags,
    }
    return render(request, 'tag_list.html', context)


def add_tag(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            Tag.objects.create(nome=nome)
            return redirect('list_tags')
    return render(request, 'tag_form.html', {'titulo': 'Adicionar Tag'})


def update_tag(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    if request.method == 'POST':
        tag.nome = request.POST.get('nome')
        tag.save()
        return redirect('list_tags')
    return render(request, 'tag_form.html', {'titulo': 'Atualizar Tag', 'tag': tag})


def delete_tag(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    if request.method == 'POST':
        tag.delete()
        return redirect('list_tags')
    return redirect('list_tags')


def add_task(request):
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        prazo_str = request.POST.get('prazo')
        tag_ids = request.POST.getlist('tags')

        prazo = None
        if prazo_str:
            try:
                # Tratar a string do datetime-local
                dt_obj = datetime.datetime.strptime(prazo_str, '%Y-%m-%dT%H:%M')
                # Tornar o datetime aware (necessário no Django)
                prazo = timezone.make_aware(dt_obj)
            except ValueError:
                pass  # Mantém prazo como None se o formato estiver errado

        tarefa = Tarefa.objects.create(
            conteudo=conteudo,
            prazo=prazo
        )
        tarefa.tags.set(tag_ids)

        return redirect('index')

    tags = Tag.objects.all()
    context = {
        'tags': tags,
    }
    return render(request, 'task_form.html', {'titulo': 'Adicionar Tarefa', 'context': context})
