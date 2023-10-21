def menu():
    menu = """
=============== MENU ===============
[u] Criar Usuário
[c] Criar Conta Corrente
[d] Depositar
[s] Sacar
[e] Extrato
[lu] Listar Usuários
[lc] Listar Contas
[q] Sair
=> """
    return input(menu)

def realizar_saque( *, saldo, valor, extrato, limite, numero_saques, limite_saques ):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques

def realizar_deposito( saldo, valor, extrato, / ):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def visualizar_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(nome, data_nascimento, cpf, endereco, lista_usuarios):
    lista_usuarios[cpf]= {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}
    print(f"Usuário {nome} cadatrado com sucesso!")
    return lista_usuarios

def criar_conta_corrente(cpf, conta_corrente, agencia, lista_contas_correntes):
    lista_contas_correntes[conta_corrente] = {"agencia": agencia, "numero_conta": conta_corrente, "usuario": cpf}
    print(f"Conta {conta_corrente} criada!")
    return lista_contas_correntes

def listar_contas(lista_contas_correntes, lista_usuarios):
    print("Contas cadastrados no sistema: ")
    for chave in lista_contas_correntes:
        print("=========================================================")
        print("Agencia: " + lista_contas_correntes[chave]["agencia"])
        print("C/C: " + str(lista_contas_correntes[chave]["numero_conta"]))
        print("Cliente: " + lista_usuarios[lista_contas_correntes[chave]["usuario"]]["nome"])

def listar_usuarios(lista_usuarios):
    print("Usuários cadastrados no sistema: ")
    for chave, valor in lista_usuarios.items():
        print(valor)

def main():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = '0001'
    lista_usuarios = {}
    lista_contas_correntes = {}
    conta_corrente = 1

    while True:

        opcao = menu()

        if opcao == "u":
            cpf = str(input("Informe o CPF do cliente: "))

            if cpf in lista_usuarios:
                print("CPF já cadastrado!")
                continue

            nome = str(input("Informe o nome do cliente: "))
            data_nascimento = str(input("Informe a data de nascimento do cliente: "))
            logradouro = str(input("Informe o logradouro do cliente (sem número): "))
            nro = int(input("Informe o número do logradouro do cliente: "))
            bairro = str(input("Informe o bairro do cliente: "))
            cidade = str(input("Informe a cidade do cliente: "))
            sigla_estado = str(input("Informe a sigla do estado do cliente: "))

            endereco=f"{logradouro}, {nro} - {bairro} - {cidade}/{sigla_estado}"
            lista_usuarios = criar_usuario(nome, data_nascimento, cpf, endereco, lista_usuarios)

        elif opcao == "c":
            cpf = str(input("Informe o CPF do cliente para criação da conta: "))

            if cpf in lista_usuarios:
                lista_contas_correntes = criar_conta_corrente(cpf, conta_corrente, AGENCIA, lista_contas_correntes)
                conta_corrente+=1
            else:
                print("CPF não cadastrado! Por favor, primeiro cadastre o usário.")

        elif opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = realizar_deposito(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = realizar_saque(saldo=saldo,valor=valor,extrato=extrato,limite=limite,numero_saques=numero_saques,limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            visualizar_extrato(saldo, extrato=extrato)

        elif opcao == "lu":
            listar_usuarios(lista_usuarios)

        elif opcao == "lc":
            listar_contas(lista_contas_correntes, lista_usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()