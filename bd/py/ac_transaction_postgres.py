import psycopg2
import random
import time

# configurações
mydb = psycopg2.connect(
  host="localhost",
  user="postgres",
  password="root",
  database="employees"
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
print("escolhi: "+c_ou_d, end="", flush=True)

# deixa commit automático (0) ou controla via transação (1)?
# se deixar commit automático (1), os clientes executam simultaneamente podem incorrer em conflito
# se controlar via transação, ocorre o bloqueio pelo BD

commit_automatico = True
#commit_automatico = False
if commit_automatico:
  pass
else:
  cursor.execute("begin")

# obtém os colaboradores do cargo
# consulta parametrizada pois existem dados com aspas simples
sql = f"select * from {tabela} where {campo} = %s"

# DESEJA FAZER CONTROLE DE CONCORRÊNCIA VIA BLOQUEIO?
#bloqueio = True
bloqueio = False
if bloqueio:
    sql += " FOR UPDATE"

cursor.execute(sql, [c_ou_d])

# obtém os resultados
colabs = cursor.fetchall()

# escolhe dois colaboradores
i = random.randint(0, len(colabs)-1)
j = i
while i == j:
  j = random.randint(0, len(colabs)-1)
alguem = colabs[i]
outro = colabs[j]

# verifica qual o tipo de salário
if alguem[4] == "Salary":
  campo_update = "salario_anual"
else:
  campo_update = "valor_hora"
# prepara o sql
sql = f"update {tabela} set {campo_update} = {campo_update} * 0.1 where nome = '{alguem[0]}'"
# dá o aumento para esse(a) colaborador(a) :-)
cursor.execute(sql)

# espera um tempo, aqui é para caracterizar a chance de conflito >-) se estiver sem controle de concorrência
time.sleep(2)

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

# mostra o resultado
print(f" => {alguem[0]} e {outro[0]}  ganharam :-)")

# referências:
# https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-ROWS
# https://stackoverflow.com/questions/51002790/locking-a-specific-row-in-postgres
# https://pypi.org/project/psycopg2/
# https://www.postgresql.org/docs/current/sql-select.html