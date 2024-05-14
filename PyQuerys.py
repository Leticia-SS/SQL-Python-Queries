# Teste de Performance 3

# Importar biblioteca CSV e SQL
import csv
import sqlite3
import pandas as pd

# Função para ler os arquivos CSV e exibir os dados
def ler_arquivo_csv(arquivo):
    with open(arquivo, mode="r", newline="") as csvfile:
        leitor_csv = csv.DictReader(csvfile)
        dados = [linha for linha in leitor_csv]
    return dados

# Ler os arquivos CSV
cargos = ler_arquivo_csv('Cargo.csv')
departamentos = ler_arquivo_csv('Departamento.csv')
dependentes = ler_arquivo_csv('Dependente.csv')
funcionarios = ler_arquivo_csv('Funcionario.csv')
salarios = ler_arquivo_csv('Salarios.csv')

    
# Ler dados da memória e conectar coma as tabelas

conn = sqlite3.connect(':memory:')

cargosDF = pd.read_csv('Cargo.csv')
departamentosDF = pd.read_csv('Departamento.csv')
dependentesDF = pd.read_csv('Dependente.csv')
funcionariosDF = pd.read_csv('Funcionario.csv')
salariosDF = pd.read_csv('Salarios.csv')

cargosDF.columns = ['ID_CARGO','DESCRICAO','SALARIO','NIVEL','CONTRATO']
departamentosDF.columns = ['ID_DEPARTAMENTO','NOME','ID_GERENTE','ANDAR','SALAS']
dependentesDF.columns = ['Nome','Dependente','ID_FUNCIONARIO','Parentesco','idade']
funcionariosDF.columns = ['Nome','ID_FUNCIONARIO','ID_CARGO','ID_DEPARTAMENTO','SALARIO','IDADE']
salariosDF.columns = ['Registro','Nome','ID_FUNCIONARIO','Cargo','ID_CARGO','Salario','Idade']

cargosDF = cargosDF.to_sql('Cargo', conn, index=False)
departamentosDF = departamentosDF.to_sql('Departamento', conn, index=False)
dependentesDF = dependentesDF.to_sql('Dependente', conn, index=False)
funcionariosDF = funcionariosDF.to_sql('Funcionario', conn, index=False)
salariosDF = salariosDF.to_sql('Salarios', conn, index=False)

# Listar individualmente as tabelas de: Funcionários, Cargos, Departamentos, Histórico de Salários e Dependentes em ordem crescente. 

consulta_funcionarios = 'SELECT * FROM Funcionario ORDER BY Nome ASC;'
resultado_funcionarios = pd.read_sql_query(consulta_funcionarios, conn)
print("Funcionários:")
print(resultado_funcionarios)

consulta_cargos = 'SELECT * FROM Cargo ORDER BY ID_CARGO ASC;'
resultado_cargos = pd.read_sql_query(consulta_cargos, conn)
print("\nCargos:")
print(resultado_cargos)

consulta_departamentos = 'SELECT * FROM Departamento ORDER BY ID_DEPARTAMENTO ASC;'
resultado_departamentos = pd.read_sql_query(consulta_departamentos, conn)
print("\nDepartamentos:")
print(resultado_departamentos)

consulta_salarios = 'SELECT * FROM Salarios ORDER BY Nome ASC;'
resultado_salarios = pd.read_sql_query(consulta_salarios, conn)
print("\nSalários:")
print(resultado_salarios)

consulta_dependentes = 'SELECT * FROM Dependente ORDER BY ID_FUNCIONARIO ASC;'
resultado_dependentes = pd.read_sql_query(consulta_dependentes, conn)
print("\nDependentes:")
print(resultado_dependentes)


# Listar os funcionários, com seus cargos, departamentos e os respectivos dependentes. 

