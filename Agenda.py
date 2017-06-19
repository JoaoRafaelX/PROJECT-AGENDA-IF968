#André Loponte e João Rafael
# -*- coding: utf8 -*-
import sys
from shutil import move


########################PRINCIPAL########################

def processarComandos(comandos) :

    #Checa se o usuário colocou os comandos
    if len(comandos) - 1:
        switchOperacoes = {"A": adicionar,
                           "A+": adicionarDesorganizado,
                           "R": remover,
                           "F": fazer,
                           "P": priorizar,
                           "L": listar}

        #Evita que o dicionário devolva um erro caso a key não esteja nele, como um default
        switchOperacoes.get(comandos[1].upper(), ajuda)(comandos[2:])
        print("")

    #Caso o usuário tenha rodado sem os comandos
    else:
        ajuda()


def ajuda(ignorarComandos = ""):
    print("\n\nPROJECT AGENDA por André Loponte e João Rafael\n" +
          "\nAs operações são: [A]dicionar, [R]emover, [F]azer, [P]riorizar e [L]istar\n" +
          "É necessário seguir a ordem, porém, é possível usar [A+] para ignorá-la\n" +
          "Exemplo da ordem padrão para adicionar uma atividade:\n" +
          "A 21102015 0429 (P) Descrição @Contexto +Projeto \n\n" +
          "Data e Hora são opcionais, mas devem ser colocadas neste formato, sem símbolos\n" +
          "Descrição é como será chamada a atividade, é um atributo livre, mas necessário\n" +
          "Contexto indica onde a atividade será realizada e deve possuir um @ antes\n" +
          "Projeto serve para agrupar atividades relacionadas e deve possuir um + antes\n" +
          "\nAs operações [R]emover e [F]azer removem a atividade do arquivo todo.txt\n" +
          "A diferença é que a [F]azer armazena a atividade no arquivo done.txt\n" +
          "Porém é necessário informar o Número da atividade, que é mostrado na [L]istar\n" +
          "A operação [L]istar mostra todas as atividades armazenadas de forma ordenada\n" +
          "Todas as atividades são ordenadas de acordo com sua prioridade, data e hora\n" +
          "\nA prioridade é um atributo importante que é adicionado na operação [P]riorizar\n" +
          "[P]riorizar também precisa do Número da atividade, mas seguido de alguma letra\n" +
          "Essa letra serve para a ordenação, também sendo alterada pelo mesmo comando\n" +
          "Caso não seja inserida nenhuma letra, a atividade terá sua prioridade removida\n" +
          "Note que prioridade pode ser colocada entre a Hora e a Descrição ao [A]dicionar\n" +
          "\nExemplos de operações: A 21102015 0429 Desc Extras| R 7 | F 4 | P 1 A | P 2\n" +
          "Listar: L | L 3 | L 1 4 | L A | L [Desc] | L Data 21102015 (Hora, Cont, Proj)")


def organizar(item, ordem = True):

    extras = {"data": ["", dataValidacao],
              "hora": ["", horaValidacao],
              "prio": ["", prioridadeValidacao],
              "cont": ["", contextoValidacao],
              "proj": ["", projetoValidacao]}

    descricao = ""
    for i in range(len(item)):
        #Só pra comentar os testes
        if item[0].startswith("#"):
            return False
        validado = False
        for j in extras:
            if not validado:
                #Primeira parte checa se a Data é o primeiro item
                if (not j == "data" or not i) or not ordem:
                    #Segunda parte checa se a Hora está antes da descrição e prioridade
                    if not j == "hora" or (not descricao.strip() and not extras["prio"][0]) or not ordem:
                        #Terceira parte checa se a prioridade está antes da descrição
                        if not j == "prio" or not descricao.strip() or not ordem:

                            #Caso o item seja validado, ele recebe o atributo anterior, que na maioria das vezes é ""
                            #Porém, caso a operação seja desordenada, o atributo anterior é adicionado à descrição
                            extras[j][0], item[i], validado = validar(extras[j][0], item[i], extras[j][1])


        #Finalmente, checa se o item não está vazio e foi encaixado em nenhum dos atributos...
        #E também se já foram colocados o contexto e o projeto
        #Nota especial: Uma string com o valor "False" é verdadeira.
        if (not validado or (validado == "Schrödinger" and not ordem) and item[i]
            and ((not extras["cont"][0] and not extras["proj"][0]) or not ordem)):
            descricao += " " + item[i]

    extrasFinais = [extras["data"][0],
                    extras["hora"][0],
                    extras["prio"][0],
                    extras["cont"][0],
                    extras["proj"][0]]

    #Finaliza caso tenha dado tudo certo
    descricao = descricao.strip()

    if descricao:
        return (descricao, extrasFinais)


