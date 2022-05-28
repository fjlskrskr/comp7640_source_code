#README#
Steps about database:
1.Open your MySQL Command Line Client (Windows Command Prompt run the command: mysql -u {userName} -p) .
2.Select the database you want to use: mysql> use {your data base name}) .
3.To set up database: mysql> source {path of group8_insert_sql} .
4.To drop the database: mysql> source {path of group8_insert_sql} .
5.The naming format of 'groupX_insert_sql.txt' and 'groupX_drop_sql.txt' may raise SQL syntax error, you might consider changing the filename to 'insert_sql.txt' and 'drop_sql.txt' and try to set up/drop the database again.

Steps about running program:
1.Open your command line (Windows Command Prompt/Windows Power Shell/...) .
2.You might have to install PyMySQL module: pip install PyMySQL .
3.Please modify the parameters in Database()._init__() in the 'database.py' file according to your user and database settings.
4.Run program by running the 'main.py' file: python {path of main.py} .

Program Operation Guide:
1.You need to be logged in to your account for other operations. You can log in to an existing account or register a new account.
2.After logging in successfully, you can perform these operations:
•Purchase item: purchase a specific item.
•Search item: search information of items with a name / keyword.
•Show: You can use this command to show items from a specific store / show all store information / show your cart content / show your order content.
•Add: You can use this command to add new products / add new stores / generate new order.
•Delete: You can use this command to delete a specific item / delete a specific store / delete your cart content / delete your order content.

