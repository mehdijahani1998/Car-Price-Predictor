
from collections import defaultdict
from sklearn import tree

from .models import Car

class PricePredictor:
    querySet = []
    carsDict = {}
    categoryDict = {}

    # carsList : [model, category, prodYear, mileage]
    carsList = []
    # priceList : [price]
    priceList = []

    def __init__(self, car_manufacturer) -> None:
        self.car_manufacturer = car_manufacturer
        self.clf = tree.DecisionTreeRegressor()

    def fillQuerySet (self):
        self.querySet = Car.objects.filter(manufacturer = self.car_manufacturer, mileage__gte = 0)

    def fillSpecificationLists(self):
        for result in self.querySet:
            self.priceList.append(result.price)
            self.carsList.append([result.car_model, result.category, result.production_year, result.mileage])

    def fillSpecificationsDicts(self):
        for car in self.carsList:
            carModel = car[0]
            carCtg = car[1]

            if not self.car_manufacturer in self.carsDict.keys():
                newIndex = len(self.carsDict.keys()) + 1
                self.carsDict.update({self.car_manufacturer : {'index': newIndex}})

            if not carModel in self.carsDict[self.car_manufacturer].keys():
                newIndex = len(self.carsDict[self.car_manufacturer].keys())
                self.carsDict[self.car_manufacturer].update({carModel : newIndex})
            
            if not carCtg in self.categoryDict:
                newIndex = len(self.categoryDict.keys()) + 1
                self.categoryDict.update({carCtg : newIndex})

            car[0] = self.carsDict[self.car_manufacturer]['index']
            car[1] = self.carsDict[self.car_manufacturer][carModel]
            car[2] = self.categoryDict[carCtg]

    def trainCLF(self):
        self.clf = self.clf.fit(self.carsList, self.priceList)

    def estimatePrice(self, carModel, carCategory, prodYear, mileage):
        
        newCarData = [[self.carsDict[self.car_manufacturer][carModel], self.categoryDict[carCategory], prodYear, mileage]]
        estimatedPrice = self.clf.predict(newCarData)
        return estimatedPrice[0]

