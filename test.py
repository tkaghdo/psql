import time
import Load as ld
import DDL as ddl

# cmd = "CREATE TABLE Persons (PersonID int, LastName varchar(255), FirstName varchar(255), Address varchar(255), City varchar(255));"

current_milli_time = lambda: int(round(time.time() * 1000))
session_id = current_milli_time()

table_1 = ddl.DDL(session_id)

table_name="PERSON"
column_names=["PERSONID", "LASTNAME", "FIRSTNAME", "ADDRESS", "CITY"]
column_data_type = ["INT", "VARCHAR(255)", "VARCHAR(255)", "VARCHAR(255)", "VARCHAR(255)"]

#table_1.create_table(table_name, column_names, column_data_type)

data = ld.Load(session_id)

#data.insert_record(table_name,
#          ["PERSONID", "LASTNAME", "FIRSTNAME", "ADDRESS", "CITY"],
#          [456, "smith", "john", "111 main st", "new york"])


data.insert_record(table_name,
          ["PERSONID", "LASTNAME", "FIRSTNAME", "ADDRESS", "CITY"],
          [456, "smith", "john", "111 main st", "new york"],
          "/persons_input.csv")

