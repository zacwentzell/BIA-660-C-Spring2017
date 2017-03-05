import csv
import datetime
import numpy as np

from collections import OrderedDict, defaultdict
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



    def __init__(self, list_of_lists, header=True, column_names=[]):
        if header and not column_names:
            self.header = list_of_lists[0]
            # Task #1
            # if the number of items in the set of the header (which on contains unique items) < number of items in the header, there are duplicates
            if len(set(self.header)) < len(self.header):
                raise Exception('Duplicate column names detected in header!')
            # a more thorough check would strip whitespace and make all characters lowercase for each of the column names (.strip() followed by .lower())

            self.data = list_of_lists[1:]
        else:
            if column_names:
                self.header = column_names
            else:
                self.header = ['column' + str(index + 1) for index, column in enumerate(list_of_lists[0])]

            self.data = list_of_lists

        # Task #2
        self.data = [[value.strip() if isinstance(value, (str,unicode)) else value for value in row] for row in self.data]
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
            return Series([row[item] for row in self.data])

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

        # only for lists of column names and bools
        elif isinstance(item, list):
            # Assignment #3, Task #2
            if all([isinstance(value, bool) for value in item]):
                return [row for index, row in enumerate(self.data) if item[index]]
            else:
                return [[row[column_name] for column_name in item] for row in self.data]

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]

    # =============Assignment #3 Additions================
    # Helper Functions
    @staticmethod
    def converter_func(data):
        try:
            data_type, values = DataFrame.check_type_and_change(data)
        except:
            return lambda x: x
        if data_type == float:
            return lambda x: float(x.replace(',', ''))
        elif data_type in [datetime.datetime, datetime.date]:
            return lambda x: parse(x)
        else:
            raise NotImplementedError

    # Task #1
    def sort_by_task1(self, column_name, reverse):
        converter_func = self.converter_func(self[column_name])
        self.data = sorted(self.data, key=lambda row: converter_func(row[column_name]), reverse=reverse)

    # Task #1, Extra Credit
    def sort_by(self, column_names, reverses):
        if isinstance(column_names, (str, unicode)) and isinstance(reverses, bool):
            self.sort_by_task1(column_name=column_names, reverse=reverses)
        elif isinstance(column_names, list) and isinstance(reverses, list):
            col_names_rev = reversed(column_names)
            reverses_rev = list(reversed(reverses))
            for index, column_name in enumerate(col_names_rev):
                self.sort_by_task1(column_name=column_name, reverse=reverses_rev[index])
        else:
            raise Exception('Incorrect arguments were passed')

    # Task #3
    def group_by_task3(self, group_by_column, agg_over_column, agg_func):
        converter_func = self.converter_func(self[agg_over_column])
        grouped = defaultdict(list)
        for row in self.data:
            grouped[row[group_by_column]].append(converter_func(row[agg_over_column]))

        return DataFrame([[key, agg_func(value)] for key, value in grouped.iteritems()],
                         column_names=[group_by_column, agg_func.__name__])

    # Task #3, Extra Credit
    def group_by(self, group_by_columns, agg_over_column, agg_func):
        if isinstance(group_by_columns, (str, unicode)):
            return self.group_by_task3(group_by_columns, agg_over_column, agg_func)
        else:
            converter_func = self.converter_func(self[agg_over_column])
            grouped = defaultdict(list)
            for row in self.data:
                # must use tuple because list type is not hashable b/c it's not immutable
                group_by_group = tuple((row[column_name] for column_name in group_by_columns))
                grouped[group_by_group].append(converter_func(row[agg_over_column]))

            column_names = group_by_columns + [agg_func.__name__]
            data = [list(key) + [agg_func(value)] for key, value in grouped.iteritems()]
            df = DataFrame(data, column_names=column_names)

            # why not make it pretty with a sort?
            df.sort_by(group_by_columns, [False for c in group_by_columns])
            return df


