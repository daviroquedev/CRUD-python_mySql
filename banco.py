# INSTALAR "pip mysql-connector-python"

# importando mysql connector

import mysql.connector

# conexao.commit() #edita  o banco de dados
# resultado = cursor.fetchall() #ler o banco de dados

#BANCO
class Conta:
    def __init__(self):
        self.con = mysql.connector.connect(host='localhost', user='root', password='root', database='dbContas',)
        self.cursor = self.con.cursor(buffered=True)

    # CADASTRA UM CLIENTE NOVO
    def cadastrar_cliente(self,numero,titular,saldo,limite,tipo):
        sql = f"INSERT INTO tbContas (numero, titular, saldo, limite, tipo) VALUES ('{numero}','{titular}','{saldo}','{limite}', '{tipo}')"
        self.cursor.execute(sql)
        self.con.commit()

    # EXIBE TODOS OS CLIENTES CADASTRADOS
    def consulta_clientes(self):
        sql = 'SELECT * FROM tbContas'
        self.cursor.execute(sql)
        clientes = self.cursor.fetchall()
        for cliente in clientes:
            print(cliente)

    # EXIBINDO CONTA INDIVIDUAL COM BASE NO ID PRIMARY KEY
    def consulta_cliente(self, idUser):
        sql = f"SELECT * FROM tbContas WHERE id_usuario LIKE '%{idUser}%'"
        self.cursor.execute(sql)
        id_usuario = self.cursor.fetchone()[0]
        #conta_nome = self.cursor.fetchone()[2]
        #conta_nome = self.cursor.fetchone()[1]
        #conta_saldo = self.cursor.fetchone()[2]
        print(f"id do usuario {id_usuario}")
        return id_usuario

    #CONSULTANDO O SALDO DA CONTA BASEADO NO TITULAR // PODE ALTERAR PRA ID
    def consulta_saldo(self, titular):
        sql = f"""SELECT saldo FROM tbContas WHERE titular LIKE '%{titular}%';
        """
        self.cursor.execute(sql)
        saldo = self.cursor.fetchone()
        print(f"Seu saldo é: R${saldo}")

    #CONSULTANDO CONTA E CAPTURANDO ID E SALDO
    def consulta_conta(self, id_cliente):
        sql = f"SELECT id_usuario, saldo, tipo FROM tbContas WHERE id_usuario = '{id_cliente}'"
        self.cursor.execute(sql)
        conta = self.cursor.fetchone()
        print(f'id e saldo e tipo {conta}')
        return conta

#CONTA CORRENTE CLASSE
class contaCorrente(Conta):
    def __init__(self):
        self.con = mysql.connector.connect(host='localhost', user='root', password='root', database='dbContas',)
        self.cursor = self.con.cursor(buffered=True)

    # MOSTRA TODAS DO TIPO
    def consulta_contas_correntes(self,tipo):
        sql = f"""SELECT * FROM tbContas WHERE tipo LIKE '%{tipo}%';
        """
        self.cursor.execute(sql)
        correnteContas = self.cursor.fetchall()
        for userCorrente in correnteContas:
            print(userCorrente)


    #DEPOSITO TIPO CORRENTE SEM TAXA DE DEPOSITO
    def deposito(self,tipo, valor,idUser):
        taxa = 0
        id_cliente = self.consulta_cliente(idUser)
        print (f"id conta corrente do deposito {id_cliente}")
        id_conta, saldo, tipoConta = self.consulta_conta(id_cliente)
        novo_saldo = saldo + valor if tipo == 'corrente' else print(f"Operação negada, conta do tipo {tipo}")
        sql = f"""UPDATE tbContas
              SET saldo = {novo_saldo}
              WHERE id_usuario = {id_cliente}"""
        print(novo_saldo)
        print(id_cliente)
        self.cursor.execute(sql)
        self.con.commit()

    # SAQUE CORRENTE COM TAXA DE 0.10
    def saque(self,tipo, valor,idUser):
        taxa = 0.10
        id_cliente = self.consulta_cliente(idUser)
        print(f"id conta corrente do deposito {id_cliente}")
        id_conta, saldo, tipoConta  = self.consulta_conta(id_cliente)
        novo_saldo = saldo - valor - taxa if tipo == 'corrente' else print(f"Operação negada, conta do tipo {tipoConta}")
        sql = f"""UPDATE tbContas
                      SET saldo = {novo_saldo}
                      WHERE id_usuario = {id_cliente}"""
        print(novo_saldo)
        print(id_cliente)
        self.cursor.execute(sql)
        self.con.commit()

