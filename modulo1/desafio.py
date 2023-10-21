menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor_deposito = float(input("Infome o valor a ser depositado: "))

        if valor_deposito <= 0:
            print("Valor depositado inválido, por favor tente novamente.")
        else:
            saldo += valor_deposito
            extrato += f"Deposito: R$ {valor_deposito:.2f}\n"
    
    elif opcao == "s":
        if numero_saques < LIMITE_SAQUES:
            
            valor_saque = float(input("Infome o valor a ser sacado: "))

            if valor_saque > 500:
                print("Operação falhou! O valor do saque excede o limite.")
                continue

            if valor_saque > saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
                continue

            saldo -= valor_saque
            extrato += f"Saque: R$ {valor_saque:.2f}\n"
            numero_saques += 1
        else:
            print("Operação falhou! Número máximo de saques excedido.")

    elif opcao == "e":
        print("\n============= EXTRATO =============")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo : R$ {saldo:.2f}")
        print("=====================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")