import sys

# difftool compares the items in input2 against the items in input1. Essentially that means that
# input1 is the master list, and input2 is checked to see if it matches anything in input1. It
# then returns a list of values of input1 with the items from input2 that matched. The returned 
# value is separated into2 lists "duplicates" and "nonduplicates"
######################################################################################################
# input1 - - - - - required - dict(list) - the master input
# input2 - - - - - required - (dict[list]) - the input of values to check for matches
# glue - - - - - - required - list(touples(string, string)) - list of tupes. The first value is the key in input1 to 
#                                                             match against and the second values is the key in input2 
#                                                             to match against for a given iteration
# capture_fields - optional - list(string) - if specified will keep only key:value pairs who's key is in
#                                            the capturefield list. If only 1 capture field is specified it will
#                                            be used for both inputs.
# flatten_dicts  - optional bool - will flatten all input's dictionaries
class difftool:
    def __init__(self, input1, input2, glue, capture_fields=[], capture_fields2=[], flatten_dicts=False):
        self.input1 = input1
        self.input2 = input2
        self.glue = glue

        if flatten_dicts == True:
            self.input1 = self.flatten(self.input1)
            self.input2 = self.flatten(self.input2)
        else:
            self.input1 = self.input1
            self.input2 = self.input2

        if capture_fields == []:
            self.input1 = input1
            self.input2 = input2
        if capture_fields != [] and capture_fields2 == []:
            self.input1 = self.strip(self.input1, capture_fields)
            self.input2 = self.strip(self.input2, capture_fields)
        if capture_fields != [] and capture_fields2 != []:
            self.input1 = self.strip(self.input1, capture_fields)
            self.input2 = self.strip(self.input2, capture_fields2)

    def flatten(self, d):
        def flatten_dict(d):
            def expand(key, value):
                if isinstance(value, dict):
                    return [(key + '.' + k, v) for k, v in flatten_dict(value).items()]
                else:
                    return [(key, value)]
            items = [item for k, v in d.items() for item in expand(k, v)]

            return dict(items)

        if isinstance(d, list):
            tmp_list = []
            for i in d:
                flat_dict = flatten_dict(i)
                tmp_list.append(dict(flat_dict))
            return tmp_list
        else:
            return flatten_dict(d)

    def strip(self, input_list, capture_fields):
        repaired_list = []
        for entry in input_list:
            tmp = {}
            for item in capture_fields:
                if item not in entry.keys():
                    tmp[item] = 'null'
                elif entry[item] == '':
                    tmp[item] = 'null'
                elif item in entry.keys():
                    tmp[item] = entry[item]
                else:
                    sys.exit(1)
            repaired_list.append(tmp)
        return repaired_list

    def compare(self):

        compared = {'duplicates': [], 'nonduplicates': []}
        num_fields = len(self.glue)

        for x in self.input1:
            values = {'input_1_items': [], 'matches_from_input2': []}
            ymatches = 0
            num_fields = len(self.glue)
            for y in self.input2:
                fieldmatches = 0
                for field in self.glue:
                    x_get_field = str(x.get(field[0]))
                    y_get_field = str(y.get(field[1]))
                    if x_get_field == y_get_field:
                        fieldmatches += 1
                if fieldmatches == num_fields:
                    ymatches += 1
                    values['matches_from_input2'].append(y)
            if ymatches > 0:
                values['input_1_items'].append(x)
                compared['duplicates'].append(values)
            else:
                values['input_1_items'].append(x)
                compared['nonduplicates'].append(values)

        return compared
