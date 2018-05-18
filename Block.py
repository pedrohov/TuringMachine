# Simulador de Maquina de Turing ver 1.0.
# Desenvolvido como trabalho pratico para a disciplina de Teoria da Computacao.
# Pedro Henrique Oliveira Veloso - 0002346, IFMG, 2018.

from Transition import Transition;

class Block(object):

    def __init__(self, blockName):
        self.name         = blockName;
        self.initial      = None;
        self.inAlphabet   = ['*', '_'];
        self.outAlphabet  = [];
        self.states       = [];
        self.finals       = [];
        self.transitions  = [];

        self.blockTrans   = [];

        self.currentState = None;

        return;

    def step(self, tape, stack):

        # Diretiva especial para parar a execucao:
        if(self.currentState == "pare"):
            self.currentState = self.initial;
            return "pare";

        # Diretiva especial para retornar a execucao ao bloco anterior:
        if(self.currentState == "retorne"):
            self.currentState = self.initial;
            return None;

        read = tape.currentChar;

        for transition in self.transitions:
            # Procura por transicao valida:
            if((transition.source == self.currentState) and
              ((transition.read == read) or (transition.read == "*"))):
                # Muda o estado atual:
                # * = Nao muda de estado:
                nextState = transition.target;
                if(nextState != "*"):
                    self.currentState = transition.target;

                # Escreve o caractere na fita:
                tape.write(transition.write);

                # Move o cabecote:
                tape.move(transition.mov);

                # Se a transicao possuir exclamacao para a execucao:
                if(transition.pause):
                    return "pause";

                # Retorna o bloco atual (permanece no bloco):
                return self;

        # Olha se o estado em que esta leva a um novo bloco:
        for transition in self.blockTrans:
            if(transition.initialState == self.currentState):
                # Empilha o bloco chamador e o estado de retorno:
                stack.append((self, transition.returnState));
                return transition.targetBlock;

        # Nao houve nenhuma transicao valida:
        return None;

    def addState(self, state):
        """ Adiciona um novo estado a maquina. """
        if(state not in self.states):
            self.states.append(state);

    def addSymbolIn(self, symbol):
        """ Adiciona um novo estado a maquina. """
        if(symbol not in self.inAlphabet):
            self.inAlphabet.append(symbol);

    def addSymbolOut(self, symbol):
        """ Adiciona um novo estado a maquina. """
        if(symbol not in self.outAlphabet):
            self.outAlphabet.append(symbol);

    def addTransition(self, transition):
        if(self.hasTransition(transition) == False):
            self.transitions.append(transition);
        return;

    def hasTransition(self, transition):
        for t in self.transitions:
            if(t.equals(transition)):
                return True;
        return False;

    def addBlockTransition(self, transition):
        if(self.hasBlockTransition(transition) == False):
            self.blockTrans.append(transition);
        return;

    def hasBlockTransition(self, transition):
        for t in self.blockTrans:
            if(t.equals(transition)):
                return True;
        return False;

    def __str__(self):
        result = "Block: " + self.name + "\nInitial: " + self.initial;
        if(len(self.transitions) == 0):
            result += "\nTransitions: { }";
        else:
            result += "\nTransitions:\n{\n";
            for i in range(0, len(self.transitions) - 1):
                transition = self.transitions[i];
                result += "\t" + transition.__str__() + "\n";
            result += "\t" + self.transitions[len(self.transitions) - 1].__str__() + "\n}";

        if(len(self.blockTrans) == 0):
            result += "\nBlock Transitions: { }";
        else:
            result += "\nBlock Transitions:\n{\n";
            for i in range(0, len(self.blockTrans) - 1):
                transition = self.blockTrans[i];
                result += "\t" + transition.__str__() + "\n";
            result += "\t" + self.blockTrans[len(self.blockTrans) - 1].__str__() + "\n}";
        return result;