#SUB CLASSE POUPANÇA
class contaPoupanca(Conta):
    def __init__(self):
        self.con = mysql.connector.connect(host='localhost', user='root', password='root', database='dbContas',)
        self.cursor = self.con.cursor(buffered=True)

    #DEPOSITO POUPANÇA
    def deposito(self,tipo, valor,idUser):
        id_cliente = self.consulta_cliente(idUser)
        print (f"id conta corrente do deposito {id_cliente}")
        id_conta, saldo, tipoConta = self.consulta_conta(id_cliente)
        novo_saldo = saldo + valor if tipo == 'poupança' else print(f"Operação negada, conta do tipo {tipoConta}")
        sql = f"""UPDATE tbContas
              SET saldo = {novo_saldo}
              WHERE id_usuario = {id_cliente}"""
        print(novo_saldo)
        print(id_cliente)
        self.cursor.execute(sql)
        self.con.commit()

    #SAQUE POUPANÇA
    def saque(self,tipo, valor,idUser):
        id_cliente = self.consulta_cliente(idUser)
        print(f"id conta poupança do deposito {id_cliente}")
        id_conta, saldo, tipoConta = self.consulta_conta(id_cliente)
        novo_saldo = saldo - valor if tipo == 'poupanca' else print(f"Operação negada, conta do tipo {tipoConta}")
        sql = f"""UPDATE tbContas
                      SET saldo = {novo_saldo}
                      WHERE id_usuario = {id_cliente}"""
        print(novo_saldo)
        print(id_cliente)
        self.cursor.execute(sql)
        self.con.commit()

    #APLICANDO RENDIMENTO POUPANÇA
    def rendimento(self,tipo,idUser):
        taxa = 1.01
        id_cliente = self.consulta_cliente(idUser)
        print(f"Aplicando rendimento poupança no id {id_cliente}")
        id_conta, saldo, tipoConta = self.consulta_conta(id_cliente)
        novo_saldo = saldo * taxa if tipo == 'poupanca' else print(f"Operação negada, conta do tipo {tipoConta}")
        sql = f"""UPDATE tbContas SET saldo = {novo_saldo} WHERE id_usuario = {id_cliente}"""
        print(novo_saldo)
        print(id_cliente)
        self.cursor.execute(sql)
        self.con.commit()

#DELETAR CONTA IF SALDO ZERADO
class deletarConta(Conta):
    def __init__(self):
        self.con = mysql.connector.connect(host='localhost', user='root', password='root', database='dbContas',)
        self.cursor = self.con.cursor(buffered=True)

    def deleteAcc(self,idUser):
        id_cliente = self.consulta_cliente(idUser)
        id_conta, saldo, tipoConta = self.consulta_conta(id_cliente)

        if saldo <= 0:
            print(f"saldoooo {saldo}")
            print(f"Conta que será deletada {id_cliente}")
            sql = f"""DELETE FROM tbContas WHERE id_usuario = {id_cliente}"""
            self.cursor.execute(sql)
            self.con.commit()
        else:
            print("Conta com saldo não pode ser encerrada")


#CHAMADA DAS CLASSES
conta = Conta()
corrente = contaCorrente()
poupanca = contaPoupanca()
delet = deletarConta()

#COMANDO PARA CONSULTAR CONTA COM BASE NO ID
#conta.consulta_conta('28')

#COMANDO PARA DELETAR CONTA COM BASE NO ID SE SALDO ZERADO
#delet.deleteAcc(20)

#COMANDO PARA CADASTRAR UMA NOVA CONTA
#conta.cadastrar_cliente('001','abc','4000','1000','poupanca')

#COMANDO PRA CONSULTAR UM ID DE USUARIO
#corrente.consulta_cliente('24')

#COMANDO PARA VER TODAS AS CONTAS DO TIPO CORRENTE || POUPANCA
#corrente.consulta_contas_correntes('poupanca')

#COMANDO DE DEPOSITO EM CONTA CORRENTE SEM TAXA DE DEPOSITO
#corrente.deposito('corrente',100,'24')

#COMANDO DE SAQUE DE CONTA CORRENTE COM 0.10 DE TAXA
#corrente.saque('corrente',500,'28')

#COMANDO PARA APLICAR RENDIMENTO A CONTA DO TIPO POUPANCA COM TIPO POUPANCA E ID DA CONTA
#poupanca.rendimento('poupanca','25')

#COMANDO PARA VER ID, SALDO E TIPO DA CONTA
#conta.consulta_conta('3')

#CONSULTA DE SALDO POR NOME TITULAR PODE SER ALTERADO POR ID
#conta.consulta_saldo('davi')

