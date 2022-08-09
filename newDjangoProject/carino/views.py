

from multiprocessing import context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Car, CarChoice ,Question, Choice

class IndexView(generic.ListView):
    template_name = 'carino/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'carino/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'carino/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
   
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'carino/detail.html', {
            'question': question,
            'error_message': "hichi entekhab nakardi ke...",
        })
    
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('carino:doctorresults', args=(question.id,)))

### carino main pages come here. everything before that was from django tutorial itself.

class CarsListView(generic.ListView):
    model = Car
    template_name = 'carino/carsList.html'
    
    context_object_name = 'cars_list'
    def get_queryset(self):
        """Return all cars in the database."""
        querySetresult = Car.objects.values_list('manufacturer', 'car_model').distinct()
        return querySetresult

# def selectCar(request, carManufacturer):
#     car = get_object_or_404(Car, pk=carManufacturer)
   
#     try:
#         selected_choice = Car.objects.filter(manufacturer = 'honda').values_list('car_model').distinct()
#         selected_choice = car.choice_set.get(pk=request.POST['choice'])

    
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'carino/carDetail.html', {
#             'car': car,
#             'error_message': "hichi entekhab nakardi ke...",
#         })
    
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('carino:doctorresults', args=(question.id,)))

def carResultsView(request, car_manufacturer):
    availableModels = Car.objects.filter(manufacturer = car_manufacturer).values_list('car_model').distinct()
    availableModelsList = [availableModels[i][0] for i in range(len(availableModels))]
    modelsVotes = {}
    
    for car_model in availableModelsList:
        
        try:
            modelsVotes.update({car_model: CarChoice.objects.get(car_model = car_model).votes})
        
        except(CarChoice.DoesNotExist):
            modelsVotes.update({car_model: 0})
            cc = CarChoice(car_model = car_model, votes = 0)
            cc.save()
    
    context = {
        'carModelsDict' : modelsVotes,
        'carManufacturer' : car_manufacturer
    }

    return render(request, 'carino/carResults.html', context)