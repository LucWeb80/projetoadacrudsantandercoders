# [Luciano Weber, Arthur Dalcin, Arthur Gomes, Davi Ribeiro, Thais Fernandes]

import json
import os
import uuid
import random
import sys

# -----------------------
# load settings
# -----------------------
sys.path.append('./data/')
from data import settings

# -----------------------
# SYSTEM functions 
# -----------------------
# não alterar nada das funções de system
def criar_transacoes(num_transacoes, proporcao_categorias, seed=settings.seed):
    assert sum([proporcao_categorias[k] for k in proporcao_categorias])==1, '`proporcao_categorias` não soma 100%! Favor rever.'

    # garantir reprodutibilidade dos valores
    random.seed(seed)

    # Calcula o número de transações por categoria com base na proporção
    numero_transacoes_por_categoria = {categoria: int(num_transacoes * proporcao) for categoria, proporcao in proporcao_categorias.items()}
    
    transacoes = []
    
    # Gera as transações
    for categoria, quantidade in numero_transacoes_por_categoria.items():
        for _ in range(quantidade):
            transacao = {
                "UUID": str(uuid.uuid4()),
                "valor": round(random.uniform(1.0, 1000.0), 2),  # Preço aleatório entre 1 e 1000
                "categoria": categoria
            }
            transacoes.append(transacao)
    
    return transacoes

def salvar_json(transacoes, path2save, filename):
    # create path if not exist
    if not os.path.exists(path2save):
        os.makedirs(path2save)
    with open(os.path.join(path2save,filename), "w") as file:
        json.dump(transacoes, file, indent=4)
    print(f"Arquivo salvo em: {os.path.abspath(os.path.curdir)+'/'+path2save+'/'+filename}")

def criar_bd(num_transacoes:int = 10000, proporcao_categorias:list = settings.categorias_proporcao, path2save="./data", filename='transactions.json'):
    salvar_json(criar_transacoes(num_transacoes,  proporcao_categorias),
                path2save, filename
    )

def load_bd(filepath='./data/transactions.json'):
    with open(filepath, "r") as file:
        bd = json.load(file)
    return bd

def tela_inicial():
    print("Bem-vindo <teu nome inteiro aqui>!")
    print('conta: 0000001-0')
    print("\nEste programa permite gerenciar transações de sua conta pessoal.")
    print("\nEscolha uma das opções abaixo:")
    print("1. Visualizar relatórios")
    print("2. Cadastrar transações")
    print("3. Editar transações")
    print("4. Excluir transações")
    print("-" * 10)
    print("0. Sair")
    print('\n')

# Funções criadas para evitar repetição no código e melhorar legibilidade e compreensão
def limpar_console():
    os.system('cls')

def aguarda_usuario():
    input("\nPressione qualquer tecla para continuar...")

