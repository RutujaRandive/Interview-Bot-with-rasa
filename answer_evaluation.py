import random

def Similarity(user_answer):
	print(user_answer)
	if user_answer==None:
		sim = -1
	else:
		sim = random.uniform(0.0,1.1)
	print(sim)
	return(sim)
		

if __name__=="__main__":
	Similarity("user_answer")