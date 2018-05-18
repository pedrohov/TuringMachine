# Simulador de Maquina de Turing ver 1.0.
# Desenvolvido como trabalho prático para a disciplina de Teoria da Computacao.
# Pedro Henrique Oliveira Veloso - 0002346, IFMG, 2018.

import sys;
import TuringMachine;
import IOParser;

if (__name__ == "__main__"):
    # Header:
    print("Simulador de Maquina de Turing ver 1.0.");
    print("Desenvolvido como trabalho pratico para a disciplina de Teoria da Computacao.");
    print("Pedro Henrique Oliveira Veloso, IFMG, 2018.\n");

    # Interpreta argumentos do programa:
    parser = IOParser.Parser(sys.argv);
    config = parser.parseProgramInput();
    if (config == None):
        sys.exit();

    # Cria e inicializa a maquina de turing
    # com os argumentos fornecidos:
    mt = TuringMachine.TM(config);
    parser.parseInputFile(mt);

    # Input:
    tapeInput = input("Palavra inicial: ");
    erro = mt.setTapeInput(tapeInput);
    if (erro):
        sys.exit();
    
    # Executa a maquina:
    mt.execute();