# -----------------------
# PROGRAM functions 
# -----------------------
## Todas as linhas abaixo foram escritas pelos quatro autores, em reunião online em 18 de agosto de 2024.
def run():
    """
    Esta é a função principal que vai rodar o programa
    """  
    while True:
        limpar_console()
        tela_inicial()
        opcao = input("Digite uma opção: ")
        
        if opcao == "1":
            if len(bd) == 0:
                limpar_console()
                print ("Não há transações cadastradas.")
                aguarda_usuario()
                continue
            visualizar_relatorios()
        elif opcao == "2":
            cadastrar_transacao()
        elif opcao == "3":
            if len (bd) == 0:
                limpar_console()
                print ("Não há transações cadastradas.")
                aguarda_usuario()
                continue
            editar_transacao_por_ID()
        elif opcao == "4":
            if len (bd) == 0:
                limpar_console()
                print ("Não há transações cadastradas.")
                aguarda_usuario()
                continue
            excluir_transacao()
        elif opcao == "0":
            print("\nSaindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
            aguarda_usuario()

def visualizar_relatorios():
    """
    Mostra um menu de opções no qual gera relatórios com base na escolha do usuário.
    """
    while True:
        limpar_console()
        print("Escolha um relatório para ser visualizado:\n")
        print("1. Exibir soma total de transações")
        print("2. 5 transações mais caras")
        print("3. 5 transações medianas")
        print("4. 5 transações mais baratas")
        print("5. Exibir média total")
        print("6. Consultar transação por ID")
        print("----------")
        print("0. Voltar ao menu principal")
        opcao = input("\nDigite uma opção: ")
        
        if opcao == "1":
            calcular_total_transacoes()
        elif opcao == "2":
            mostrar_m5_transacoes('max')
        elif opcao == "3":
            mostrar_m5_transacoes('media')
        elif opcao == "4":
            mostrar_m5_transacoes('min')
        elif opcao == "5":
            calcular_media()
        elif opcao == "6":
            consultar_transacao_por_ID()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def salvar_relatorio(dados):
    """
    Salvar o relatório gerado em .txt
    \nAplicar esta função em todos os relatórios listados em `visualizar_relatorios`
    """
    with open("relatorio.txt", "w") as file:
        file.write(str(dados))


def calcular_total_transacoes():
    """
    Calcula o valor total de transações da conta.
    """
    limpar_console()
    total = sum(transacao['valor'] for transacao in bd)
    print(f"O valor total das transações é: R${total:.2f}")
    
    save_report = input("Deseja salvar o relatório? (s/n): ")
    if save_report.lower() == 's':
        salvar_relatorio(total)
        print(f"Relatório salvo com sucesso.")
        aguarda_usuario()
    elif save_report.lower() == 'n':
        pass
    else:
        print("Opção inválida. Tente novamente.")
        aguarda_usuario()

def mostrar_m5_transacoes(m):
    """
    Mostra as m5 transações realizadas, sendo m parâmetro que deve ser adicionada à função.
    """
    limpar_console()
    
    if m == 'max':
        transacoes_ordenadas = sorted(bd, key=lambda x: x['valor'], reverse=True)[:5]
    elif m == 'min':
        transacoes_ordenadas = sorted(bd, key=lambda x: x['valor'])[:5]
    elif m == 'media':
        media = sum(transacao['valor'] for transacao in bd) / len(bd)
        transacoes_ordenadas = sorted(bd, key=lambda x: abs(x['valor'] - media))[:5]
    
    print()
    for i, transacao in enumerate(transacoes_ordenadas):
        print(f"{i+1}. {transacao['categoria']} - R$ {transacao['valor']:.2f}")

    save_report = input("Deseja salvar o relatório? (s/n): ")
    if save_report.lower() == 's':
        salvar_relatorio(transacoes_ordenadas)
        print(f"Relatório salvo com sucesso.")
        aguarda_usuario()
    elif save_report.lower() == 'n':
        aguarda_usuario()
    else:
        print("Opção inválida. Tente novamente.")
        aguarda_usuario()


def calcular_media():
    """
    Calcula a média dos valores das transações.
    """
    limpar_console()
    media = sum(transacao['valor'] for transacao in bd) / len(bd)
    print(f"A média das transações é: R${media:.2f}")

    save_report = input("Deseja salvar o relatório? (s/n): ")
    if save_report.lower() == 's':
        salvar_relatorio(media)
        print(f"Relatório salvo com sucesso.")
    elif save_report.lower() == 'n':
        pass
    else:
        print("Opção inválida. Tente novamente.")
    aguarda_usuario()

def consultar_transacao_por_ID():
    limpar_console()
    id = input("Digite o UUID: ")

    for transacao in bd:
        if transacao['UUID'] == id:
            print(f"Transação encontrada!")
            print(f"{transacao['categoria']} - R$ {transacao['valor']:.2f}")
            aguarda_usuario()
            return
            
    print("Transação não encontrada")
    aguarda_usuario()
    return 


def cadastrar_transacao():
    """
    Cadastra uma nova transação.
    """
    limpar_console()
    try:
        valor = float(input("Digite o valor da transação: "))
        categoria = input("Digite a categoria da transação: ")
    except ValueError:
        print("\nValor inválido. Tente novamente.")
        aguarda_usuario()
        return
    nova_transacao = {
        "UUID": str(uuid.uuid4()),
        "valor": round(valor, 2),
        "categoria": categoria
    }
    bd.append(nova_transacao)
    print()
    salvar_json(bd, "./data", "transactions.json")
    print("Transação cadastrada com sucesso.")
    aguarda_usuario()

def editar_transacao_por_ID():
    """
    Edita uma transação específica pelo seu UUID.
    """
    limpar_console()
    id_editar = input("Digite o UUID da transação a ser editada: ")
    transacao = next((t for t in bd if t['UUID'] == id_editar), None)
    
    if transacao:
        try:
            novo_valor = float(input(f"Digite o novo valor (atual: R${transacao['valor']}): R$"))
        except ValueError:
            print("\nValor inválido. Tente novamente.")
            aguarda_usuario()
            return
        nova_categoria = input(f"Digite a nova categoria (atual: {transacao['categoria']}): ")
        
        transacao['valor'] = round(novo_valor, 2)
        transacao['categoria'] = nova_categoria
        
        salvar_json(bd, "./data", "transactions.json")
        print("Transação editada com sucesso.")
    else:
        print("Transação não encontrada.")
        aguarda_usuario()

def excluir_transacao():
    """
    Exclui uma transação específica pelo UUID.
    """
    limpar_console()
    id_excluir = input("Digite o UUID da transação a ser excluída: ")
    transacao = next((t for t in bd if t['UUID'] == id_excluir), None)
    
    if transacao:
        bd.remove(transacao)
        salvar_json(bd, "./data", "transactions.json")
        print("Transação excluída com sucesso.")
        aguarda_usuario()
    else:
        print("Transação não encontrada.")

        aguarda_usuario()

if __name__ == "__main__":
    
    # -----------------------
    # NÃO ALTERAR ESTE BLOCO
    # -----------------------
    # criar o banco de dados caso ele não exista
    print(os.path.abspath('.'))
    if not os.path.exists('./data/transactions.json'):
        criar_bd()
    
    # load bd 
    bd = load_bd()
    # -----------------------

    # -----------------------
    # ABAIXO PODE ALTERAR
    # -----------------------
    #limpar console (opcional)
    os.system('cls' if os.name == 'nt' else 'clear')
    # inicia o programa
    run()
