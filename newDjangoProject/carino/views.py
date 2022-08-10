

from multiprocessing import context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View

from .truecarDataCollector import DataCollector
from .pricePredictor import PricePredictor
from .models import Car ,Question, Choice

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
        querySetresult = Car.objects.values_list('manufacturer').distinct()
        return querySetresult

def selectCar(request, car_manufacturer):
    try:
        carModel = request.POST['model_choice']
        carCtg = request.POST['cat_choice']
        carProYear = int(request.POST['year_field'])
        carMileage = int(request.POST['mileage_field'])

    except (KeyError):
        availableModels = Car.objects.filter(manufacturer = car_manufacturer).values_list('car_model').distinct()
        availableCategories = Car.objects.filter(manufacturer = car_manufacturer).values_list('category').distinct()
    
        context = {
            'carModels' : availableModels,
            'carCategories' : availableCategories,
            'carManufacturer' : car_manufacturer,
            'error_message': "hichi entekhab nakardi ke...",
        }
        return render(request, 'carino/carDetail.html', context)
    
    else:
        
        pp = PricePredictor(car_manufacturer)
        pp.getPreparedPricePredictor()
        predictedPrice = pp.estimatePrice(carModel, carCtg, carProYear, carMileage)

        context = {
            'carManufacturer': car_manufacturer,
            'car_model' : carModel,
            'car_category' : carCtg,
            'prod_year' : carProYear,
            'mileage' : carMileage,
            'predicted_price': predictedPrice
        }
        del pp

        return render(request, 'carino/carResults.html', context)

    #return HttpResponseRedirect(reverse('carino:doctorresults', args=(question.id,)))

def carResultsView(request, car_manufacturer):
    try:
        carModel = request.GET['model_choice']
        carCtg = request.GET['cat_choice']
        carProYear = int(request.GET['year_field'])
        carMileage = int(request.GET['mileage_field'])

    except (KeyError):
        return render(request, 'carino/carDetail.html', {
            'error_message': "hichi entekhab nakardi ke...",
        })
    
    context = {
        'carManufacturer' : car_manufacturer,
    }

    return render(request, 'carino/carResults.html', context)

def showCarDetails (request, car_manufacturer):
    availableModels = Car.objects.filter(manufacturer = car_manufacturer).values_list('car_model').distinct()
    availableCategories = Car.objects.filter(manufacturer = car_manufacturer).values_list('category').distinct()
    
    context = {
        'carModels' : availableModels,
        'carCategories' : availableCategories,
        'carManufacturer' : car_manufacturer
    }

    return render(request, 'carino/carDetail.html', context)

class AwesomeView(View) :

    def get(self, request):
        try:
            msg = request.session.get('msg', False)
        except (KeyError):  
            msg = None
        if ( msg ) : del(request.session['msg'])
        return render(request, 'carino/addCarRecord.html', {'msg':msg})

    def post(self, request):
        carManufacturer = request.POST['manf']
        numberOfPages = int(request.POST['number_of_pages'])

        dataCollector = DataCollector()
        dataCollector.insertFromSoupToDB(carManufacturer, numberOfPages)

        del dataCollector
        msg = 'added records successfuly :)'
        request.session['msg'] = msg
        return redirect(request.path)
