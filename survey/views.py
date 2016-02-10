from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_countries import countries

from .models import Choice, Question, Submit

page = 1

class IndexView(generic.ListView):
    template_name = 'survey/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('pub_date')[:]

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'survey/results.html'

'''def detail(request, question_id, num=1):
    question_list = Question.objects.order_by('pub_date')[:]
    paginator = Paginator(question_list, 1) # Show 1 question per page

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    return render(request, 'survey/detail.html', {'questions': questions})'''

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
        selected_choice = [question.choice_set.get(pk=request.POST['choice1']), question.choice_set.get(pk=request.POST['choice2'])]
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
    submit = Submit(q1=choice_set['1'], q2="", q3="")
    submit.save()
    #for key in choice_set:
     #   choice_set[key].votes += 1
      #  choice_set[key].save()
    return HttpResponseRedirect(reverse('survey:results', args={1, }))


"""def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'survey/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('survey:detail', args=(question.id, 2)))"""