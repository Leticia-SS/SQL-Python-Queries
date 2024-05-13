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

# Listar tabelas individualmente
print("Cargos:")
for cargo in cargos:
    print(cargo)

print("\nDepartamentos:")
for departamento in departamentos:
    print(departamento)

print("\nDependentes:")
for dependente in dependentes:
    print(dependente)

print("\nFuncionários:")
for funcionario in funcionarios:
    print(funcionario)

print("\nSalários:")
for salario in salarios:
    print(salario)
    

def listar_funcionarios_com_detalhes(funcionarios, cargos, departamentos, dependentes):
    funcionarios_com_detalhes = []
    for funcionario in funcionarios:
        cargo_id = funcionario['ID_CARGO']
        departamento_id = funcionario['ID_DEPARTAMENTO']
        dependente_id = funcionario['ID_FUNCIONARIO']
        
        cargo = next((c for c in cargos if c['ID_CARGO'] == cargo_id), None)
        departamento = next((d for d in departamentos if d['ID_DEPARTAMENTO'] == departamento_id), None)
        dependente = next((dep for dep in dependentes if dep['ID_FUNCIONARIO'] == dependente_id), None)
        
        funcionario_com_detalhes = {
            'Funcionário': funcionario,
            'Cargo': cargo,
            'Departamento': departamento,
            'Dependente': dependente
        }
        funcionarios_com_detalhes.append(funcionario_com_detalhes)
    return funcionarios_com_detalhes

funcionarios_com_detalhes = listar_funcionarios_com_detalhes(funcionarios, cargos, departamentos, dependentes)
for func in funcionarios_com_detalhes:
    print("Funcionário:", func['NOME'])
    print("Cargo:", func['ID_CARGO'])
    print("Departamento:", func['ID_DEPARTAMENTO'])
    print("Dependente:", func['ID_FUNCIONARIO'])
    print()
