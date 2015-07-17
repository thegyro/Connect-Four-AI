#This is the Connect Four AI driver program.
#It implements the connect four modeler and uses Minimax as its
#adversarial search algorithm for deciding the moves of the AI
#
#Authors - Tushar Nagarajan and Srinath Rajagopalan
#email - tushar.nagarajan@gmail.com and srinath132@gmail.com


import adversary
import copy
import time, sys

class ConnectFourState():

	'''
	basic methods for constructing and proper hashing of State objects
	'''
	def __init__(self, shape):
		self.shape=shape
		self.board=[['.']*shape[1] for i in range(shape[0])]
		
	def __eq__(self, other):
		return tuple(self.board)==tuple(other.board)
		
	def __hash__(self):
		return hash(tuple(map(tuple,self.board)))
	
	def copy(self):
		new_state = ConnectFourState(self.shape)
		new_state.board=copy.deepcopy(self.board)
		return new_state
	
	
	'''
	returns a list of actions that can be taken from the current state
	actions are integers representing the column where a coin can be dropped
	'''
	def getLegalActions(self):
	
		if self.isGoal('X') or self.isGoal('O'):
			return []
	
		top=self.board[0]
		legal_actions=[i for i in range(len(top)) if top[i]=='.']
		return legal_actions
	
	''' 
	returns a State object that is obtained by the agent (parameter)
	performing an action (parameter) on the current state
	'''	
	def generateSuccessor(self, agent, action):
	
		row=0
		while(row<self.shape[0] and self.board[row][action]!= 'O' and self.board[row][action] != 'X'):
			row+=1
		
		new_state=self.copy()
		new_state.board[row-1][action]=agent
		return new_state

	'''
	returns True/False if the agent(parameter) has won the game
	by checking all rows/columns/diagonals for a sequence of >=4
	'''
	def isGoal(self, agent):
		
		seq=agent*4
		
		for row in self.board:
			if seq in ''.join(row):
				return True
		
		for col in map(list, zip(*self.board)):
			if seq in ''.join(col):
				return True
			
		diags=[]
		pos_right=[(0,j) for j in range(self.shape[1]-4+1)]+[(i,0) for i in range(1,self.shape[0]-4+1)]
		pos_left=[(0,j) for j in range(4-1, self.shape[1])]+[(i,self.shape[1]-1) for i in range(1,self.shape[0]-4+1)]

		for each in pos_right:
			d=''
			start=list(each)
			while(1):				
				if start[0]>=self.shape[0] or start[1]>=self.shape[1]:
					break
				d+=self.board[start[0]][start[1]]
				start[0]+=1
				start[1]+=1
			if seq in d:
				return True

		for each in pos_left:	
			d=''
			start=list(each)
			while(1):
				if start[1]<0 or start[0]>=self.shape[0] or start[1]>=self.shape[1]:
					break
				d+=self.board[start[0]][start[1]]
				start[0]+=1
				start[1]-=1
			
			if seq in d:
				return True
		
		return False
		
	'''
	Print's the current state's board in a nice pretty way
	'''
	def printBoard(self):
		print '-'*self.shape[1]*2
		for row in self.board:
			print ' '.join(row)
		print '-'*self.shape[1]*2


def evaluationFunction(gameState, agent, adversary):
	"""
		Some fancy heuristic tushar suggested me to try so that my AI doesn't
		suck at shallow depths.
	"""
	if gameState.isGoal(agent):
		return 10000
	if gameState.isGoal(adversary):
		return -10000
	
	
	def getSeqs():
	
		seqs=[]
		seqs+=[''.join(row) for row in gameState.board]
		seqs+=[''.join(col) for col in map(list, zip(*gameState.board))]
	
		#check diagonals
		pos_right=[(0,j) for j in range(gameState.shape[1]-4+1)]+[(i,0) for i in range(1,gameState.shape[0]-4+1)]
		pos_left=[(0,j) for j in range(4-1, gameState.shape[1])]+[(i,gameState.shape[1]-1) for i in range(1,gameState.shape[0]-4+1)]

		for each in pos_right:
			d=''
			start=list(each)
			while(1):				
				if start[0]>=gameState.shape[0] or start[1]>=gameState.shape[1]:
					break
				d+=gameState.board[start[0]][start[1]]
				start[0]+=1
				start[1]+=1
			seqs.append(d)

		for each in pos_left:	
			d=''
			start=list(each)
			while(1):
				if start[1]<0 or start[0]>=gameState.shape[0] or start[1]>=gameState.shape[1]:
					break
				d+=gameState.board[start[0]][start[1]]
				start[0]+=1
				start[1]-=1
			seqs.append(d)
		
		return seqs
	
	score=0
	seqs=getSeqs()

	score+=5*sum([1 for each_seq in seqs if 'O.OO' in each_seq])
	score+=5*sum([1 for each_seq in seqs if 'OO.O' in each_seq])
	score-=3*sum([1 for each_seq in seqs if 'X.XX' in each_seq])
	score+=3*sum([1 for each_seq in seqs if 'XX.X' in each_seq])
	
	score+=5*sum([1 for each_seq in seqs if 'OOO.' in each_seq])
	score+=5*sum([1 for each_seq in seqs if '.OOO' in each_seq])
	score-=3*sum([1 for each_seq in seqs if 'XXX.' in each_seq])
	score-=3*sum([1 for each_seq in seqs if '.XXX' in each_seq])
	
	return score


def main():
	shape = (6, 7)

	startState = ConnectFourState(shape)

	print "Welcome to the Connect Four AI program."
	print "Decide what agent you want to play against: "
	print "Press 1 for a Minimax agent and 2 for an AlphaBeta agent: ",

	try:
		choice = int(raw_input().strip())
	except ValueError as e:
		print "Didn't press an integer dammit.Bye."
		sys.exit(0)

	print "Decide the depth you want the AI to go."
	print "Beware! If you choose a depth > 3, I pray you have a long life with infinite patience."
	print "Enter the depth: ",
	d = int(raw_input().strip())

	if choice == 1:
		aiagent = adversary.MinimaxAgent(evaluationFunction, 'O', 'X', depth=d)

	elif choice == 2:
		aiagent = adversary.AlphaBetaAgent(evaluationFunction,'O','X', depth=d)

	else:
		print "Invalid choice :-/. Bye"
		sys.exit(0)

	
	print "Press between 1 to 7 for deciding column number."
	print "Starting State: "
	startState.printBoard()

	print 

	state = startState
	while 1:
		print "AI's turn:"
		action = aiagent.getAction(state)
		time.sleep(1)
		print "AI puts in column %d \n" % (action + 1)

		nextState = state.generateSuccessor('O', action)
		nextState.printBoard()

		if nextState.isGoal('O'):
			print "AI Wins!"
			break

		userAction = int(raw_input("\nYour turn: ").strip())
		nextState = nextState.generateSuccessor('X', userAction-1)
		nextState.printBoard()

		if nextState.isGoal('X'):
			print "You win!"
			break

		print
		state = nextState
		time.sleep(2)


if __name__ == "__main__":
	main()
	sys.exit(0)


