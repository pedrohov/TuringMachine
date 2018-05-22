# Simulador de Maquina de Turing ver 1.0.
# Desenvolvido como trabalho pratico para a disciplina de Teoria da Computacao.
# Python v.3.6.4
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
        tapeRes = "";
        stringLength = len(self.tapeInput);

        if(self.index >= 0):
            selectedChar = self.tapeInput[self.index:(self.index + 1)];
            if(selectedChar == ""):
                selectedChar = "_";
            tapeRes = self.tapeInput[:self.index] + self.delim[0] + selectedChar;
            tapeRes += self.delim[1] + self.tapeInput[(self.index + 1):];

            if(selectedChar == "_"):
                stringLength += 1;

            qtd = 20 - self.index;
            # Precisa cortar o inicio da string:
            if(qtd < 0):
                tapeRes = tapeRes[(self.index - 20):];
            else:
                for i in range(0, qtd):
                    tapeRes = '_' + tapeRes;

            qtd = 20 - stringLength + self.index;

            # Precisa cortar o fim da string:
            if(qtd < 0):
                tapeRes = tapeRes[:(-(stringLength - 20 - self.index))];

            # Precisa adicionar '_':
            else:
                for i in range(0, qtd):
                    tapeRes = tapeRes + '_';
        else:
            # Index menor que zero:
            tapeRes = self.tapeInput;
            qtd = 20 + self.index + 1;
            for i in range(0, qtd):
                tapeRes = '_' + tapeRes;

            index = 0;

            tapeRes = tapeRes[:qtd] + self.delim[0] + '_';
            tapeRes += self.delim[1] + self.tapeInput;

            qtd = 20 - stringLength + self.index;

            # Precisa cortar o fim da string:
            if(qtd < 0):
                tapeRes = tapeRes[:(-(stringLength - 20 - self.index))];

            # Precisa adicionar '_':
            else:
                for i in range(0, qtd):
                    tapeRes = tapeRes + '_';

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