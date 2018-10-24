import json
import os

class Psql:
    def __init__(self, session_id):
        self.session_id = session_id

    def insert(self, table_name, column_names, column_values):
        # Personsq
        # [123, "smith", "john", "111 main st", "new york"]
        # TODO you are here
        pass


    def create_db_files(self, table_name, column_names):
        try:
            os.mkdir(table_name)
            # create a json file for each column
            for i in column_names:
                with open(table_name + "/" + i + ".json", "w") as f:
                    json.dump({}, f)

        except FileExistsError:
            print("Directory ", table_name, " already exists")




    def create_table(self, table_name, column_names, column_data_type):
        table_name = table_name.upper()
        if self.does_table_exist(table_name) == True:
            print("ERROR: TABLE " + table_name + " ALREADY EXISTS")
        else:
            self.add_table_to_dictionary(table_name)
            self.create_db_files(table_name, column_names)


    def add_table_to_dictionary(self, table_name):
        with open('tables.json') as json_data:
            d = json.load(json_data)
        d["TABLES"].append(table_name)

        with open('tables.json', 'w') as f:
            json.dump(d, f)


    def does_table_exist(self, table_name):
        table_exists = False
        with open('tables.json') as json_data:
            d = json.load(json_data)
        for i in d["TABLES"]:
            if i == table_name:
                table_exists = True
                break
            else:
                table_exists = False

        return table_exists
