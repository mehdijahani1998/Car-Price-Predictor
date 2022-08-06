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
]