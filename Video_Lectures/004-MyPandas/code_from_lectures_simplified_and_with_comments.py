import csv

from collections import OrderedDict

class DataFrame(object):

    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        """
        Opens a file using the csv module.
        https://docs.python.org/2/library/csv.html
        :param file_path: a string representing the path to the file e.g. ~/Documents/textfile.txt
        :param delimiting_character: a string representing the char(s) that separate columns in a row of data
        :param quote_character: a string for the char(s) that surround values in a column, e.g. "value" -> "
        :return: returns a DataFrame object with the data from the csv file at file_path
        """
        # opens a file in read, universal newline mode and store the file object in infile for this with block
        with open(file_path, 'rU') as infile:

            # create a csv.reader object to process the file and store it in the variable reader
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)

            # creates a variable data and assigns it an empty list
            data = []

            # for each row read (past tense) in from the csv by reader
            for row in reader:
                # append a row (a list) to data
                data.append(row)

            # return an instantiated object of the current class (DataFrame if this is my original code)
            # passing data into the list_of_lists argument
            return cls(list_of_lists=data)
        # end of with block, infile is closed automatically



    def __init__(self, list_of_lists, header=True):
        """
        The __init__ method is called anytime you instantiate the class.
        E.g.
        df = DataFrame(list_of_lists=some_list_of_lists)
        :param self: this argument is implicitly passed, i.e. don't worry about it outside of this class definition.
                    It is the object that you've instantiated.
        :param list_of_lists: a list of lists, namely a list of rows, where each row is a list of values for columns
                                in a dataset
        :param header: a list of strings, where each string is a name of a column (in the same order as the columns)
        """

        # if what was passed into header is True or has a value that is equivalent to false, i.e. bool(header) is True
        if header: # then do this

            # set the header attribute of this DataFrame object that is being instantiated to the first row of what
            # was passed into list_of_lists
            self.header = list_of_lists[0]
            # set the data attribute of this DataFrame object to all the rows after the first row
            # (remember things start from 0 in python not 1)
            self.data = list_of_lists[1:]

        # if what was passed into header is False or has a value that is equivalent to false, i.e. bool(header) is False
        else: # then do this
            # set the data attr to list_of_lists (there's no header here)
            self.data = list_of_lists

            # create a variable called generated_header and set it as an empty list
            generated_header = []

            # choose the first row of the data set as a sample row to iterate through the columns, enumerate it so
            # we can keep a count of what index we're at in the row
            for index, column in enumerate(self.data[0]): # for each index and row in this first row of data
                # append a string that is 'column' concatenated with a string of the current index + 1
                generated_header.append('column' + str(index + 1))

            # set our header attr to this generated_header
            self.header = generated_header

        # we're now outside of the if/else

        # create an empty list called ordered_dict_rows
        ordered_dict_rows = []

        # for each row in self.data
        for row in self.data:
            # for each iteration of the above loop create an empty list called ordered_dict_data
            ordered_dict_data = []

            # for each index and value of this row in self.data
            for index, row_value in enumerate(row):
                # append a tuple to ordered_dict_data that contains the value in header that's at the same index as
                # this value in row
                ordered_dict_data.append((self.header[index], row_value))

            # outside of the inner loop (line 79)
            # ordered_dict_data now contains a list of tuples

            # create an OrderedDict using ordered_dict_data and assign it to ordered_dict_row
            # now we've converted this row to an OrderedDict!
            ordered_dict_row = OrderedDict(ordered_dict_data)

            # append ordered_dict_row to ordered_dict_rows
            ordered_dict_rows.append(ordered_dict_row)

        # now ordered_dict_rows has all the data from before but each row is an OrderedDict instead of just a list of
        # values
        # assign these to the data attr of this DataFrame object
        self.data = ordered_dict_rows



    def __getitem__(self, item):
        """
        the __getitem__ magic method is called whenenver you use square brackets on an object, e.g.  obj[item]

        :param item: this is the object that is inside of the brackets, e.g. df[item]
        :return: returns different things based on what item is, see below
        """
        # this is for rows only
        # if item is an integer or a slice object
        if isinstance(item, (int, slice)):
            return self.data[item]

        # this is for columns only
        # if item is a string or unicode object
        elif isinstance(item, (str, unicode)):
            return [row[item] for row in self.data]

        # this is for rows and columns
        # if item is a tuple
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




infile = open('SalesJan2009.csv')
lines = infile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]
things = lines[559].split('"')
data[559] = things[0].split(',')[:-1] + [things[1]] + things[-1].split(',')[1:]


df = DataFrame(list_of_lists=data)
# get the 5th row
fifth = df[4]
sliced = df[4:10]

# get item definition for df [row, column]

# get the third column
tupled = df[:, 2]
tupled_slices = df[0:5, :3]

tupled_bits = df[[1, 4], [1, 4]]


# adding header for data with no header
df = DataFrame(list_of_lists=data[1:], header=False)

# fetch columns by name
named = df['column1']
named_multi = df[['column1', 'column7']]

#fetch rows and (columns by name)
named_rows_and_columns = df[:5, 'column7']
named_rows_and_multi_columns = df[:5, ['column4', 'column7']]


#testing from_csv class method
df = DataFrame.from_csv('SalesJan2009.csv')
rows = df.get_rows_where_column_has_value('Payment_Type', 'Visa')
indices = df.get_rows_where_column_has_value('Payment_Type', 'Visa', index_only=True)

rows_way2 = df[indices, ['Product', 'Country']]

2+2