# Simulador de Maquina de Turing ver 1.0.
# Desenvolvido como trabalho pratico para a disciplina de Teoria da Computacao.
# Pedro Henrique Oliveira Veloso - 0002346, IFMG, 2018.

class Transition(object):

	def __init__(self, source, target, read, write, mov, pause):
		self.source = source;
		self.target = target;
		self.read   = read;
		self.write  = write;
		self.mov    = mov;
		self.pause  = pause;
		return;

	def equals(self, transition):
		if((self.source == transition.source)  and
			(self.target == transition.target) and
			(self.read == transition.read)     and
			(self.write == transition.write)   and
			(self.mov == transition.mov)):
			return True;

		return False;

	def __str__(self):
		result = "{ Source: " + self.source + ", target: " + self.target;
		result += ", " + self.read + "/" + self.write + ", mov: " + self.mov + " }";
		return result;