#Função que facilita a organização
#Roda a validação e checa se o atributo já esta preenchido
def validar(atributo, item, funcao):
    if funcao(item):
        if atributo:
            #Schrödinger que vai identificar se o atributo anterior vai para a descrição ou não
            return item, atributo, "Schrödinger"
        return item, atributo, True
    return atributo, item, False


def remontarTuplas(itens):
    tuplas = []
    for i in itens:
        tuplas.append(desprepararItem(i))
    return tuplas


########################OPERAÇÕES########################

def adicionar(comandos, ordem = True):

    item = organizar(comandos, ordem)

    #Caso o item venha sem descrição...
    #Ou não venha item
    while not item:
        if not ordem:
            print("Atividade sem descrição!\n" +
              "Deseja checar ordenadamente?")
            if simNao():
                item = organizar(comandos, True)
                ordem = True
                print("")
            else:
                return False
        else:
            print("Atividade sem descrição!\n")
            return False

    #Mostra o item na tela organizadinho para a confirmação
    mostrarItem(prepararItem(item), True)

    #Confirmação
    print("\nDeseja inserir esta atividade?")
    if not simNao():
        print("Operação cancelada!")
        return False

    #Pega todas as partes e junta em uma string
    texto = ""
    for i in soltarItem(item):
        if i:
            texto = (texto + " " + i).strip()

    #Então dá um append simples
    if texto:
        try:
            f = open(arquivo_TODO, "a")
            f.write(texto + "\n")
            f.close()
        except IOError as err:
            print("Ocorreu um erro ao tentar adicionar a tarefa ao arquivo!")
            print(err)


def adicionarDesorganizado(comandos):
    #Somente muda uma variável no Adicionar
    return adicionar(comandos, False)


#Ajuda no Remover, Fazer e Priorizar
def prepararOperacao(comandos):

    if soDigitos(comandos):
        numero = int(comandos)
        arquivo = lerArquivo()

        itens = []
        for i in range(len(arquivo)):
            itens.append(prepararItem(arquivo[i]))

        itens = ordenar(itens)
        if numero < 1 or numero > len(itens):
            print("Número inválido")
        else:
            return itens, numero
    return "", ""


def remover(comandos):

    itens = numero = ""
    if len(comandos) == 1:
        itens, numero = prepararOperacao(comandos[0])

    if itens and numero:
        print(mostrarItem(itens[numero - 1]))
        print("Realmente deseja deletar esta atividade?")
        if simNao():
            #Deleta o item e remonta o todo.txt
            itens.pop(numero - 1)
            escreverArquivo(remontarTuplas(itens))
            return True
    else:
        print("Comando inválido!")
        return False


def fazer(comandos):

    itens = numero = ""
    if len(comandos) == 1:
        itens, numero = prepararOperacao(comandos[0])

    if itens and numero:
        print(mostrarItem(itens[numero - 1]))
        print("Essa é atividade que deseja terminar?")
        if simNao():

            #Dá um append no arquivo done.txt
            done = lerArquivo(True)
            terminado = itens.pop(numero - 1)
            terminado = desprepararItem(terminado)

            texto = ""
            for i in soltarItem(terminado):
                if i:
                    texto = (texto + " " + i).strip()

            if texto:
                try:
                    f = open(arquivo_DONE, "a")
                    f.write(texto + "\n")
                    f.close()
                except IOError as err:
                    print("Ocorreu um erro ao tentar adicionar a tarefa ao arquivo!")
                    print(err)

            #Então deleta da lista e remonta o todo.txt
            escreverArquivo(remontarTuplas(itens))

            return True
    else:
        print("Comando inválido!")
    return False


def priorizar(comandos):

    #Pega a prioridade tanto como A ou (A)
    itens = numero = prioridade = ""
    if len(comandos) > 0 and len(comandos) <= 2:
        itens, numero = prepararOperacao(comandos[0])
        if len(comandos) == 2:
            if len(comandos[1]) == 1:
                if comandos[1] >= "A" and comandos[1] <= "Z":
                    prioridade = "(" + comandos[1] + ")"
            elif len(comandos[1]) == 3:
                if comandos[1][1] >= "A" and comandos[1][1] <= "Z":
                    prioridade = "(" + comandos[1][1] + ")"

    if itens and numero:
        print(mostrarItem(itens[numero - 1]))
        if prioridade:
            print("Deseja colocar prioridade", prioridade, "nesta atividade?")
        else:
            print("Deseja remover a prioridade desta atividade?")
        if simNao():
            #Muda a prioridade na lista
            itens[numero - 1][2] = prioridade
            #Então remonta o todo.txtx
            escreverArquivo(remontarTuplas(itens))
            return True
    else:
        print("Comando inválido!")
    return False


