# Shahar_Ariel_314868977

import json
import csv


class DataSummary:
    data = None
    dataType = dict()

    def __init__(self, datafile="", metafile=""):
        """
        Constractor: initialize the class object
        :param datafile: open the JSON with the Data in it
        :raise ValueError if not both files are entered - both files are a must
        :param metafile: open the CSV with the metaData in it
        """
        # checks if user entered both file names:
        if datafile == "" or metafile == "":
            raise ValueError
        # open and check if the files exist:
        f_meta = open(metafile)
        meta = csv.reader(f_meta)
        f_data = open(datafile)
        # loads the file and convert them into dictionaries:
        self.data = json.load(f_data)
        self.data = self.data["data"]
        self.dataType = dict(zip(next(meta), next(meta)))
        # put all the Datatypes into the data and delete all the dataTypes in the data that are not in the dataTypes:
        for row in self.data:
            # create a list of the keys in the data:
            keys = list(row.keys())
            # create none existing keys in the data from the CSV:
            for feature in self.dataType:
                if feature not in keys:
                    row[feature] = None
            # delete the keys that are in the data but not in the CSV:
            for feature in keys:
                if feature not in self.dataType:
                    row.pop(feature)

    def __getitem__(self, key):
        """
         Getitem:enable the user to use the [] operator in the DataSummary object
         when entering a number the [] will return the value in the index
         when entering a string the [] will check and return all the values of that key
        :param key: the index or category to return
        :raise IndexError if the index is out of the range of the list
        KeyError if the feature is not in the dataType
        :return: the key'th record or a list of all values in the 'key' category
        """
        # check if the key is a number
        is_num = isinstance(key, (int, float))
        if is_num == 1:
            # if it's a number, checks if it's in range.
            if len(self.data) <= key:
                raise IndexError("index is out of range")
            data = self.data[key].copy()
        else:
            # if it's not a number, checks if it's in the dataTypes
            if key not in self.dataType:
                raise KeyError("feature Not in features list")
            data = [row[key] for row in self.data]
        return data

    def __get_value_list(self, feature):
        """
        checks if the feature is in the dataType, and its type and return a list of values
        :param feature: the user choice for the feature to get a list from
        :raise ValueError if feature not in dataType
        TypeError if value is categorical
        :return: a list of values in the feature entered
        """

        # check if the feature is a number
        if feature not in self.dataType:
            raise ValueError("Feature not in data!")
        # check the number type
        if self.dataType[feature] not in ['int', 'float']:
            raise TypeError("Feature value is categorical")
        # cast the correct number type to the values and return a list of them
        if self.dataType[feature] == 'int':
            return [int(val) for val in self[feature] if val is not None]
        else:
            return [float(val) for val in self[feature] if val is not None]

    def sum(self, feature):
        """
        sums all the chosen feature values
        :param feature: a feature to sum all of its values (the values in the feature must be numbers)
        :return: a sum of all the feature values
        """
        # sums the values from the get_values_list of the feature
        return sum(self.__get_value_list(feature))

    def count(self, feature):
        """
        count all the chosen feature values
        :param feature: a feature to count all of its values (the values in the feature must be numbers)
        :return: a count of all the feature values
        """
        # checks if the feature is in the dataType
        if feature not in self.dataType:
            raise ValueError("Feature not in data!")
        # calculate and return the number of values in this feature without 'None'
        return len(self[feature]) - self[feature].count(None)

    def mean(self, feature):
        """
        give the mean of all the chosen feature values
        :param feature: a feature to calculate the mean of all of its values (the values in the feature must be numbers)
        :return: the mean of the features values (sum / amount)
        """
        # calculate and return the mean of the values of the feature
        return self.sum(feature) / self.count(feature)

    def min(self, feature):
        """
        give the minimum value in the chosen feature
        :param feature: a feature to calculate the minimum of all of its values
            (the values in the feature must be numbers)
        :return: the minimum value in the feature
        """
        # return the min of the list from get_value_list of the feature
        return min(self.__get_value_list(feature))

    def max(self, feature):
        """
        give the maximum value in the chosen feature
        :param feature: a feature to calculate the maximum of all of its values
            (the values in the feature must be numbers)
        :return: the maximum value in the feature
        """
        # return the max of the list from get_value_list of the feature
        return max(self.__get_value_list(feature))

    def unique(self, feature):
        """
        gives a list of values that appear once in the chosen feature
        :param feature: a feature to create a unique values list from
        :return: a list with the unique values
        """
        # create a list of the values without the None
        values = [val for val in self[feature] if val is not None]
        # check the value type and if it's a number, casts it to the correct type
        if self.dataType[feature] == 'int':
            values = [int(val) for val in values]
        elif self.dataType[feature] == 'float':
            values = [float(val) for val in values]
        # create a list of all the values that appear once and sorts it
        return sorted([x for x in values if values.count(x) == 1])

    def mode(self, feature):
        """
        gives a list of the values that appear the most in the chosen feature
        (not including None)
        :param feature: a feature to create the list of the most common values from
        :return: a list with the most common values in the feature
        """
        # create a local max value
        common = 0
        # for each value, checks that it's not null and counts it
        for val in self[feature]:
            if val is None:
                continue
            num = self[feature].count(val)
            # checks for the biggest number of appearances of a value
            if num > common:
                common = num
            # create a list of values that appear the same amount as calculated before
            # then transform it to a set to remove duplicates then returns it to a list and return it
        return list(set([val for val in self[feature] if self[feature].count(val) == common]))

    def empty(self, feature):
        """
        give the amount of None in the chosen feature
        :param feature: a feature to count the amount of None in
        :return: an int with the amount of None in the feature
        """
        # count the number of None in the chosen feature
        return self[feature].count(None)

    def to_csv(self, filename, delimiter=","):
        """
        create a new csv file with the name of filename, that include the field names from the dataType
        and the data from data and a chosen delimiter
        :param filename: the name of the new file to create
        :param delimiter: can use (" ", ".", ":", "|", "-", ";", "#", "*", ","), only one defaults to ","
        :return: None
        """
        # checks if the delimiter is in the supported characters
        if delimiter not in (" ", ".", ":", "|", "-", ";", "#", "*", ","):
            delimiter = ","
        # create a list of the field names and holds it
        fieldnames = list(self.dataType.keys())
        # create a list of the data and holds it
        rows = self.data
        # opening a csv file and a writer with the chosen delimiter or the default one and the fieldnames
        with open(filename, "w+", newline='') as new_file:
            writer = csv.DictWriter(new_file, delimiter=delimiter, fieldnames=fieldnames)
            # writes the data into the file
            writer.writeheader()
            writer.writerows(rows)
        return None


# def main():
#     d = DataSummary("Happiness.json", "Happiness_meta.csv")
#     print("sum: ", d.sum("Happiness Rank"))
#     print("mean: ", d.mean("Happiness Rank"))
#     print("[Country]: ", d["Country"])
#     print("[10] :", d[10])
#     print("min: ", d.min("Happiness Rank"))
#     print("unique: ", d.unique("Happiness Rank"))
#     print("unique: ", d.unique("Country"))
#     print("unique: ", d.unique("Region"))
#     print("mode: ", d.mode("Region"))
#     print("mode: ", d.mode("Class"))
#     print("empty: ", d.empty("Country"))
#     # d.to_csv("test2", "|")
#
#
# if __name__ == "__main__":
#     main()