class Series(list):
    def __init__(self, list_of_values):
        # Run the __init__ method for list so it behaves like a list
        super(Series, self).__init__(list_of_values)
        # Add some of our own attributes to this object
        try:
            self.type, self.converted_values = DataFrame.check_type_and_change(list_of_values)
        except:
            self.type = object
            self.converted_values = list_of_values

    def __eq__(self, other):
        ret_list = []

        for item in self:
            ret_list.append(item == other)

        return ret_list

    # Assignment #3, Task #2
    def __le__(self, other):
        return [item <= other for item in self.converted_values]

    def __lt__(self, other):
        return [item < other for item in self.converted_values]

    def __ge__(self, other):
        return [item >= other for item in self.converted_values]

    def __gt__(self, other):
        return [item > other for item in self.converted_values]


# Here's some test code
df = DataFrame.from_csv('SalesJan2009.csv')

# Task #1
df.sort_by('Price', False)
assert list(df['Price']) == sorted(list(df['Price']), key=lambda x: float(x.replace(',', '')))
df.sort_by('Transaction_date', True)
assert list(df['Transaction_date']) == sorted(list(df['Transaction_date']), key=lambda x: parse(x), reverse=True)
# Task #1, Extra Credit
df.sort_by(['Payment_Type', 'Price'], [True, False])
assert list(df['Payment_Type']) == sorted(list(df['Payment_Type']), reverse=True)
unique_payment_types = set(df['Payment_Type'])
for pt in unique_payment_types:
    data = [row['Price'] for row in df[df['Payment_Type'] == pt]]
    assert data == sorted(data, key=lambda x: float(x.replace(',', '')))
try:
    df.sort_by(['Payment_Type', 'Price', 'Name', 'Product'], [False, False, False, False])
except:
    print "sort_by doesn't work for more than 2 columns"

# Task #2
test_bool_indexing = df['Price'] < 1100
assert all([isinstance(x, bool) for x in test_bool_indexing])
test = df[test_bool_indexing]
assert all([float(x['Price'].replace(',', '')) < 1100 for x in test])

# Task #3
test = df.group_by('Payment_Type', 'Price', np.mean)
test.sort_by('Payment_Type', False)
assert list(test[test.header[-1]]) == [1717.2727272727273, 1503.370786516854, 1655.0541516245487, 1627.1072796934866]
# Task #3, Extra Credit
test_ec = df.group_by(['Country', 'Payment_Type'], 'Price', np.mean)
test_ec.sort_by(['Country', 'Payment_Type'], [False, False])
assert list(test_ec[test_ec.header[-1]]) == [1200.0, 1200.0, 2400.0, 1800.0, 1636.3636363636363, 1800.0, 1200.0, 1200.0, 1200.0, 1200.0, 1680.0, 1200.0, 1200.0, 3300.0, 1200.0, 1200.0, 2160.0, 1440.0, 1866.6666666666667, 1534.8837209302326, 1200.0, 1200.0, 1200.0, 2000.0, 1200.0, 1200.0, 1200.0, 1200.0, 2000.0, 1200.0, 2400.0, 2043.75, 2400.0, 1200.0, 1636.3636363636363, 1733.3333333333333, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1500.0, 1900.0, 1275.0, 1200.0, 3600.0, 4350.0, 2000.0, 1542.8571428571429, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 2400.0, 3600.0, 1200.0, 1200.0, 1200.0, 1200.0, 2164.2857142857142, 2400.0, 1200.0, 1200.0, 1200.0, 1418.1818181818182, 1200.0, 1200.0, 1200.0, 1200.0, 3600.0, 1200.0, 4350.0, 1200.0, 2000.0, 1200.0, 1200.0, 2000.0, 1200.0, 2000.0, 2000.0, 1200.0, 2123.0769230769229, 2210.5263157894738, 3600.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 2160.0, 1200.0, 1371.4285714285713, 1400.0, 1494.7368421052631, 1690.2777777777778, 1341.1764705882354, 1559.9236641221373, 1674.1150442477876]
try:
    df.group_by(['Payment_Type', 'Country', 'Name', 'Product'], 'Price', np.mean)
except:
    print "group_by doesn't work for more than 2 columns"