def listar(comandos):

    #Cria a lista ordenada e pronta para ser mostrada
    arquivo = lerArquivo()
    itens = []
    for i in range(len(arquivo)):
        itens.append(prepararItem(arquivo[i]))
    itens = ordenar(itens)

    print("\n")
    if len(comandos) == 1:

        #Caso o comando seja um ID
        if soDigitos(comandos[0]):
            numero = int(comandos[0])
            if numero <= len(itens) and numero > 0:
                printCores((str(numero) + ". " + mostrarItem((itens[numero - 1]))), itens[numero - 1][2])
                return True
            else:
                print("Atividade de número", str(numero), "não foi encontrada!")
                return False

        #Caso o comando seja uma prioridade
        elif prioridadeValidacao(comandos[0], True):
            prio = rawPrio(comandos[0], True)
            for i in range(len(itens)):
                #Impedir que dê erro de index quando não tem prioridade
                if itens[i][2]:
                    if prio == itens[i][2][1].upper():
                        printCores((str(i + 1) + ". " + mostrarItem(itens[i])), itens[i][2])
            return True


    elif len(comandos) == 2:
        #Caso o comando seja um alcance de IDs
        if soDigitos(comandos[0] + comandos[1]):
            numeroA = int(comandos[0])
            numeroB = int(comandos[1])
            if numeroA > numeroB:
                numeroB, numeroA = numeroA, numeroB

            numeroA = tratarNumeros(numeroA, len(itens))
            numeroB = tratarNumeros(numeroB, len(itens))

            for i in range(numeroA - 1, numeroB):
                printCores((str(i + 1) + ". " + mostrarItem(itens[i])), itens[i][2])
            return True

        #Caso o comando seja uma Data
        elif comandos[0].upper() == "DATA" and dataValidacao(comandos[1]):
            casoComando(itens, comandos[1], 0, dataPesquisa)
            return True
        #Caso o comando seja uma Hora
        elif comandos[0].upper() == "HORA" and horaValidacao(comandos[1]):
            casoComando(itens, comandos[1], 1, horaPesquisa)
            return True
        #Caso o comando seja um Contexto
        elif comandos[0].upper() == "CONT" and contextoValidacao(comandos[1]):
            casoComando(itens, comandos[1], 4, projcontPesquisa)
            return True        
        #Caso o comando seja um Projeto
        elif comandos[0].upper() == "PROJ" and projetoValidacao(comandos[1]):
            casoComando(itens, comandos[1], 5, projcontPesquisa)
            return True

    if len(comandos):
        #Caso o comando seja uma Descrição
        if comandos[0][0] == "[" and comandos[-1][-1] == "]":
            descricao = (" ".join(comandos)[1:-1]).upper()
            if descricao:
                for i in range(len(itens)):
                    if descricao in itens[i][3].upper():
                        printCores((str(i + 1) + ". " + mostrarItem(itens[i])), itens[i][2])
            return True
        else:
            print("Comando Inválido")
            return False

    #Caso o comando não se encaixe em nenhum dos casos passados...
    #Ele age normalmente, como se tivesse sido somente um L normal
    #E sim, eu tenho muita saudade do Switch case
    else:
        for i in range(len(itens)):
            printCores((str(i + 1) + ". " + mostrarItem(itens[i])), itens[i][2])


#Só para ajudar nessa parte do alcance
def tratarNumeros(numero, lenItens):
    if numero > lenItens:
        numero = lenItens
    if numero < 1:
        numero = 1
    return numero


#Diminuir a repetição nos casos do listar
def casoComando(itens, comandos, atrib, funcao):
    for i in range(len(itens)):
        if funcao(comandos) == itens[i][atrib].upper():
            printCores((str(i + 1) + ". " + mostrarItem(itens[i])), itens[i][2])

#Funções usadas no casoComando
def dataPesquisa(data):
    return data[0:2] + "/" + data[2:4] + "/" + data[4:]
def horaPesquisa(hora):
    return hora[0:2] + "H" + hora[2:] + "M"
def projcontPesquisa(projcont):
    return projcont.upper()

########################ARQUIVO########################

