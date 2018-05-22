# Simulador de Maquina de Turing ver 1.0.
# Desenvolvido como trabalho pratico para a disciplina de Teoria da Computacao.
# Python v.3.6.4
# Pedro Henrique Oliveira Veloso - 0002346, IFMG, 2018.

from pathlib import Path;
from TuringMachine import TM;

class Parser:

    def __init__(self, data):
        self.data      = data;
        self.inputFile = None;
        self.mt        = None;

    def parseProgramInput(self):
        """
            Recebe a linha de comando da execucao do programa,
            retorna uma array [modo de execucao, n.o de steps, delimitador],
            ou retorna None caso a linha esteja mal formatada.
        """
        # Precisa de ao menos duas entradas,
        # nome do programa e arquivo a ser simulado:
        if(len(self.data) < 2):
            print("\n> Argumentos insuficientes.");
            return None;

        # Checa se o arquivo informado existe:
        self.inputFile = self.data[len(self.data) - 1];
        filepath = Path(self.inputFile);
        if(filepath.is_file() == False):
            print("\n> Arquivo de entrada invalido.");
            return None;

        # Cria a array de configuracao:
        config = [TM.MODE_RESUME, TM.MAX_STEPS, TM.STD_DELIM];

        # Checa se o formato dos
        # demais argumentos e valido:
        foundHead  = False;
        foundSteps = False;
        for i in range(1, len(self.data) - 1):
            arg = self.data[i];
            
            if(((arg == "-resume") or (arg == "-r")) and (foundHead == False) and (foundSteps == False)):
                config[0] = TM.MODE_RESUME;
            elif(((arg == "-verbose") or (arg == "-v")) and (foundHead == False) and (foundSteps == False)):
                config[0] = TM.MODE_VERBOSE;
            elif(((arg == "-head") or (arg == "-h"))  and (foundHead == False) and (foundSteps == False)):
                foundHead = True;
            elif(((arg == "-step") or (arg == "-s"))  and (foundHead == False) and (foundSteps == False)):
                foundSteps = True;
            elif (foundSteps == True):
                config[1] = int(arg);
                foundSteps = False;
            elif (foundHead == True):
                delim = self.checkHead(arg);
                if(delim == None):
                    print("\nDelimitador " + arg + " invalido.");
                    return None;

                config[2] = delim;
                foundHead = False;

        return config;

    def checkHead(self, head):
        # Delimitador deve possuir exatamente dois caracteres:
        if(len(head) != 2):
            return None;

        return [head[0], head[1]];

    def parseInputFile(self, machine):
        """
            Le o arquivo de entrada e o interpreta,
            criando os blocos, estados, transicoes
            e o alfabeto que define a Maquina de Turing.
        """

        currentBlock = "";

        try:
            with open(self.inputFile) as file:
                # Itera sobre cada linha do arquivo:
                for fLine in file:

                    # Divide a linha em um vetor:
                    line = fLine.split();

                    # Comentario ou linha vazia:
                    if((len(line) == 0) or (line[0] == ';')):
                        continue;
                    # Inicio de um novo bloco:
                    elif(line[0] == 'bloco'):
                        currentBlock = self.addBlock(machine, line);
                    # Fim do bloco:
                    elif(line[0] == 'fim'):
                        continue;
                    # Transicao:
                    else:
                        self.addTransition(machine, line, currentBlock);

        except IOError:
            print("Erro ao abrir arquivo.\n");

    def addBlock(self, machine, line):
        name    = self.formatBlockName(line[1]);
        initial = self.formatState(line[2]);
        machine.addBlock(name, initial);
        return name;

    def addTransition(self, machine, line, block):
        """ Adiciona uma nova transicao a maquina. """

        # Transicao a ser adicionada
        # esta dentro do bloco atual
        if(line[2] == "--"):
            source = self.formatState(line[0]);
            read   = line[1];
            write  = line[3];
            mov    = line[4];
            target = self.formatState(line[5]);

            pausa = False;
            if(len(line) > 6):
                stopSign = line[6];
                if(stopSign == "!"):
                    pausa = True;


            machine.addTransition(source, target, read, write, mov, block, pausa);
        else:
            initial = self.formatState(line[0]);
            target  = self.formatBlockName(line[1]);
            returnS = self.formatState(line[2]);
            machine.addBlockTransition(initial, returnS, block, target);
        return;

    def formatState(self, state):

        if(state == "pare"):
            return "pare";
        elif(state == "retorne"):
            return "retorne";

        try:
            intState = int(state);
            strState = str(intState);
            for i in range(0, (4 - len(strState))):
                strState = "0" + strState;

            return strState;
        except ValueError:
            print("> (" + state + "). Nome de estado invalido. Estados devem ser numeros inteiros.");

        return;

    def formatBlockName(self, name):

        for i in range(0, (16 - len(name))):
            name = "." + name;

        return name;

    def prompt(self, iniConfig):
        print("\nAperte enter para continuar ou configure a maquina.");
        print("-v ou -verbose\n\tExecuta a maquina de turing e exibe cada passo." +
            "\n-r ou -resume\n\tExecuta a maquina de turing e exibe apenas o resultado." +
            "\n-s # ou -step #\n\tInforma o numero maximo de passos possivel." +
            "\n-h '[]' ou -head '[]'\n\tAltera o caractere delimitador do cabecote da fita.");
        line = input("Config: ");
        print("");
        aLine = line.split();
        config = [iniConfig[0], iniConfig[1], iniConfig[2]];

        foundSteps = False;
        foundHead  = False;
        for i in range(0, len(aLine)):
            arg = aLine[i];
            
            if(((arg == "-resume") or (arg == "-r")) and (foundHead == False) and (foundSteps == False)):
                config[0] = TM.MODE_RESUME;
            elif(((arg == "-verbose") or (arg == "-v")) and (foundHead == False) and (foundSteps == False)):
                config[0] = TM.MODE_VERBOSE;
            elif(((arg == "-head") or (arg == "-h"))  and (foundHead == False) and (foundSteps == False)):
                foundHead = True;
            elif(((arg == "-step") or (arg == "-s"))  and (foundHead == False) and (foundSteps == False)):
                foundSteps = True;
            elif (foundSteps == True):
                config[1] = int(arg);
                foundSteps = False;
            elif (foundHead == True):
                delim = [arg[1], arg[2]];
                config[2] = delim;
                foundHead = False;
        
        return config;