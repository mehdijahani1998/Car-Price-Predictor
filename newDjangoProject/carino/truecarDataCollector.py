
import requests as rqs

from bs4 import BeautifulSoup as bsp
from .models import Car

class DataCollector:
    def getSoupsResultsFromTrueCar(self, carManufacturerName, numberOfPages):
        soups = []
        rawURL = "https://www.truecar.com/used-cars-for-sale/listings/{}/"
        for i in range(numberOfPages):
            pageNum = i+1
            reqURL = rawURL.format(carManufacturerName) if pageNum == 1 else rawURL.format(carManufacturerName) + '?page={}'.format(pageNum)
            request = rqs.get(reqURL)
            soup = bsp(request.text, 'html.parser')
            print("read page number {} and retreived its soup".format(pageNum))
            soups.append(soup)
        return soups

    def insertFromSoupToDB (self, carManufacturer, numberOfPages):
        soups = self.getSoupsResultsFromTrueCar(carManufacturer, numberOfPages)
        for soup in soups:
            cards = soup.find_all('div', attrs={'class':'card-content vehicle-card-body order-3 vehicle-card-carousel-body', 'data-test':'cardContent'})

            index = 1
            for card in cards:
                carPrice = card.find('div', attrs={'data-test': 'vehicleCardPricingBlockPrice', 'class': 'heading-3 margin-y-1 font-weight-bold'})
                producedYear = card.find('span', attrs={'class': 'vehicle-card-year font-size-1'})
                carModel = card.find('span', attrs={'class': 'vehicle-header-make-model text-truncate'})
                carCategory = card.find('div', attrs={'data-test':'vehicleCardTrim', 'class':'font-size-1 text-truncate'})
                relatedLink = card.find('a', attrs={'class':'linkable order-2 vehicle-card-overlay', 'data-test':'vehicleCardLink'})
                carMileage = card.find('div', attrs={'data-test': 'vehicleMileage', 'class': 'font-size-1 text-truncate'})
                print(carManufacturer,' - '
                    ,carModel.text.replace(carManufacturer.capitalize()+' ', ''),' - ',carCategory.text
                    , ' - ',carPrice.text.replace('$','').replace(',','')
                    , ' - ',producedYear.text, ' - ', carMileage.text.replace(',','').replace(' miles', '')
                    , ' - ', relatedLink['href'])

                tempCarModel = Car(manufacturer = carManufacturer, car_model = carModel.text.replace(carManufacturer.capitalize()+' ', '')
                                , category = carCategory.text, price = int(carPrice.text.replace('$','').replace(',',''))
                                , production_year = int(producedYear.text), mileage = int(carMileage.text.replace(',','').replace(' miles', '')))
                tempCarModel.save()

                print("added {} record(s) to database".format(index))
                index += 1

