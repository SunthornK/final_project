import copy
import csv
import os

class Csv:
    def __init__(self, file_name):
        self.__filename = file_name
        self.__location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.__file = []

    def read_csv(self):
        with open(os.path.join(self.__location, self.__filename)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                self.__file.append(dict(r))
        return self.__file


class Database:
    def __init__(self):
        self.database = []

    def update_tables(self):
        for table in self.database:
            table.update_csv()

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def update_csv(self):
        if not self.table:
            return

        with open(f"{self.table_name}.csv", "w", newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.table[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(self.table)

    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def __is_float(self, element):
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)

    def insert(self, item):
        self.table.append(item)

    def update(self,find_key, find_value, new_key, new_value):
        for i in self.table:
            if i[find_key] == find_value:
                i[new_key] = new_value
        return self.table

    def select(self, attributes_list):
        temps = []
        for item in self.table:
            dict_temp = {}
            for key in item:
                if key in attributes_list:
                    dict_temp[key] = item[key]
            temps.append(dict_temp)
        return temps

    def __str__(self):
        return f"{self.table_name}:{str(self.table)}"

