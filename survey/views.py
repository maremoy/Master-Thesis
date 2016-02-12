from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_countries import countries
import logging

from .models import Choice, Question, Submit

logger = logging.getLogger(__name__)

def index(request):
    request.session.flush()
    return render(request, 'survey/index.html')

def results(request):
    request.session.flush()
    return render(request, 'survey/results.html')

def cancel(request):
    request.session.flush()
    return render(request, 'survey/index.html')

def detail(request, question_id):
    if not question_id in request.session:
        request.session[question_id]='0'
    try:
        question = Question.objects.get(pk=question_id)
        logger.error("Could not get the questions with id: " + question_id)
    except(Question.DoesNotExist):
        return submit(request)
    percentage = 6.67*int(question_id) - 6.67
    return render(request, 'survey/detail.html', {'question': question, 'choice_set': request.session[question_id], 'percentage': percentage, 'countries': list(countries)})

def vote(request, question_id):
    if 'previous_button' in request.POST:
        return HttpResponseRedirect(reverse('survey:detail', kwargs={'question_id': int(question_id) - 1},))
    else:
        question = get_object_or_404(Question, pk=question_id)
        if question.question_type == 1:
            return voteChoice(request, question_id, question)
        else:
            return voteCountryChoice(request, question_id, question)

def voteChoice(request, question_id, question):
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        percentage = 6.67*int(question_id) - 6.67
        return render(request, 'survey/detail.html', {'question':question, 'error_message': "You didn't select a choice.", "percentage": percentage})
    else:
        request.session[question_id]=selected_choice.choice_value
        return HttpResponseRedirect(reverse('survey:detail', kwargs={'question_id': int(question_id) + 1},))

def voteCountryChoice(request, question_id, question):
    try:
        selected_choice = request.POST['dropdown']
    except (KeyError, CountryChoice.DoesNotExist):
        percentage = 6.67*int(question_id) - 6.67
        return render(request, 'survey/detail.html', {'question':question, 'error_message': "You didn't select a choice.", 'choice_set':request.session[question_id], 'percentage': percentage, 'countries': list(countries)})
    else:
        request.session[question_id]=selected_choice
        return HttpResponseRedirect(reverse('survey:detail', kwargs={'question_id': int(question_id) + 1},))

def submit(request):
    try:
        submit = Submit(anglo_b = request.session['1'], anglo_uf = request.session['2'],
            nordic_b = request.session['3'], nordic_uf = request.session['4'],
            german_b = request.session['5'], german_uf = request.session['6'],
            latin_b = request.session['7'], latin_uf = request.session['8'],
            asian_b = request.session['9'], asian_uf = request.session['10'],
            japanese_b = request.session['11'], japanese_uf = request.session['12'],
            gender = request.session['13'], age = request.session['14'], country = request.session['15'],)
    except KeyError:
        return render(request, 'survey/results.html', {'error_message': "You did not answer all the questions in the survey. If you have any questionsm, pleas send an email:"})
    else:
        submit.save()
        return HttpResponseRedirect(reverse('survey:results'))