from django.db import models
from django.utils import timezone


class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'todoapp'  # ADICIONAR ISSO


class Tarefa(models.Model):
    conteudo = models.TextField()
    data_hora_criacao = models.DateTimeField(default=timezone.now)
    prazo = models.DateTimeField(null=True, blank=True)
    concluida = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='tarefas')

    def __str__(self):
        return self.conteudo[:30] + "..."

    def toggle_status(self):
        self.concluida = not self.concluida
        self.save()

    class Meta:
        ordering = ['concluida', '-data_hora_criacao']
        app_label = 'todoapp'  # ADICIONAR ISSO
