import numpy as np
import re
import csv

if __name__ == '__main__':
    # creates all the lists for the CSV file values
    long = []
    lat = []
    age = []
    rooms = []
    population = []
    household = []
    income = []
    value = []
    ocean = []
    # open the CSV and appending the correct values in the corresponding lists
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
            ocean.append(d["ocean_proximity"])
    # create the lists for the double valued colum
    totalRooms = []
    totalBedrooms = []
    # splits the doubled value and putting each side to the corresponding list, and puts -1 if the value is missing
    for i in rooms:
        i = re.split(",", i)
        left = re.findall('\d+', i[0])
        right = re.findall('\d+', i[1])
        if len(left) > 0:
            totalRooms.append(eval(left[0]))
        else:
            totalRooms.append(0)
        if len(right) > 0:
            totalBedrooms.append(eval(right[0]))
        else:
            totalBedrooms.append(-1)
    # transpose all the lists to np arrays
    long = np.array(long, dtype='f')
    lat = np.array(lat, dtype='f')
    age = np.array(age, dtype='i')
    totalRooms = np.array(totalRooms, dtype='i')
    totalBedrooms = np.array(totalBedrooms, dtype='i')
    population = np.array(population, dtype='i')
    household = np.array(household, dtype='i')
    income = np.array(income, dtype='f')
    value = np.array(value, dtype='i')
    ocean = np.array(ocean)
    # gets all the value type in ocean to a new np array
    oc_value = np.unique(ocean)
    # changing the value type to a numerical value (to the index of the type in the oc_value array)
    for i in oc_value:
        ocean[ocean == i] = np.where(oc_value == i)[0]
    # gets all the indexes where there were no values
    a = np.where(totalBedrooms == -1)
    b = np.where(totalRooms == -1)
    # put in the missing places the mean without those places
    totalBedrooms[a] = (totalBedrooms.sum() + len(a)) / (len(totalBedrooms) - len(a))
    totalRooms[b] = (totalRooms.sum() + len(b)) / (len(totalRooms) - len(b))

