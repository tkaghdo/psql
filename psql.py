import json
import os

class Psql:
    def __init__(self, session_id):
        self.session_id = session_id

    def insert(self, table_name, column_names, column_values):
        # PERSON1
        # ["PERSONID", "LASTNAME", "FIRSTNAME", "ADDRESS", "CITY"]
        # [123, "smith", "john", "111 main st", "new york"]


        # in folder PERSON1:
        #    get the number of the last record in each file. they should be all equal.
        #    insert the first value into the first column name
        #    insert second value into second column name
        #

        max_record_count = 0
        for i in column_names:
            self.get_last_record_sequence(table_name, i)
        pass

    # TODO you are here
    def get_last_record_sequence(self, table_name, column_name):
        try:
            with open(table_name + "/" + column_name + ".json") as json_data:
                d = json.load(json_data)

            print(len(d))
            if len(d) == 0:

            #for key, value in d.items():


        except FileNotFoundError:
            print("ERROR: TABLE " + table_name + " DOES NOT EXIST")


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
