# Simulador de Maquina de Turing ver 1.0.
# Desenvolvido como trabalho pratico para a disciplina de Teoria da Computacao.
# Pedro Henrique Oliveira Veloso - 0002346, IFMG, 2018.

from Tape import Tape;
from time import sleep;
from Block import Block;
from Transition import Transition;
from BlockTransition import BlockTransition;

class TM(object):

    # Constantes de configuracao:
    MODE_RESUME  = 0;
    MODE_VERBOSE = 1;
    MAX_STEPS    = 500;
    STD_DELIM    = ['(', ')'];

    def __init__(self, config):
        self.blocks   = [];
        self.alphabet = ['*', '_'];

        self.mode  = config[0];
        self.steps = config[1];
        self.delim = config[2];

        self.tape = Tape(self.delim);

        # Variaveis para execucao:
        self.start        = False;
        self.lastState    = None;
        self.currentBlock = None;   # Bloco a ser processado.
        self.stack        = [];     # Pilha de chamada de blocos.

        return;

    def execute(self):
        """ Executa a maquina de turing. """

        # Determina o bloco de inicio:
        if(self.currentBlock == None):
            main = self.getBlock("............main");
            # Se nao houver o bloco main, encerra a execucao:
            if(main == None):
                print("> Bloco 'main' nao especificado.");
                return;
            self.currentBlock = main;

        # Faz a execucao e mostra apenas o resultado final:
        
        for i in range(0, self.steps + 1):
            stop = self.step();
            if(stop):
                break;

            # Faz a execucao passo a passo:
            #if(self.mode == TM.MODE_VERBOSE):
            #    sleep(1);

        if(self.mode == TM.MODE_RESUME):
            self.tape.show(self.currentBlock.name, self.lastState);
        
        return;

    def step(self):
        """
            Executa um unico passo na maquina de turing.
            Retorna True se a execucao for interrompida.
        """

        # Exibe o inicio do cabecote:
        if((self.tape.index == -1) and (self.start == False)):
            self.tape.move(Tape.MOVE_RIGHT);
            if(self.mode == TM.MODE_VERBOSE):
                self.tape.show(self.currentBlock.name, self.currentBlock.currentState);
            self.start = True;
            return False;

        # Mostra o cabecote:
        if(self.mode == TM.MODE_VERBOSE):
            self.tape.show(self.currentBlock.name, self.currentBlock.currentState);

        # Executa a transicao no bloco:
        newBlock = self.currentBlock.step(self.tape, self.stack);

        # Determina o novo bloco:
        if(newBlock == None):
            # Se a transicao nao levou a bloco nenhum
            # verifica se ha algum bloco para retornar:
            if(len(self.stack) == 0):
                # Encerra a execucao:
                print("> Nao existem mais transicoes possiveis.");
                return True;
            else:
                # Deve retornar ao bloco que o chamou no estado especificado:
                (block, state) = self.stack.pop();
                self.currentBlock = block;
                self.currentBlock.currentState = state;
        elif(newBlock == "pare"):
            # Diretiva especial para parar a execucao:
            return True;
        elif(newBlock == "pause"):
            # Diretiva especial para pausar a execucao:
            print("> Execucao pausada.");
            return True;
        else:
            # Atualiza o bloco atual:
            self.currentBlock = newBlock;

        self.lastState = self.currentBlock.currentState;

        return False;

    def setTapeInput(self, tapeInput):
        """
            Verifica se a entrada e valida,
            carrega a entrada para o cabecote.
        """
        for c in tapeInput:
            if(c not in self.alphabet):
                print("> A entrada possui simbolos invalidos.");
                return True;

        self.tape.tapeInput = tapeInput;
        return False;

    def addSymbol(self, symbol):
        """ Adiciona um novo estado a maquina. """
        if(symbol not in self.alphabet):
            self.alphabet.append(symbol);
        return;

    def addBlock(self, blockName, initialState):
        """ Adiciona um novo bloco a maquina. """
        # Checa se o bloco ja existe:
        if(self.hasBlock(blockName)):
            # Se existir atualiza o seu estado inicial:
            block = self.getBlock(blockName);
            block.initial = initialState;
            block.currentState = initialState;
            return;

        # Cria um novo bloco:
        newBlock = Block(blockName);
        newBlock.initial = initialState;
        newBlock.currentState = initialState;

        # Insere o bloco:
        self.blocks.append(newBlock);
        return newBlock;

    def hasBlock(self, name):
        """ Checa se existe um bloco com o nome 'name'. """
        for block in self.blocks:
            if(block.name == name):
                return True;
        return False;

    def getBlock(self, name):
        """ Busca um bloco pelo nome. """
        for block in self.blocks:
            if(block.name == name):
                return block;

        return None;

    def addBlockTransition(self, initialState, returnState, blockName, targetBlock):
        """ Adiciona uma nova transicao entre blocos para o bloco 'blockName'. """
        block = self.getBlock(blockName);
        tgtBlock = self.getBlock(targetBlock);

        # Se o bloco alvo ainda nao foi criado
        # cria um novo bloco com estado inicial qualquer:
        if(tgtBlock == None):
            tgtBlock = self.addBlock(targetBlock, "###");

        newTransition = BlockTransition(initialState, returnState, block, tgtBlock);
        block.addBlockTransition(newTransition);
        return;

    def addTransition(self, source, target, read, write, mov, blockName, pause):
        """ Adiciona uma nova transicao entre estados para o bloco 'blockName'. """
        block = self.getBlock(blockName);
        self.addSymbol(read);

        block.addState(source);
        block.addState(target);
        block.addSymbolIn(read);
        block.addSymbolOut(write);

        movement = "";
        if(mov == 'e'):
            movement = Tape.MOVE_LEFT;
        elif(mov == 'd'):
            movement = Tape.MOVE_RIGHT;
        else:
            movement = Tape.STAY;

        newTransition = Transition(source, target, read, write, movement, pause);
        block.addTransition(newTransition);
        return;

    def __str__(self):
        result = "Blocks:\n{\n";
        for i in range(0, len(self.blocks) - 1):
            block = self.blocks[i];
            result += block.__str__() + "\n";
        result += self.blocks[len(self.blocks) - 1].__str__() + "\n}";
        return result;