#Pega todas as linhas do arquivo e passa pelo lerItem
def lerArquivo(done = False):

    #Append+ para criar o arquivo caso ele não exista sem precisar de um Try Catch
    if done:
        f = open(arquivo_DONE, "a+")
    else:
        f = open(arquivo_TODO, "a+")
    f.seek(0)
    linhas = f.readlines()
    f.close()
    linhas = limparLista(linhas)

    tuplas = []
    for i in range(len(linhas)):
        if linhas[i]:
            item = linhas[i].split(" ")
            #Organiza para virar tupla
            item = organizar(item)
            if item:
                tuplas.append(item)

    return tuplas


def escreverArquivo(lista):

    #Cria um arquivo de backup pra evitar problemas
    bak = open(arquivo_BKUP, "w")
    for i in lista:
        item = soltarItem(i)
        texto = ""
        #Evita qualquer espaço vazio no arquivo
        for j in item:
            if j:
                texto = (texto + " " + j).strip()
        if texto:
            bak.write(texto + "\n")
    bak.close()

    #Tive que importar o move da SHUTIL pra substituir o arquivo antigo
    move(arquivo_BKUP, arquivo_TODO)


########################ORDENAR########################

def ordenar(itens):

    #Prioridade
    dictPrio = ordenarPrioridade(itens)
    for i in dictPrio:
        #Data e Hora
        dictPrio[i] = ordenarDataHora(dictPrio[i])

    #Transforma em lista
    itens = dictLista(dictPrio)

    return itens


def ordenarDataHora(itens):

    #Junta a data com a hora e organiza de forma crescente
    for i in range(len(itens)):
        for j in range(len(itens) - (i + 1)):
            iDataHora = rawDataHora(itens[j][0], itens[j][1])
            jDataHora = rawDataHora(itens[j+1][0], itens[j+1][1])
            if iDataHora > jDataHora:
                itens[j], itens[j+1] = itens[j+1], itens[j]

    return itens


def ordenarPrioridade(itens):

    #Organiza as prioridades na ordem alfabética
    for i in range(len(itens)):
        for j in range(len(itens) - (i + 1)):
            if rawPrio(itens[j][2]) < rawPrio(itens[j+1][2]):
                itens[j], itens[j+1] = itens[j+1], itens[j]

    #Cria um dicionário com as prioridades usadas
    dictPrio = {}
    for i in range(len(itens)):
        prio = rawPrio(itens[i][2])
        if not dictPrio.get(prio, ""):
            dictPrio[prio] = []

    #Agrupa listas dentro das prioridades
    for i in dictPrio:
        for j in range(len(itens)):
            if rawPrio(itens[j][2]) == i:
                dictPrio[i].append(itens[j])

    return dictPrio


def dictLista(dicionario):

    #Pega todos as keys de um dicionário e as coloca em uma lista
    keys = []
    for i in dicionario:
        keys.append(i)

    #Organiza as keys
    for i in range(len(keys)):
        for j in range(len(keys) - (i + 1)):
            if keys[j] > keys[j+1]:
                    keys[j], keys[j+1] = keys[j+1], keys[j]

    #Então coloca os na lista que vai ser devolvida
    lista = []
    for i in range(len(keys)):
        for j in dicionario:
            if j == keys[i]:
                for k in range(len(dicionario[j])):
                    lista.append(dicionario[j][k])

    return lista


def rawDataHora(data, hora):

    if data and hora:
        return int(data[6:] + data[3:5] + data[0:2] + hora[0:2] + hora [3:5])
    elif data:
        #Caso só tenha data, a hora fica acima do limite
        return int(data[6:] + data[3:5] + data[0:2] + "2401")
    elif hora:
        #Caso só tenha hora, a data fica acima do limite
        return int("100000000" + hora[0:2] + hora[3:5])
    #Caso não tenha nada, a hora fica acima do limite de ambas
    return 1000000002402

def rawPrio(prio, listar = False):

    if prio:
        if len(prio) == 1 and listar:
            return prio.upper()
        return prio[1].upper()
    return "| |"


########################VALIDAÇÃO########################

def prioridadeValidacao(pri, listar = False):

    pri = pri.upper()

    if listar and len(pri) == 1:
        pri = "(" + pri + ")"
    if len(pri) == 3:
        if pri[0] == "(" and pri[2] == ")":
            if pri[1] >= "A" and pri[1] <= "Z":
                return True
    return False

def horaValidacao(horaMin):

    if len(horaMin) == 4 and soDigitos(horaMin):
        if int(horaMin[0:2]) < 24 and int(horaMin[2:4]) < 60:
            return True
    return False

