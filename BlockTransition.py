# Simulador de Maquina de Turing ver 1.0.
# Desenvolvido como trabalho pratico para a disciplina de Teoria da Computacao.
# Python v.3.6.4
# Pedro Henrique Oliveira Veloso - 0002346, IFMG, 2018.

class BlockTransition(object):

	def __init__(self, initialState, returnState, sourceBlock, targetBlock):
		self.initialState = initialState;
		self.returnState  = returnState;
		self.sourceBlock  = sourceBlock;
		self.targetBlock  = targetBlock;
		return;

	def equals(self, transition):
		if((self.initialState == transition.initialState)  		   and
			(self.returnState == transition.returnState) 		   and
			(self.sourceBlock.name == transition.sourceBlock.name) and
			(self.targetBlock.name == transition.targetBlock.name)):
			return True;

		return False;

	def __str__(self):
		result = "{ Source: " + self.sourceBlock.name + ", " + self.returnState;
		result += ". Target: " + self.targetBlock.name + ", " + self.initialState + " }";
		return result;