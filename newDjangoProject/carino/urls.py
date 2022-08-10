from django.urls import path

from . import views

app_name = 'carino'
urlpatterns = [
    # ex: /carino/
    path('', views.IndexView.as_view(), name='gorbeindex'),
     # ex: /carino/5/
    path('<int:pk>/', views.DetailView.as_view(), name='sooskdetail'),
    # ex: /carino/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='doctorresults'),
    # ex: /carino/5/vote/
    path('<int:question_id>/vote/', views.vote, name='shotorvote'),

    path('cars/', views.CarsListView.as_view() , name = 'carsListView'),
    path('cars/<str:car_manufacturer>', views.showCarDetails, name = 'carModelDetail'),
    path('cars/<str:car_manufacturer>/select', views.selectCar, name = 'carModelSelect'),
    path('cars/<str:car_manufacturer>/results', views.carResultsView, name = 'carModelChoices'),

    path('cars/add_record/', views.AwesomeView.as_view(), name = 'addMoreRecords')
]