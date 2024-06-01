from django.db import models

# Create your models here.
from django.db import models


class Experience(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=10)

    def __str__(self):
        return self.nom


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=10)

    def __str__(self):
        return self.nom


class Technologie(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=10)

    def __str__(self):
        return self.nom


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    experiences = models.ManyToManyField(Experience)
    technologie = models.OneToOneField(Technologie, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class UserResponse(models.Model):
    id = models.AutoField(primary_key=True)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Question n° {self.question.id} - Response correcte: {self.is_correct}"
