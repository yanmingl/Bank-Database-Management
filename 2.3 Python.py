# example of python connecting to MySQL server and databases
#
import mysql.connector
#
from mysql.connector import Error

#
import pandas as pd
from matplotlib import pyplot as plt

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='autobankms',
                                         user='Yanming',
                                         password='Phappiness902',
                                         auth_plugin='mysql_native_password')
    if connection.is_connected():
        # Set up the connection & print message
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Your connected to database: ", record)
        
        # Question1: Find the specific number of accounts that users whose first name is like "Ric"
        sql_select_Query = "select u.firstName, count(*) as num_accounts\
                            from users u, account a\
                            where u.userID = a.accountID\
                            and u.firstName like '%Ric%'\
                            group by u.firstName;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Find specific number of accounts that users whose first name is like 'Ric' :\n")
        print(records)

        # Format the query result
        for row in records:
            print('firstName =', row[0], ',num_of_account=',row[1])

        # Question2: User's balance
        sql_user_balance = "select u.firstName, a.balance \
                            from Users u, account a \
                            where u.userID = a.userID;"
        cursor = connection.cursor()
        cursor.execute(sql_user_balance)
        result = cursor.fetchall()
        print("User's balance:")
        print(result)

        # Reformat the query result using pandas        
        df = pd.DataFrame(result)  # tranform to dataframe format
        pData = df.rename(columns={0: 'firstName', 1: 'balance'}) # change the column names
        pData.balance = pd.to_numeric(pData.balance) # change the data format
        pData = pData.set_index('firstName')  # set the firstName as index for visua.
        pData = pData.sort_values('balance')  # sort the balance value
        print(pData)

        # Draw the histogram for User's balance using matplotlib
        pData['balance'].plot(kind="barh")
        plt.title("User's Balance")
        plt.xlabel('balance')
        plt.ylabel('firstName')
        plt.show()



except Error as e:
    print("Error while connecting to MySQL", e)
# finally:
#     if (connection.is_connected()):
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")

# you should see the following output
# '''Connected to MySQL Server version  8.0.17
# Your connected to database:  ('classicmodels',)
# True
# MySQL connection is closed'''
#

