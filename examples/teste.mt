; Detector de palindrome:
	bloco main 01
		01 a -- A i 10
		01 b -- B i 20
		10 moveFim 11
		20 moveFim 21

		; leu a
		11 iniEsq 12
		12 a -- A i 30
		12 b -- * i 70
		12 _ -- * i 60