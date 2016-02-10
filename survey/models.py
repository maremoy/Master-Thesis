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

    CHOICE_ONE_BEAUTIFUL = 'not beautiful'
    CHOICE_ONE_USER_FRIENDLY = 'not easy'

    CHOICE_SEVEN_BEAUTIFUL = 'very beautiful'
    CHOICE_SEVEN_USER_FRIENDLY = 'very easy'

    CHOICES_ONE=((CHOICE_ONE_BEAUTIFUL, 'not beautiful'), (CHOICE_ONE_USER_FRIENDLY, 'not user friendly'),)
    CHOICES_SEVEN=((CHOICE_SEVEN_BEAUTIFUL, 'very beautiful'), (CHOICE_SEVEN_USER_FRIENDLY, 'very user friendly'),)

    choice_one = models.CharField(max_length=200, choices=CHOICES_ONE, blank=True)
    choice_seven = models.CharField(max_length=200, choices=CHOICES_SEVEN, blank=True)

    CHOICE = 1
    COUNTRYCHOICE = 2
    CHOICETYPES=((CHOICE, 1), (COUNTRYCHOICE, 2),)
    question_type = models.IntegerField(choices=CHOICETYPES, default=1)

    def __str__(self):
    	return self.question_name

@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ManyToManyField(Question)
    choice_value = models.CharField(max_length=10)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_number


class Submit(models.Model):
    question_one = models.ForeignKey(Choice)
    def __str__(self):
        return self.question_one