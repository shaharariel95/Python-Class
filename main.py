import numpy as np
import re
import csv
if __name__ == '__main__':
    long = []
    lat = []
    age = []
    rooms = []
    population = []
    household = []
    income = []
    value = []

    with open("./CA-Housing.csv") as file:
        reader = csv.DictReader(file)
        for d in reader:
            long.append(d["longitude"])
            lat.append(d["latitude"])
            age.append(d["housing_median_age"])
            rooms.append(d["rooms"])
            population.append(d["population"])
            household.append(d["households"])
            income.append(d["median_income"])
            value.append(d["median_house_value"])

    totalRooms = []
    totalBedrooms = []

    for i in rooms:
        print(i)
    # for i in rooms:
    #     dict(i)
    #     print(i)
    for i in rooms:
        totalRooms.append(i["total_rooms"])
        totalBedrooms.append(i["total_bedrooms"])

    for i in totalBedrooms:
        print(i)
