# Car Price Predictor Web Service

This is a simple website that helps you estimate a used car price. Dataset is derived from "truecar" website.

## Pages

### Main Page
```
localhost:8000/carino/cars
```
The main page of the website shows you a list of available manufacturers. If you want to add a manufacturer you can click on "Do you want to add more records?".

### Select Car Details

```
localhost:8000/carino/cars/<str:car_manufacturer>
```
After you selected the manufacturer you enter the car details page. On this page, you can choose the model, category, production year, and mileage of your car. After you click on the "search this model" button, you can see the estimated price of your car.

### Add More Records to the Database

```
localhost:8000/carino/cars/add_record
```
You can directly add more records to the database in this URL. You just need to enter the manufacturer's name and the number of pages that you need to be scraped from truecar website. Note that all letters have to be lowercase in the manufacturer's name.

## Structure
This project is created using Django. Therefore, it follows the same famous structure of views, models, and templates. However, there are two additional scripts used in the project that provide scraping and prediction services.

### Data Collector
Collecting data is done using beautiful soup [`bs4`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). There are two methods for Data collector object. 
- One is `getSoupsResultsFromTrueCar` which gets the manufacturer's name and number of pages then reads data from truecar website and returns a soup object containing the raw result.
- The second method is `insertFromSoupToDB` which also gets the manufacturer's name and number of pages and by using `getSoupsResultsFromTrueCar` retrieves data. It then extracts specific data from the soup object and inserts the result into the database.

### Price Predictor
We use [`scikit-learn`](https://scikit-learn.org/stable/install.html) to predict a car price based on given information. `PricePredictor` object reads data from the database with `fillQuerySet` method. It turns retrieved data into a 2D list using `fillSpecificationLists` method. Cars specifications are stored in `carsList` and their corresponding prices are stored in `priceList`.

Since the scikit-learn classifier works with 2D lists and only gets integer input, we have to turn string values into integers. By using `fillSpecificationsDicts` method we use hashmap structure to turn model and category values into integers.

In the end `trainCLF` method trains a decision tree based on retrieved data from database and finally `estimatePrice` is used to predict a car's price based on its specifications.

## Requirements and Dependencies
Requirements are available in `requirements.txt`. You can directly install them with this command:
```bash
pip install -r requirements.txt
```

---
## Important Note
Part of this project is the implementation of [Django tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/). Please ignore those parts that aren't related to the price prediction part.