consulta_02 = '''
    SELECT 
        f.Nome AS Funcionário,
        c.DESCRICAO AS Cargo,
        d.NOME AS Departamento,
        dep.Nome AS Dependente
    FROM 
        Funcionario f
        JOIN Cargo c ON f.ID_CARGO = c.ID_CARGO
        JOIN Departamento d ON f.ID_DEPARTAMENTO = d.ID_DEPARTAMENTO
        LEFT JOIN Dependente dep ON f.ID_FUNCIONARIO = dep.ID_FUNCIONARIO
    ORDER BY 
        f.Nome ASC;
'''

resultado_02 = pd.read_sql_query(consulta_02, conn)
print(resultado_02)

# Listar os funcionários que tiveram aumento salarial nos últimos 3 meses:

consulta_03 = '''
     SELECT 
        f.Nome AS Funcionário,
        MAX(f.SALARIO) AS Maior_Salário
    FROM 
        Funcionario f;
'''

resultado_03 = pd.read_sql_query(consulta_03, conn)
print(resultado_03)


# Listar a média de idade dos filhos dos funcionários por departamento.

dependentes_por_departamento = {}

for dependente in dependentes:
    id_funcionario = dependente['ID_FUNCIONARIO']
    departamento_funcionario = None
   
    for funcionario in funcionarios:
        if funcionario['ID_FUNCIONARIO'] == id_funcionario:
            id_departamento_funcionario = funcionario['ID_DEPARTAMENTO']
            
            for departamento in departamentos:
                if departamento['ID_DEPARTAMENTO'] == id_departamento_funcionario:
                    departamento_funcionario = departamento['NOME']
                    
            
    if departamento_funcionario:
        if departamento_funcionario not in dependentes_por_departamento:
            dependentes_por_departamento[departamento_funcionario] = []
        dependentes_por_departamento[departamento_funcionario].append(int(dependente['idade']))

for departamento, idades in dependentes_por_departamento.items():
    if idades:
        media_idade = sum(idades) / len(idades)
        print(f"Média de idade dos filhos no departamento {departamento}: {media_idade:.2f} anos")
    else:
        print(f"Não há informações de dependentes no departamento {departamento}")


# Consulta para listar os estagiários que possuem filhos

consulta_05 = '''
   SELECT 
        f.Nome AS Funcionário
    FROM 
        Funcionario f
        JOIN Cargo c ON f.ID_CARGO = c.ID_CARGO
        JOIN Dependente d ON f.ID_FUNCIONARIO = d.ID_FUNCIONARIO
    WHERE 
        c.NIVEL = 'Junior' AND
        d.Parentesco = 'filha'
    GROUP BY 
        f.Nome;
'''

resultado_consulta_05 = pd.read_sql_query(consulta_05, conn)
print(resultado_consulta_05)


# Listar o funcionário que teve o salário médio mais alto:

total_salarios = {}

repeticao_funcionario = {}

for salario in salarios:
    id_funcionario = salario['ID_FUNCIONARIO']
    salario_funcionario = float(salario['Salario'])

    if id_funcionario in total_salarios:
        total_salarios[id_funcionario] += salario_funcionario
        repeticao_funcionario[id_funcionario] += 1
    else:
        total_salarios[id_funcionario] = salario_funcionario
        repeticao_funcionario[id_funcionario] = 1

salario_medio_funcionario = {}
for id_funcionario, total_salario in total_salarios.items():
    ocorrencias = repeticao_funcionario[id_funcionario]
    salario_medio = total_salario / ocorrencias
    salario_medio_funcionario[id_funcionario] = salario_medio

funcionario_salario_maximo = max(salario_medio_funcionario, key=salario_medio_funcionario.get) # type: ignore

print(f"Funcionário com o salário médio mais alto:")
for funcionario in funcionarios:
    if funcionario['ID_FUNCIONARIO'] == funcionario_salario_maximo:
        print(f"Nome: {funcionario['Nome']}")
        print(f"ID: {funcionario['ID_FUNCIONARIO']}")
        print(f"Salário Médio: {salario_medio_funcionario[funcionario_salario_maximo]:.2f}")
        break


