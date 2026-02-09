from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='tasks')

    def __str__(self):
        return self.content[:30]

    def toggle_status(self):
        self.is_completed = not self.is_completed
        self.save()

    class Meta:
        ordering = ['is_completed', '-created_at']
