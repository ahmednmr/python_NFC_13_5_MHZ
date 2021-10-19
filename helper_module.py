

def helper_2s_complement(num):
	_2Complement=~num
	_2Complement+=1
	_2Complement&=0x000000FF
	return _2Complement