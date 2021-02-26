import random

def Similarity(user_answer):
	print("eval=",user_answer)
	if user_answer==None or user_answer == 'start':
		sim = -1
	else:
		sim = random.uniform(0.0,1.1)
	# print(sim)
	return(sim)
		

if __name__=="__main__":
	Similarity("user_answer")
