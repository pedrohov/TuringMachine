# Simulador de Maquina de Turing ver 1.0.
# Desenvolvido como trabalho pratico para a disciplina de Teoria da Computacao.
# Pedro Henrique Oliveira Veloso - 0002346, IFMG, 2018.

class Tape(object):

    MOVE_LEFT  = 'e';
    MOVE_RIGHT = 'd';
    STAY       = 'i';

    def __init__(self, delim):
        self.tapeInput = "";
        self.index     = -1;
        self.delim     = delim;
        return;

    def move(self, direction):
        if(direction == Tape.MOVE_LEFT):
            self.index -= 1;
        elif(direction == Tape.MOVE_RIGHT):
            self.index += 1;
        return;

    def show(self, block, state):
        """ Imprime o cabecote. """
        if(state == "retorne"):
            state = "rtrn";

        result = block + "." + state + ": ";
        tapeRes = self.tapeInput[:self.index] + self.delim[0] + self.tapeInput[self.index:(self.index + 1)];
        tapeRes += self.delim[1] + self.tapeInput[(self.index + 1):];

        if(self.index < 0):
            tapeRes = self.tapeInput;

        result += tapeRes;
        
        print(result);
        return;

    def write(self, symbol):
        """ Escreve um caractere no cabecote. """
        # Nao altera se o simbolo for "*":
        if(symbol == "*"):
            return;

        tapeRes = self.tapeInput[:self.index] + symbol + self.tapeInput[(self.index+1):];
        self.tapeInput = tapeRes;
        return;

    @property
    def currentChar(self):
        if((self.index < 0) or (self.index >= len(self.tapeInput))):
            return '_';

        return self.tapeInput[self.index];

    def __str__(self):
        pass;