import json
import os

class Load:
    def __init__(self, session_id):
        self.session_id = session_id

    def insert_from_file(self, table_name, column_names, column_values, file_location, delim=',', skip_rows=0):
        if self.does_table_exists(table_name):
            processing_files_names = self.split_input(table_name, column_names)

    def split_input(self, table_name, column_names):

    def insert_record(self, table_name, column_names, column_values):
        if self.does_table_exists(table_name):
            last_row_count = self.get_last_row_count(table_name)
            for i, column_name in enumerate(column_names):
                self.append(table_name, column_name, last_row_count + 1, column_values[i])
            self.update_last_row_count(table_name)

    def append(self, table_name, column_name, record_location, value, sep=","):
        file_name = table_name + "/" + column_name + ".json"
        try:
            with open(file_name, 'rb+') as f:
                f.seek(-1, os.SEEK_END)

                if self.get_last_row_count(table_name) == 0:
                    sep = ""

                data_type = self.get_data_type(table_name, column_name)

                quote = ""
                if "VARCHAR" in data_type:
                    quote = "\""

                f.write(bytes(sep, "utf-8")
                        + b"\""
                        + bytes(str(record_location), "utf-8")
                        + b"\""
                        + b": "
                        + bytes(quote, "utf-8") + bytes(str(value), "utf-8") + bytes(quote, "utf-8")
                        + b"}")

        except Exception as e:
            print(e)


    def get_data_type(self, table_name, column_name):
        try:
            with open(table_name + "/" + "DATA_TYPES.json", "r") as f:
                d = json.load(f)
            return d[column_name]
        except FileNotFoundError as e:
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
            self.create_data_types_meta_data(table_name, column_names, column_data_type)


    def create_data_types_meta_data(self, table_name, column_names, column_data_type):
        d = {}
        for i, v in enumerate(column_names):
            d[v] = column_data_type[i]
        try:
            with open(table_name + "/" + "DATA_TYPES.json", "w") as f:
                json.dump(d, f)
        except FileNotFoundError as e:
            print(e)

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
