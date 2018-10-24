import time
import psql as psql

# cmd = "CREATE TABLE Persons (PersonID int, LastName varchar(255), FirstName varchar(255), Address varchar(255), City varchar(255));"

current_milli_time = lambda: int(round(time.time() * 1000))
session_id = current_milli_time()

q1 = psql.Psql(session_id)

table_name="Person1"
column_names=["PERSONID", "LASTNAME", "FIRSTNAME", "ADDRESS", "CITY"]
column_data_type = ["INT", "VARCHAR(255)", "VARCHAR(255)", "VARCHAR(255)", "VARCHAR(255)"]

# q1.create_table(table_name, column_names, column_data_type)

q1.insert(table_name,
          ["PERSONID", "LASTNAME", "FIRSTNAME", "ADDRESS", "CITY"],
          [123, "smith", "john", "111 main st", "new york"])


