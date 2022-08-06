import datetime


from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self) -> str:
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text


class Car(models.Model):
    manufacturer = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.IntegerField()
    production_year = models.IntegerField()
    mileage = models.IntegerField()

    # class Meta:
    #     ordering = ('manufacturer', 'car_model')

    def __str__(self) -> str:
        return self.manufacturer + '-' + self.car_model + '-' + str(self.price) + '-' + str(self.production_year)


