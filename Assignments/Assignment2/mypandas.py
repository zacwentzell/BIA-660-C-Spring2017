import csv
import datetime
import numpy as np

from collections import OrderedDict
from dateutil.parser import parse

class DataFrame(object):

    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        with open(file_path, 'rU') as infile:
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)
            data = []

            for row in reader:
                data.append(row)

            return cls(list_of_lists=data)



    def __init__(self, list_of_lists, header=True):
        if header:
            self.header = list_of_lists[0]
            # Task #1
            # if the number of items in the set of the header (which on contains unique items) < number of items in the header, there are duplicates
            if len(set(self.header)) < len(self.header):
                raise Exception('Duplicate column names detected in header!')
            # a more thorough check would strip whitespace and make all characters lowercase for each of the column names (.strip() followed by .lower())

            self.data = list_of_lists[1:]
        else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(list_of_lists[0])]
            self.data = list_of_lists

        # Task #2
        self.data = [[value.strip() for value in row] for row in self.data]
        # Might as well clean the header too
        self.header = [value.strip() for value in self.header]

        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]

    # Task #3
    @staticmethod
    def check_type_and_change(list_of_values):
        try:
            new_data = [float(value.replace(',', '')) for value in list_of_values]
            return float, new_data
        except:
            pass

        try:
            new_data = [parse(value) for value in list_of_values]
            return datetime.datetime, new_data
        except:
            raise Exception('Error: Data is not floats or timestamps')


    def sum(self, column_name):
        datatype, cast_data = self.check_type_and_change(self[column_name])
        if datatype == float:
            return sum(cast_data)

            # OR you could say
            return reduce(lambda x, y: x+y, cast_data)

            # OR
            summed_values = 0
            for value in cast_data:
                summed_values += value
            return summed_values
        else:
            raise Exception("I don't know how to handle timestamps")

    def mean(self, column_name):
        return self.sum(column_name)/len(self[column_name])

    def median(self, column_name):
        datatype, cast_data = self.check_type_and_change(self[column_name])
        if datatype == float:
            sorted_values = sorted(cast_data)
            mid_point_index = int(len(sorted_values)/2)

            # if there are an odd number of values
            if len(sorted_values) % 2 != 0:
                return sorted_values[mid_point_index]
            elif len(sorted_values) == 1:
                return sorted_values[0]
            elif not sorted_values:
                raise Exception('There are no values...')
            else: # if there an even number of values
                return (sorted_values[mid_point_index] + sorted_values[mid_point_index + 1])/2.0
        else:
            raise Exception("I don't know how to handle timestamps")

    def min(self, column_name):
        return min(self.check_type_and_change(self[column_name])[1])

    def max(self, column_name):
        return max(self.check_type_and_change(self[column_name])[1])

    def std(self, column_name):
        datatype, cast_data = self.check_type_and_change(self[column_name])
        if datatype == float:
            mean = self.mean(column_name)
            return (sum([(value - mean)**2 for value in cast_data])/len(cast_data))**0.5
        else:
            raise Exception("I don't know how to handle timestamps")

    # Task #4
    def add_rows(self, list_of_lists):
        if not all([len(row) == len(self.header) for row in list_of_lists]):
            raise Exception('Invalid number of columns in one or more rows.')

        self.data.extend([OrderedDict(zip(self.header, row)) for row in list_of_lists])

    # Task #5
    def add_column(self, list_of_values, column_name):
        if len(list_of_values) != len(self.data):
            raise Exception('Invalid number of rows in column to be added')

        if column_name.strip().lower() in [column_head.lower() for column_head in self.header]:
            raise Exception('Duplicate column name!')

        for index, value in enumerate(list_of_values):
            self.data[index][column_name] = value

    def __getitem__(self, item):
        # this is for rows only
        if isinstance(item, (int, slice)):
            return self.data[item]

        # this is for columns only
        elif isinstance(item, (str, unicode)):
            return [row[item] for row in self.data]

        # this is for rows and columns
        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rowz]
                    elif all([isinstance(thing, (str, unicode)) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], (str, unicode)):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        # only for lists of column names
        elif isinstance(item, list):
            return [[row[column_name] for column_name in item] for row in self.data]

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]


# Here's some test code
df = DataFrame.from_csv('SalesJan2009.csv')

try:
    df_bad = DataFrame.from_csv('SalesJan2009_dupheader.csv')
except:
    print 'Caught the duplicate header exception!'

assert df['City'] == [value.strip() for value in df['City']]
converted_prices = [float(x.replace(',', '')) for x in df['Price']]

assert df.sum('Price') == np.sum(converted_prices)
assert df.mean('Price') == np.mean(converted_prices)
assert df.median('Price') == np.median(converted_prices)
assert df.min('Price') == np.min(converted_prices)
assert df.max('Price') == np.max(converted_prices)
assert int(df.std('Price')) == int(np.std(converted_prices)) # floating point arithmetic strangeness, see for yourself

converted_dates = [parse(x) for x in df['Transaction_date']]
assert df.min('Transaction_date') == np.min(converted_dates)
assert df.max('Transaction_date') == np.max(converted_dates)

some_rows = df[12:15]
# using list() below to get the values out of the itervalues() generator object
new_rows = [list(row.itervalues()) for row in some_rows]

df.add_rows(new_rows)
bad_rows = [row.append('extra column') for row in new_rows]
try:
    df.add_rows(bad_rows)
except:
    print 'Caught the bad rows'

df.add_column(df['Price'], 'Prices again')
bad_column = df['Price'] + ['9.99']
try:
    df.add_column(bad_column, 'Bad Column')
except:
    print 'Caught the bad column'