import mysql.connector
import random
import time

# configurações
# muda os dados de acordo com quem ira utilzar
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="chicago"
)

# qual tabela utilizar?
#tabela = "chicago_ordenada_indice"
tabela = "chicago"

# qual campo utilizar?
campo = "departamento"
#campo = "cargo"

# conexão
cursor = mydb.cursor()

# obter cargos ou departamentos
cursor.execute(f"SELECT distinct {campo} FROM {tabela}")
lista_c_ou_d = cursor.fetchall()

# sortear (menos concorrência) ou pegar o primeiro (concorrência total)
sortear = False
#sortear = True

if sortear:
    # sortear um cargo ou departamento
    i = random.randint(0, len(lista_c_ou_d)-1)
else:
    # pega sempre o primeiro 
    i = 0

c_ou_d = lista_c_ou_d[i][0]
#print("escolhi: "+c_ou_d, end="", flush=True)

# deixa commit automático (0) ou controla via transação (1)?
# se deixar commit automático (1), os clientes executam simultaneamente podem incorrer em conflito
# se controlar via transação, ocorre o bloqueio pelo BD

# no commit automatico = true eu NÃO uso transação
# no commit automatico = false eu inicio uma transação
commit_automatico = True
#commit_automatico = False
if commit_automatico:
  cursor.execute("set autocommit=1")
else:
  cursor.execute("set autocommit=0")
  cursor.execute("start transaction") # não precisaria deste comando, pois autocommit=0 já inicia uma transação

# obtém os colaboradores do cargo
# consulta parametrizada pois existem dados com aspas simples
sql = f"select * from {tabela} where {campo} = %s"  
cursor.execute(sql, [c_ou_d])

# obtém os resultados
colabs = cursor.fetchall()

# escolhe dois colaboradores
"""
i = random.randint(0, len(colabs)-1)
j = i
while i == j:
  j = random.randint(0, len(colabs)-1)
alguem = colabs[i]
outro = colabs[j]
"""

alguem = colabs[i]
# verifica qual o tipo de salário
if alguem[4] == "Salary":
  campo_update = "salario_anual"
else:
  campo_update = "valor_hora"

# escolher qual departamento sera utilizado
depto = 'POLICE'
#depto = 'TREASURER'

# prepara o sql
sql = f"update {tabela} set {campo_update} = {campo_update} * 1.1 where departamento = '{depto}'"
# dá o aumento para esse(a) colaborador(a) :-)
cursor.execute(sql)

print("departamento: ", depto)
#print("\n")
# espera um tempo, aqui é para caracterizar a chance de conflito >-) se estiver sem controle de concorrência
#time.sleep(2)

"""
# REPETE PARA O OUTRO
# verifica qual o tipo de salário
if outro[4] == "Salary":
  campo_update = "salario_anual"
else:
  campo_update = "valor_hora"
# prepara o sql
sql = f"update {tabela} set {campo_update} = {campo_update} * 0.1 where nome = '{outro[0]}'"
# dá o aumento para esse(a) colaborador(a) :-)
cursor.execute(sql)

if not commit_automatico:
  # efetiva a transação
  cursor.execute("commit")
"""
# mostra o resultado
#print(f" => {alguem[0]} e {outro[0]}  ganharam :-)")

# referências:
# https://dev.mysql.com/doc/refman/8.0/en/select.html (ctrl+f => buscar: "for update")
# https://dev.mysql.com/doc/refman/5.6/en/innodb-autocommit-commit-rollback.html
# https://www.w3resource.com/mysql/aggregate-functions-and-grouping/aggregate-functions-and-grouping-count-with-distinct.php
# https://popsql.com/learn-sql/mysql/how-to-duplicate-a-table-in-mysql
# https://stackoverflow.com/questions/44693751/python-and-mysql-query-with-quotes
# https://stackoverflow.com/questions/22242081/select-for-update-holding-entire-table-in-mysql-rather-than-row-by-row
# https://dev.mysql.com/doc/refman/8.0/en/commit.html
