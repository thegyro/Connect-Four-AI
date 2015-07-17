#Contains the classes for implementing the adversarial search algorithms
#The ones implemented are MiniMax search and Alpha Beta pruning.
#FUTURE WORK - Couple both into one class to avoid redundant code.
#
#Author - Srinath Rajagopalan
#email  - srinath132@gmail.com

class MinimaxAgent:
	def __init__(self, evalFn, agent, adversary, depth=2):
		self.evaluationFunction = evalFn
		self.depth = depth
		self.agent = agent
		self.adversary = adversary

	def getAction(self, gameState):
		return self.computeMinimaxAction(gameState)

	def computeMinimaxAction(self, gameState):
		nextActions = gameState.getLegalActions()
		successorStates  = [(action,gameState.generateSuccessor(self.agent, action)) for action in nextActions]

		opScore = -999999
		opAction = None

		for next in successorStates:
			nextAction = next[0]
			nextState = next[1]

			nextValue = self.value(nextState, self.adversary,0)

			optimal = [(opAction, opScore), (nextAction, nextValue)]
			opAction, opScore = max(optimal, key = lambda x: x[1])
			#print opAction, opScore

		return opAction

	def value(self, gameState, agent, depth):
		if depth == self.depth or gameState.isGoal(self.adversary) or gameState.isGoal(self.agent):
			return self.evaluationFunction(gameState, self.agent, self.adversary)

		if agent == self.agent:
			return self.maxValue(gameState,depth)

		else:
			return self.minValue(gameState,depth)


	def maxValue(self, gameState, depth):
		nextActions = gameState.getLegalActions()
		successorStates = [gameState.generateSuccessor(self.agent, action) for action in nextActions]

		v = -999999
		for nextState in successorStates:
			v = max(v, self.value(nextState, self.adversary, depth))

		return v


	def minValue(self, gameState, depth):
		nextActions = gameState.getLegalActions()
		successorStates = [gameState.generateSuccessor(self.adversary, action) for action in nextActions]

		v = +999999
		for nextState in successorStates:
			v = min(v, self.value(nextState, self.agent, depth+1))

		return v



class AlphaBetaAgent:
	def __init__(self, evalFn, agent, adversary, depth=2):
		self.evaluationFunction = evalFn
		self.depth = depth
		self.agent = agent
		self.adversary = adversary

	def getAction(self, gameState):
		alpha = -999999
		beta  = +999999
		return self.computeAlphaBetaAction(gameState, alpha, beta)

	def computeAlphaBetaAction(self, gameState, alpha, beta):
		nextActions = gameState.getLegalActions()
		successorStates  = [(action,gameState.generateSuccessor(self.agent, action)) for action in nextActions]

		opScore = -999999
		opAction = None

		for next in successorStates:
			nextAction = next[0]
			nextState = next[1]

			nextValue = self.value(nextState, self.adversary, alpha, beta, 0)

			optimal = [(opAction, opScore), (nextAction, nextValue)]
			opAction, opScore = max(optimal, key = lambda x: x[1])
			alpha = max(alpha, opScore)

		return opAction

	def value(self, gameState, agent, alpha, beta, depth):
		if depth == self.depth or gameState.isGoal(self.adversary) or gameState.isGoal(self.agent):
			return self.evaluationFunction(gameState, self.agent, self.adversary)

		if agent == self.agent:
			return self.maxValue(gameState, alpha, beta, depth)

		else:
			return self.minValue(gameState, alpha, beta, depth)


	def maxValue(self, gameState, alpha, beta, depth):
		nextActions = gameState.getLegalActions()
		successorStates = [gameState.generateSuccessor(self.agent, action) for action in nextActions]

		v = -999999
		for nextState in successorStates:
			v = max(v, self.value(nextState, self.adversary, alpha, beta, depth))

			if v >= beta:
				return v

			alpha = max(alpha, v)

		return v


	def minValue(self, gameState, alpha, beta, depth):
		nextActions = gameState.getLegalActions()
		successorStates = [gameState.generateSuccessor(self.adversary, action) for action in nextActions]

		v = +999999
		for nextState in successorStates:
			v = min(v, self.value(nextState, self.agent, alpha, beta, depth+1))

			if v <= alpha:
				return v

			beta = min(beta, v)

		return v