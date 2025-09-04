from django.db import models
name = models.CharField(max_length=100, unique=True)


class Meta:
verbose_name = "Category"
verbose_name_plural = "Categories"
ordering = ["name"]


def __str__(self):
return self.name




class Priority(BaseModel):
name = models.CharField(max_length=100, unique=True)


class Meta:
verbose_name = "Priority"
verbose_name_plural = "Priorities"
ordering = ["name"]


def __str__(self):
return self.name




class Task(BaseModel):
title = models.CharField(max_length=255)
description = models.TextField(blank=True)
status = models.CharField(
max_length=50,
choices=StatusChoices.choices,
default=StatusChoices.PENDING,
)
deadline = models.DateTimeField(null=True, blank=True)
priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")


class Meta:
ordering = ["-created_at"]


def __str__(self):
return self.title




class SubTask(BaseModel):
parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
title = models.CharField(max_length=255)
status = models.CharField(
max_length=50,
choices=StatusChoices.choices,
default=StatusChoices.PENDING,
)


class Meta:
ordering = ["-created_at"]


def __str__(self):
return f"{self.title} (of {self.parent_task.title})"




class Note(BaseModel):
task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="notes")
content = models.TextField()


class Meta:
ordering = ["-created_at"]


def __str__(self):
return f"Note for {self.task.title} @ {timezone.localtime(self.created_at).strftime('%Y-%m-%d %H:%M')}"