def dataValidacao(data):

    if len(data) == 8 and soDigitos(data):
        dia = int(data[0:2])
        mes = int(data[2:4])
        ano = int(data[4:])

        if mes < 0 or mes > 12:
            #Mês inválido
            return False

        #Checa o número de dias de cada mês
        #Achei mais interessante que fazer com uma lista
        if mes <= 7:
            dias = 30       #2, 4 e 6
            if mes % 2:
                dias = 31   #1, 3, 5 e 7
        elif mes > 7:
            dias = 31       #8, 10, 12
            if mes % 2:
                dias = 30   #9 e 11

        #Checa se é bissexto, mesmo que não precise
        if mes == 2:
            dias = 28
        if not ano % 4 and (ano % 100 or not ano % 400):
            dias = 29

        #Checagem dos dias no mês
        if dia > 0 and dia <= dias:
            return True

    return False


def projetoValidacao(proj):
    return projcontValidacao("+", proj)

def contextoValidacao(cont):
    return projcontValidacao("@", cont)

def projcontValidacao(simbolo, texto):
    if len(texto) > 1 and texto.startswith(simbolo):
        return True
    return False


########################UTILIDADES########################

def printCores(texto, prio):

    #São 4 cores específicas pras prioridades mais importantes
    #E um cinza mais escuro pra última prioridade
    switchCores = {"(A)":       "\033[;1m\033[1;31m",
                   "(B)":       "\033[1;32m",
                   "(C)":       "\033[1;33m",
                   "(D)":       "\033[1;36m",
                   "(Z)":       "\033[1;30m",
                   "BOLD":      "\033[;1m",
                   "REVERSE":   "\033[;7m",
                   "RESET":     "\033[0;0m"}

    cor = switchCores.get(prio.upper(), "")
    if not cor and prio:
        cor = switchCores.get("BOLD")

    print(cor + texto + switchCores["RESET"])


def soDigitos(numero):

    if type(numero) != str :
        return False
    for x in numero :
        if x < "0" or x > "9" :
            return False
    return True


#Devolve todas as partes separadas e nas posições certas
def soltarItem(item):

    desc = item[0].strip()
    extras = item[1]
    data = hora = prio = cont = proj = ""

    if extras:
        if extras[0]:
            data = extras[0]
        if extras[1]:
            hora = extras[1]
        if extras[2]:
            prio = extras[2].upper()
        if extras[3]:
            cont = extras[3]
        if extras[4]:
            proj = extras[4]

    return [data, hora, prio, desc, cont, proj]


#Devolve as partes prontas para serem listadas
def prepararItem(item):

    data, hora, prio, desc, cont, proj = soltarItem(item)

    if  len(desc) > 1:
        desc = "[" + desc[0].upper() + desc[1:] + "]"
    else:
        desc = "[" + desc.upper() + "]"
    if data:
        data = data[0:2] + "/" + data[2:4] + "/" + data[4:]
    if hora:
        hora = hora[0:2] + "h" + hora[2:] + "m"

    return [data, hora, prio, desc, cont, proj]


#Devolve as partes como tupla novamente
def desprepararItem(item):

    data, hora, prio, desc, cont, proj = item[0:6]
    if data:
        data = data[0:2] + data[3:5] + data[6:]
    if hora:
        hora = hora[0:2] + hora [3:5]
    desc = desc[1:-1]

    return (desc, [data, hora, prio, cont, proj])


#É basicamente uma forma de printar a lista
def mostrarItem(item, mostrarFormato = False):

    formato = ["Data      ", "Hora  ", "(P)", "[Desc]", "@Cont", "+Proj"]
    texto = textoFormato = ""
    for i in range(len(item)):
        if item[i]:
            espacosT = espacosF = " "
            #Essa parte é só pra deixar organizadinho na hora da confirmação
            if mostrarFormato:
                if len(item[i]) >= len(formato[i]):
                    espacosF = " " * (len(item[i]) - len(formato[i]) + 1)
                else:
                    espacosT = " " * (len(formato[i]) - len(item[i])+ 1)
                textoFormato += formato[i] + espacosF
            texto += item[i] + espacosT
    print(textoFormato.strip())
    if mostrarFormato:
        print(texto.strip())
    else:
        return texto.strip()


#Confirmação básica
def simNao():
    Sims = ["S", "SI", "SIM", "Y", "YE", "YES", "1"]
    print("(S)im ou (N)Ão: ")
    while True:
        escolha = input("").upper()
        if escolha in Sims:
            return True
        elif escolha.strip():
            return False


#Remove todas partes vazias do arquivo
def limparLista(lista):

    listaFinal = []
    while lista:
        item = lista.pop(0).strip()
        if item:
            item = item.strip("\n")
            listaFinal.append(item)
    return listaFinal


########################EXECUÇÃO########################

arquivo_TODO = "todo.txt"
arquivo_DONE = "done.txt"
arquivo_BKUP = "todo.bak"

processarComandos(sys.argv)

