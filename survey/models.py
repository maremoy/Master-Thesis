from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django_countries.fields import CountryField

@python_2_unicode_compatible
class Question(models.Model):
    question_name = models.CharField(max_length=200, default=" ")
    picture = models.ImageField(upload_to = "./images", blank=True)
    question_text = models.CharField(max_length=200, default=" ")
    CHOICE = 1
    COUNTRYCHOICE = 2
    CHOICETYPES=((CHOICE, 1), (COUNTRYCHOICE, 2),)
    question_type = models.IntegerField(choices=CHOICETYPES, default=1)

    def __str__(self):
    	return self.question_name

@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class Submit(models.Model):
    q1 = models.CharField(max_length=200)
    q2 = models.CharField(max_length=200)
    q3 = models.CharField(max_length=200)
    def __str__(self):
        return 'q1: ' + self.q1 + ', q2: ' + self.q2 + ', q3: ' + self.q3