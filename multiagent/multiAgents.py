# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import time
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        minFdist=9999
        minGdist=9999

        for g in newGhostStates:
        	minGdist = min(minGdist, manhattanDistance(newPos,g.getPosition()))

        val = 0
        if minGdist < 2:
        	val = val -9999

        for f in newFood.asList():
        	minFdist = min(minFdist, manhattanDistance(newPos,f))

        numF = len(newFood.asList())
        if numF < 1:
        	val = val +9999

        val = val - minFdist - (newFood.width * newFood.height)*numF

        return val

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()

        def maxVal(state,depth,agentIndex):
        	if agentIndex == 0:		#when every one has taken equal turn
        		depth=depth-1	

        	if depth == 0:
        		return self.evaluationFunction(state)

        	actions = state.getLegalActions(agentIndex)
        	if 'Stop' in actions: actions.remove('Stop')

        	if len(actions) == 0:	#terminal State
        		return self.evaluationFunction(state)

        	v = -999999
        	for actn in actions:
        		v = max(v,minVal(state.generateSuccessor(agentIndex, actn),
        							depth,
        							(agentIndex+1)%numAgents))

        	return v

        def minVal(state,depth,agentIndex):
        	if agentIndex == 0:		#when every one has taken equal turn
        		depth=depth-1	

        	if depth == 0:
        		return self.evaluationFunction(state)

        	actions = state.getLegalActions(agentIndex)
        	if 'Stop' in actions: actions.remove('Stop')

        	if len(actions) == 0:	#terminal State
        		return self.evaluationFunction(state)

        	v = 999999
        	for actn in actions:
        		if agentIndex == numAgents-1:
        			v = min(v,maxVal(state.generateSuccessor(agentIndex, actn),
        							depth,
        							(agentIndex+1)%numAgents))
        		else:
        			v = min(v,minVal(state.generateSuccessor(agentIndex, actn),
        							depth,
        							(agentIndex+1)%numAgents))

        	return v

        # print gameState.getLegalActions(1)
        def minimax(state,depth,agentIndex):
        	actions = state.getLegalActions(agentIndex)
        	if 'Stop' in actions: actions.remove('Stop')
        	if len(actions) == 0:	#terminal State
        		return self.evaluationFunction(state)

        	if agentIndex == 0: 	# Pacman
        		bestActn=actions[0]
        		v = -999999
        		print len(actions),"==============================="
        		for actn in actions:
        			t = minVal(state.generateSuccessor(agentIndex, actn),depth,(agentIndex+1)%numAgents)
        			print actn,t
        			if v < t: 		# Max agent
        				v=t
        				bestActn = actn	
        		print bestActn
        		return bestActn
        	
        	else :					# Ghost
        		print "error"

    	return minimax(gameState,self.depth,0)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()

        def maxVal(state,depth,agentIndex,alpha,beta):
        	if agentIndex == 0:		#when every one has taken equal turn
        		depth=depth-1	

        	if depth == 0:
        		return self.evaluationFunction(state)

        	actions = state.getLegalActions(agentIndex)
        	if 'Stop' in actions: actions.remove('Stop')

        	if len(actions) == 0:	#terminal State
        		return self.evaluationFunction(state)

        	v = -999999
        	for actn in actions:
        		v = max(v,minVal(state.generateSuccessor(agentIndex, actn),
        							depth,
        							(agentIndex+1)%numAgents,
        							alpha,beta))
        		
        		alpha = max(alpha,v)
        		if v > beta:
        			return v

        	return v

        def minVal(state,depth,agentIndex,alpha,beta):
        	if agentIndex == 0:		#when every one has taken equal turn
        		depth=depth-1	

        	if depth == 0:
        		return self.evaluationFunction(state)

        	actions = state.getLegalActions(agentIndex)
        	if 'Stop' in actions: actions.remove('Stop')

        	if len(actions) == 0:	#terminal State
        		return self.evaluationFunction(state)

        	v = 999999
        	for actn in actions:
        		if agentIndex == numAgents-1:
        			v = min(v,maxVal(state.generateSuccessor(agentIndex, actn),
        							depth,
        							(agentIndex+1)%numAgents,
        							alpha,beta))
        		else:
        			v = min(v,minVal(state.generateSuccessor(agentIndex, actn),
        							depth,
        							(agentIndex+1)%numAgents,
        							alpha,beta))

        		beta = min(beta,v)
        		if v < alpha:
        			return v

        	return v

        # print gameState.getLegalActions(1)
        def minimax(state,depth,agentIndex,alpha,beta):
        	actions = state.getLegalActions(agentIndex)
        	if 'Stop' in actions: actions.remove('Stop')
        	if len(actions) == 0:	#terminal State
        		return self.evaluationFunction(state)

        	if agentIndex == 0: 	# Pacman
        		bestActn=actions[0]
        		v = -999999
        		for actn in actions:
        			t = minVal(state.generateSuccessor(agentIndex, actn),
        												depth,
        												(agentIndex+1)%numAgents,
        												alpha,beta)
        			if v < t: 		# Max agent
        				v=t
        				bestActn = actn

        			alpha = max(alpha,v)
        			if v >= beta:
        				return bestActn
        		# print bestActn
        		return bestActn
        	
        	else :					# Ghost
        		print "error"

    	return minimax(gameState,self.depth,0,-999999,999999)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition()
    Foods = currentGameState.getFood()
    GhostPos = currentGameState.getGhostPositions()
    ScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
    Capsules = currentGameState.getCapsules()
    numF = len(Foods.asList())
    numC = len(Capsules)

    fdist = []
    minGdist = 9999
    minCdist = 9999

    for gpos in GhostPos:
    	minGdist = min(minGdist, manhattanDistance(Pos,gpos))

    val = 0
    # print ScaredTimes
    if minGdist < 2:
    	val = val -9999

    for f in Foods.asList():
    	fdist.append(manhattanDistance(Pos,f))
    fdist.sort()

    fscore=0
    for i in range(0,min(10,len(fdist))):
    	fscore += (5.0/(i+1))*fdist[i]

    for c in Capsules:
    	minCdist = min(minCdist, manhattanDistance(Pos,c))

    # if minCdist == 1:
    # 	val = val +10

    if numF < 1:
    	val = val +9999

    val = val + 2*max(4,minGdist) -3.5*numC - 50*numF +10/numF - fscore

    # print currentGameState
    print val 
    return val 

# Abbreviation
better = betterEvaluationFunction

