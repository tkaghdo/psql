import json
import os

class Psql:
    def __init__(self, session_id):
        self.session_id = session_id

    def insert(self, table_name, column_names, column_values):
        if self.does_table_exists(table_name):
            last_row_count = self.get_last_row_count(table_name)
            for i, v in enumerate(column_names):
                self.append(table_name, v, last_row_count + 1, column_values[i])
            self.update_last_row_count(table_name)

    def append(self, table_name, fname, record_location, value, sep=","):
        file_name = table_name + "/" + fname + ".json"
        try:
            with open(file_name, 'rb+') as f:
                f.seek(-1, os.SEEK_END)

                if self.get_last_row_count(table_name) == 0:
                    sep = ""
                print(value, type(value).__name__)
                f.write(bytes(sep, "utf-8")
                        + b"\""
                        + bytes(str(record_location), "utf-8")
                        + b"\""
                        + b": "
                        + bytes(str(value), "utf-8") # TODO need to put double quotes in the json files for string values
                        + b"}")

        except Exception as e:
            print(e)



    def does_table_exists(self, table_name):
        found = False
        try:
            with open("tables.json") as json_data:
                d = json.load(json_data)
            tables = d["TABLES"]
            for i in tables:
                if table_name == i:
                    found = True
                    break
        except FileNotFoundError as e:
            print("ERROR: FILE NOT FOUND")
            print(e)

        return found

    def update_last_row_count(self, table_name):
        try:
            with open(table_name + "/" + "META.json") as json_data:
                d = json.load(json_data)
            d["ROW_COUNT"] = d["ROW_COUNT"] + 1

            with open(table_name + "/" + "META.json", "w") as json_data:
                json.dump(d, json_data)

        except FileNotFoundError as e:
            print(e)

    def get_last_row_count(self, table_name):
        try:
            with open(table_name + "/" +  "META.json") as json_data:
                d = json.load(json_data)
            return d["ROW_COUNT"]
        except FileNotFoundError as e:
            print("ERROR: FILE " + table_name + "/" +  "META.json" + " NOT FOUND")
            print(e)

    def create_db_files(self, table_name, column_names):
        try:
            os.mkdir(table_name)
            # create a json file for each column
            for i in column_names:
                with open(table_name + "/" + i + ".json", "w") as f:
                    json.dump({}, f)

            self.create_metadata_file(table_name)

        except FileExistsError:
            print("Directory ", table_name, " already exists")

    def create_metadata_file(self, table_name):
        d = {}
        d["ROW_COUNT"] = 0
        d["TABLE_NAME"] = table_name

        try:
            with open(table_name + "/" + "META.json", "w") as f:
                json.dump(d, f)
        except Exception as e:
            print("ERROR CREATING META DATA FILE")
            print(e)


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