# Listar o analista que é pai de 2 (duas) meninas

consulta_07 = '''
    SELECT 
        f.Nome AS Funcionário
    FROM 
        Funcionario f
        JOIN Dependente d ON f.ID_FUNCIONARIO = d.ID_FUNCIONARIO
    WHERE 
        d.Parentesco = 'filho' 
    GROUP BY 
        f.Nome;
'''

resultado_consulta_07 = pd.read_sql_query(consulta_07, conn)
print(resultado_consulta_07)


# Listar o analista que tem o salário mais alto, e que ganhe entre 5000 e 9000
id_cargo_analista_marketing = None
for cargo in cargos:
    if cargo['DESCRICAO'] == 'Analista de Marketing':
        id_cargo_analista_marketing = cargo['ID_CARGO']
        break

if id_cargo_analista_marketing:
    analistas_marketing = [funcionario for funcionario in funcionarios if funcionario['ID_CARGO'] == id_cargo_analista_marketing]

    analistas_marketing_no_intervalo = [analista for analista in analistas_marketing if 5000 <= float(analista['SALARIO']) <= 9000]

    if analistas_marketing_no_intervalo:
        analista_marketing_salario_maximo = max(analistas_marketing_no_intervalo, key=lambda x: float(x['SALARIO']))
        
        print(f"Analista de Marketing com o salário mais alto entre 5000 e 9000:")
        print(f"Nome: {analista_marketing_salario_maximo['Nome']}")
        print(f"ID: {analista_marketing_salario_maximo['ID_FUNCIONARIO']}")
        print(f"Salário: {analista_marketing_salario_maximo['SALARIO']}")
    else:
        print("Não há Analistas de Marketing com salário dentro do intervalo de 5000 a 9000.")
else:
    print("O cargo 'Analista de Marketing' não foi encontrado na tabela de cargos.")
    

# Listar qual departamento possui o maior número de dependentes

dependentes_por_departamento = {}

for funcionario in funcionarios:
    id_departamento = funcionario['ID_DEPARTAMENTO']
    if id_departamento not in dependentes_por_departamento:
        dependentes_por_departamento[id_departamento] = 0
    
    dependentes_por_departamento[id_departamento] += 1

if dependentes_por_departamento:
    departamento_maior_dependentes = max(dependentes_por_departamento, key=dependentes_por_departamento.get) # type: ignore
    
    print(f"O departamento com o maior número de dependentes é o de ID: {departamento_maior_dependentes}, 
          com {dependentes_por_departamento[departamento_maior_dependentes]} dependentes.")
else:
    print("Não há dependentes associados a nenhum departamento.")

    
# Listar a média de salário por departamento em ordem decrescente

salarios_departamento = {}
funcionarios_departamento = {}

for funcionario in funcionarios:
    id_departamento = funcionario['ID_DEPARTAMENTO']
    salario_funcionario = float(funcionario['SALARIO'])
    
    if id_departamento not in salarios_departamento:
        salarios_departamento[id_departamento] = 0
        funcionarios_departamento[id_departamento] = 0
    
    salarios_departamento[id_departamento] += salario_funcionario
    funcionarios_departamento[id_departamento] += 1

media_salarios_por_departamento = {}
for id_departamento in salarios_departamento:
    total_salarios = salarios_departamento[id_departamento]
    numero_funcionarios = funcionarios_departamento[id_departamento]
    media_salarios_por_departamento[id_departamento] = total_salarios / numero_funcionarios

departamentos_ordenados = sorted(media_salarios_por_departamento, key=media_salarios_por_departamento.get, reverse=True) # type: ignore

print("Média de salário por departamento em ordem decrescente:")
for id_departamento in departamentos_ordenados:
    media_salario = media_salarios_por_departamento[id_departamento]
    print(f"Departamento ID: {id_departamento} - Média de Salário: {media_salario:.2f}")