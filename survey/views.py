from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_countries import countries

from .models import Choice, Question, Submit

class IndexView(generic.ListView):
    template_name = 'survey/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('pub_date')[:]

def results(request):
    return render(request, 'survey/results.html')

choice_set = {}

def detail(request, question_id, choice_set=choice_set):
    try:
        question = Question.objects.get(pk=question_id)
    except(Question.DoesNotExist):
        return submit(request)
    percentage = 25*int(question_id) - 25
    return render(request, 'survey/detail.html', {'question': question, 'choice_set':choice_set, 'percentage': percentage, 'countries': list(countries)})

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
        percentage = 25*int(question_id) - 25
        return render(request, 'survey/detail.html', {'question':question, 'error_message': "You didn't select a choice.", "percentage": percentage})
    else:
        choice_set[question_id] = selected_choice
        return HttpResponseRedirect(reverse('survey:detail', kwargs={'question_id': int(question_id) + 1},))

def voteCountryChoice(request, question_id, question):
    try:
        selected_choice = request.POST['dropdown']
    except (KeyError, CountryChoice.DoesNotExist):
        percentage = 25*int(question_id) - 25
        return render(request, 'survey/detail.html', {'question':question, 'error_message': "You didn't select a choice.", 'choice_set':choice_set, 'percentage': percentage, 'countries': list(countries)})
    else:
        choice_set[question_id] = selected_choice
        return HttpResponseRedirect(reverse('survey:detail', kwargs={'question_id': int(question_id) + 1},))

def submit(request):
    try:
        submit = Submit(anglo_b = choice_set['1'], anglo_uf = choice_set['2'],
            nordic_b = choice_set['3'], nordic_uf = choice_set['4'],
            german_b = choice_set['5'], german_uf = choice_set['6'],
            latin_b = choice_set['7'], latin_uf = choice_set['8'],
            asian_b = choice_set['9'], asian_uf = choice_set['10'],
            japanese_b = choice_set['11'], japanese_uf = choice_set['12'],
            gender = choice_set['13'], age = choice_set['14'], country = choice_set['15'],)
    except KeyError:
        return render(request, 'survey/results.html', {'error_message': "hei paa deg"})
    else:
        submit.save()
        choice_set.clear()
        return HttpResponseRedirect(reverse('survey:results'))