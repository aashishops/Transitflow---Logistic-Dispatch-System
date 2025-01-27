import cx_Oracle
from datetime import datetime

# Function to establish database connection
def establish_connection():
    # Connection details
    username = "admin"
    password = "adminlol"
    host = "transitflow.cvk40qw4k75e.us-east-1.rds.amazonaws.com"
    port = 1521
    service_name = "ORCL"

    # Construct the connection string
    dsn = cx_Oracle.makedsn(host, port, service_name)

    # Establish a connection
    connection = cx_Oracle.connect(username, password, dsn)
    return connection

# Function to convert timestamp values
def convert_timestamp_values(values):
    converted_values = []
    for value in values:
        if isinstance(value, str) and len(value) >= 19:
            try:
                value = datetime.strptime(value[:19], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass  # If conversion fails, keep the original value
        converted_values.append(value)
    return converted_values

# Function to insert values into a table
def insert_values(table_name, values):
    try:
        connection = establish_connection()
        cursor = connection.cursor()

        # Convert timestamp values in the input
        values = convert_timestamp_values(values)

        # Prepare the insert statement
        insert_statement = f"INSERT INTO {table_name} VALUES ({', '.join([':' + str(i) for i in range(1, len(values) + 1)])})"

        # Execute the insert statement
        cursor.execute(insert_statement, values)

        # Commit the transaction
        connection.commit()

        print("Values inserted successfully into table:", table_name)

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print("Database error -", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Function to delete records from a table
def delete_record(table_name, condition):
    try:
        connection = establish_connection()
        cursor = connection.cursor()

        # Prepare the delete statement
        delete_statement = f"DELETE FROM {table_name} WHERE {condition}"

        # Execute the delete statement
        cursor.execute(delete_statement)

        # Commit the transaction
        connection.commit()

        print("Record(s) deleted successfully from table:", table_name)

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print("Database error -", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Function to read data from a table
def read_table(table_name):
    try:
        connection = establish_connection()
        cursor = connection.cursor()

        # Prepare the select statement
        select_statement = f"SELECT * FROM {table_name}"

        # Execute the select statement
        cursor.execute(select_statement)

        # Fetch all rows
        rows = cursor.fetchall()

        # Print the rows
        for row in rows:
            # Convert timestamp values in the row
            row = convert_timestamp_values(row)
            print(row)

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print("Database error -", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


# Function to convert timestamp values in a dictionary
def convert_timestamp_values_in_dict(values_dict):
    converted_values_dict = {}
    for key, value in values_dict.items():
        if isinstance(value, str) and len(value) >= 19:
            try:
                value = datetime.strptime(value[:19], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass  # If conversion fails, keep the original value
        converted_values_dict[key] = value
    return converted_values_dict

def read_specific_column(table_name, condition_column, condition_value, columns):
    try:
        connection = establish_connection()
        cursor = connection.cursor()

        # Prepare the select statement with specific columns
        select_statement = f"SELECT {', '.join(columns)} FROM {table_name} WHERE {condition_column} = :1"

        # Execute the select statement with the condition value
        cursor.execute(select_statement, (condition_value,))

        # Fetch all rows
        rows = cursor.fetchall()
        
        return rows

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print("Database error -", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Function to update a record in a table
def update_records(table_name, update_values, condition, condition_value):
    try:
        connection = establish_connection()
        cursor = connection.cursor()

        # Construct the update statement
        update_statement = f"UPDATE {table_name} SET "
        update_statement += ", ".join([f"{key} = :{key}" for key in update_values.keys()])
        update_statement += f" WHERE {condition}"

        # Merge update_values with condition_values
        all_values = {**update_values, 'courier_id': condition_value}

        # Execute the update statement
        cursor.execute(update_statement, all_values)

        # Commit the transaction
        connection.commit()

        print("Record updated successfully in table:", table_name)

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print("Database error -", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


# Example usage:
# Insert values into the table with timestamp value
# insert_values("ORIGIN_WAREHOUSE", ['Chennai', 'O', '2024-04-20 12:34:56'])
# insert_values("Transit", ['TR006', 'W', 'Toronto', 'Vancouver','2024-03-28 11:30:00','2024-03-28 12:00:00'])
# insert_values("user1", ['C012', 'Mical', 'Tailor', 4445256669, 'michael.taylor@example.com', 'qwety'])

# # Read the table
# # read_table("ORIGIN_WAREHOUSE")
# print("Table :\n")
# # read_table("user1")

# # update_record("ORIGIN_WAREHOUSE", {'Orig_Arrival_Time': '2024-04-10 12:34:56'}, "Orig_Arrival_Time = :timestamp_value", '2024-04-20 12:34:56')
# # Delete a particular record
# # delete_record("ORIGIN_WAREHOUSE", "Orig_Arrival_Time = :timestamp_value", '2024-04-10 12:34:56')

# # delete_record("user1", "Login_ID = 'C012'")
# print("deleted")
# # Read the Dispatch Hub table after deletion
# # read_table("user1")

# # Update a record in the table with timestamp value
# # Update a record in the user1 table
# # Update a record in the user1 table
# # Example usage:
# read_table("user1")
# print("updating")
# update_values = {'Login_ID': 'A004', 'F_Name': 'David', 'L_Name': 'Wilson', 'Phone_no': 5556667777, 'Email_id': 'david.wilson@example.com', 'Password': 'admin456'}
# update_values = convert_timestamp_values_in_dict(update_values)
# update_record("user1", update_values, "Login_ID = :login_id", 'A003')

# read_table("user1")
# Read the table
# read_table("ORIGIN_WAREHOUSE")