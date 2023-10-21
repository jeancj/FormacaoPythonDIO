from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento        
        super().__init__(endereco)

    def __str__(self):
        return f"{self.cpf} | {self.nome} | {self.data_nascimento} | {self.endereco}"

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        excedeu_saldo = valor > self._saldo
        
        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True

        else:
            print("Operação falhou! O valor informado é inválido.")
    
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            return True
        
        else:
            print("Operação falhou! O valor informado é inválido.")

        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        self.limite = limite
        self.limite_saques = limite_saques
        super().__init__(numero, cliente)

    def sacar(self, valor):
        numero_saques = len( [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__ ] )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)            
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico():
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """
=============== MENU ===============
[u] Criar Usuário
[c] Criar Conta Corrente
[d] Depositar
[s] Sacar
[e] Extrato
[lu] Listar Clientes
[lc] Listar Contas
[q] Sair
=> """
    return input(menu)

def criar_cliente(clientes):
    cpf = str(input("Informe o CPF do cliente: "))
    cliente = buscar_cliente(cpf, clientes)

    if cliente:
        print(f"Cliente já cadastrado com o cpf {cpf}")
        return

    nome = str(input("Informe o nome do cliente: "))
    data_nascimento = str(input("Informe a data de nascimento do cliente: "))
    logradouro = str(input("Informe o logradouro do cliente (sem número): "))
    nro = int(input("Informe o número do logradouro do cliente: "))
    bairro = str(input("Informe o bairro do cliente: "))
    cidade = str(input("Informe a cidade do cliente: "))
    sigla_estado = str(input("Informe a sigla do estado do cliente: "))

    endereco=f"{logradouro}, {nro} - {bairro} - {cidade}/{sigla_estado}"

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("Cliente criado com sucesso")

def buscar_cliente(cpf, clientes):
    clientes_encontrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_encontrados[0] if clientes_encontrados else None    

def buscar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta")
        return
    
    return cliente.contas[0]

def realizar_deposito( clientes ):
    
    cpf = input("Informe o cpf do cliente: ")
    cliente = buscar_cliente( cpf, clientes )

    if not cliente:
        print(f"Cliente não encontrado com o cpf {cpf}")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)       

    conta = buscar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def realizar_saque(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print(f"Cliente não encontrado com o cpf {cpf}")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = buscar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def visualizar_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print(f"Cliente não encontrado com o cpf {cpf}")
        return

    conta = buscar_conta_cliente(cliente)
    
    if not conta:
        return
    
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_conta_corrente(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print(f"Cliente não encontrado com cpf {cpf}, não foi possível criar a conta")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso")

def listar_contas(contas):
    print("Contas cadastrados no sistema: ")
    
    for conta in contas:
        print("=========================================================")
        print(conta)

def listar_clientes(clientes):
    print("clientes cadastrados no sistema: ")
    for cliente in clientes:
        print("=========================================================")
        print(str(cliente))

def main():

    clientes = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "u":
            criar_cliente(clientes)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta_corrente(numero_conta, clientes, contas)

        elif opcao == "d":
            realizar_deposito(clientes)

        elif opcao == "s":
            realizar_saque(clientes)

        elif opcao == "e":
            visualizar_extrato(clientes)

        elif opcao == "lu":
            listar_clientes(clientes)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()            