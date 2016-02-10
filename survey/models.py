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
        return self.choice_value


class Submit(models.Model):
    anglo_b = models.ForeignKey(Choice, related_name="anglo_b", blank=True, null=True)
    anglo_uf = models.ForeignKey(Choice, related_name="anglo_uf", blank=True, null=True)
    nordic_b = models.ForeignKey(Choice, related_name="nordic_b", blank=True, null=True)
    nordic_uf = models.ForeignKey(Choice, related_name="nordic_uf", blank=True, null=True)
    german_b = models.ForeignKey(Choice, related_name="german_b", blank=True, null=True)
    german_uf = models.ForeignKey(Choice, related_name="german_uf", blank=True, null=True)
    latin_b = models.ForeignKey(Choice, related_name="latin_b", blank=True, null=True)
    latin_uf = models.ForeignKey(Choice, related_name="latin_uf", blank=True, null=True)
    asian_b = models.ForeignKey(Choice, related_name="asian_b", blank=True, null=True)
    asian_uf = models.ForeignKey(Choice, related_name="asian_uf", blank=True, null=True)
    japanese_b = models.ForeignKey(Choice, related_name="japanese_b", blank=True, null=True)
    japanese_uf = models.ForeignKey(Choice, related_name="japanese_uf", blank=True, null=True)
    gender = models.ForeignKey(Choice, related_name="gender", blank=True, null=True)
    age = models.ForeignKey(Choice, related_name="age", blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return "Country: " + str(self.country) + ", age: " + str(self.age)  