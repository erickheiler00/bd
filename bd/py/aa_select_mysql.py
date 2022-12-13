import mysql.connector

# configurações
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mypass",
  database="employees"
)

# conexão
mycursor = mydb.cursor()

# comando select
mycursor.execute("SELECT * FROM chicago")

# obter os resultados
myresult = mycursor.fetchall()

# percorrer os resultados
for x in myresult:
  print(x)

# referência:
# https://www.w3schools.com/python/python_mysql_select.asp