from django.db import models
from django.conf import settings
import uuid

class Questionnaire(models.Model):
    title = models.CharField(max_length=255, verbose_name="Questionnaire Title")
    description = models.TextField(verbose_name="Questionnaire Description")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name_plural = "Questionnaires"

    def __str__(self):
        return self.title

class Section(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255, verbose_name="Section Title")
    description = models.TextField(verbose_name="Section Description")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name_plural = "Sections"

    def __str__(self):
        return self.title

class Question(models.Model):
    TEXT_BOX = 1
    SINGLE_CHOICE = 2
    MULTIPLE_CHOICE = 3
    LOCATION = 3
    QUESTION_TYPE_CHOICES = [
        (TEXT_BOX, 'Text Box'),
        (SINGLE_CHOICE, 'Single Choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (LOCATION, 'Absolute Location'),
    ]

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=255, verbose_name="Question Text")
    question_type = models.IntegerField(choices=QUESTION_TYPE_CHOICES, verbose_name="Question Type")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.question

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255, verbose_name="Option Text")
    class Meta:
        verbose_name_plural = "Options"

    def __str__(self):
        return self.text

        
class Survey(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    response = models.TextField(verbose_name="Response Answer")

    class Meta:
        verbose_name_plural = "Responses"

    def __str__(self):
        return f"Response to {self.question.question}"

