from animation import *
from enemy import *
from tower import *
import math

class Shot(object):
	def __init__(self, tower, enemy, board, cellDim):
		self.targetEnemy = enemy
		self.originTower = tower
		self.rows = len(board)
		self.cols = len(board[0])
		self.cellDim = cellDim
		self.speed = 15
		self.color = self.whichColor(self.originTower)
		self.location = self.calculateLocation(self.originTower)
		self.angle = self.calculateAngle(self.originTower, 
		self.targetEnemy)
		self.dx = -1*math.cos(self.angle)*self.speed
		self.dy = -1*math.sin(self.angle)*self.speed
		self.center = self.calculateCenter(self.location)

	def __repr__(self):
		return "Shot(%r, %r, %r)" % (self.location, self.dx, self.dy)
		
	def whichColor(self, tower):
		if isinstance(tower, OrangeTower):
			return "orange"
		elif isinstance(tower, RedTower):
			return "red"
		elif isinstance(tower, GreenTower):
			return "green"
		elif isinstance(tower, PurpleTower):
			return "#8C489F" 

	def calculateLocation(self, tower):
		startx = tower.center[0]-5
		starty = tower.center[1]-5
		endx = startx+10
		endy = starty+10
		location = [startx, starty, endx, endy]
		return location

	def calculateAngle(self, tower, enemy):
		xDistance = tower.center[0] - enemy.center[0]
		yDistance = tower.center[1] - enemy.center[1]
		angle = math.atan2(yDistance, xDistance)
		return angle

	def calculateCenter(self, location):
		centerX = (location[2] - location[0])//2.0 + location[0]	
		centerY = (location[3] - location[1])//2.0 + location[1]
		return [centerX, centerY]

	def moveShot(self):
		self.location[0] += self.dx * self.originTower.shotSpeed
		self.location[1] += self.dy * self.originTower.shotSpeed
		self.location[2] += self.dx * self.originTower.shotSpeed
		self.location[3] += self.dy * self.originTower.shotSpeed
		self.center = self.calculateCenter(self.location)

	def isOffScreen(self):
		if (self.location[0] < 0 or 
		self.location[1] < 0 or 
		self.location[2] > (self.cols+1)*self.cellDim or 
		self.location[3] > (self.rows+1)*self.cellDim):
			return True
		return False


###########################################
# Button class
###########################################

class TowerButton(object):
	def __init__(self, buttonNum, canvas, towerName, boardDim):
		self.buttonNum = buttonNum
		self.canvas = canvas
		self.towerName = towerName
		self.statsBarWidth = 200
		self.towerBarTopPad = 60
		self.iconColor = towerName[:len(towerName)-6]
		startx, endx = boardDim+10, (boardDim+
		self.statsBarWidth-10)
		starty = (self.towerBarTopPad+10+
		(buttonNum*60+10)+self.buttonNum*10) 
		endy = starty + 60
		self.location = [startx, starty, endx, endy]

	def __repr__(self):
		return "Button(%r, %r)" % (self.location, self.iconColor)

	def drawButton(self, pressed):
		if pressed == False:
			self.canvas.create_rectangle(self.location[0],
			self.location[1], self.location[2], self.location[3],
			fill="#333333", outline="white")
		elif pressed == True:
			self.canvas.create_rectangle(self.location[0],
			self.location[1], self.location[2], self.location[3],
			fill="#333333", outline=self.iconColor)	
		self.canvas.create_text(self.location[0] + 120, 
		self.location[1]+(self.location[3]-self.location[1])//2, 
		text=self.towerName, fill="white")
		self.drawTowerIcon()
		
	def drawTowerIcon(self):
		startx = self.location[0] + 20
		starty = self.location[1] + ((self.location[3]-
		self.location[1])-40)//2
		endx = startx + 40
		endy = starty + 40
		self.iconLocation = [startx, starty, endx, endy]
		self.canvas.create_oval(startx, starty, 
		endx, endy, fill=self.iconColor)	

###########################################
# Tower Array class
###########################################


class TowerArray(object):
	def __init__(self):
		self.towerList = []


###########################################
# Tower class
###########################################

class Tower(object):
	def __init__(self, row, col, board, cellDim):
		self.row = row
		self.col = col
		self.board = board
		self.cellDim = cellDim
		self.location = self.calculateLocation(
		self.row, self.col, cellDim)
		self.shotOnScreen = False
		self.radius = 70
		self.center = self.calculateCenter(self.location) 
		self.shots = []
		self.color = "black"
		self.shotSpeed = 1.4
		self.shotDamage = 0
		self.slowDown = False

	def __repr__(self):
		return "Tower(%r, %r, %r)" % (self.row, self.col, self.color)

	def calculateLocation(self, row, col, cellDim):	
		startx = col*cellDim
		starty = row*cellDim
		endx = startx + cellDim
		endy = starty + cellDim
		return [startx, starty, endx, endy]

	def calculateCenter(self, location): 
		centerX = (location[2] - location[0])//2.0 + location[0] 
		centerY = (location[3] - location[1])//2.0 + location[1]
		return [centerX, centerY]

	def fireShot(self, enemy):
		self.shotOnScreen = True
		shot = Shot(self, enemy, self.board, self.cellDim)
		self.shots.append(shot)   
			

###########################################
# Orange Tower class
###########################################

class OrangeTower(Tower):
	def __init__(self, row, col, board, cellDim):
		super(OrangeTower, self).__init__(row, col, board, cellDim)
		self.color = "orange"
		self.cost = 3
		self.shotDamage = 1
	
		
###########################################
# Red Tower class
###########################################

class RedTower(Tower):
	def __init__(self, row, col, board, cellDim):
		super(RedTower, self).__init__(row, col, board, cellDim)
		self.color = "red"
		self.cost = 10
		self.shotDamage = 2


###########################################
# Green Tower class
###########################################

class GreenTower(Tower):
	def __init__(self, row, col, board, cellDim):
		super(GreenTower, self).__init__(row, col, board, cellDim)
		self.color = "green"
		self.cost = 15
		self.shotSpeed = 1.6
		self.radius = 90
		self.shotDamage = 3


###########################################
# Purple Tower class
###########################################

class PurpleTower(Tower):
	def __init__(self, row, col, board, cellDim):
		super(PurpleTower, self).__init__(row, col, board, cellDim)
		self.color = "#8C489F"
		self.radius = 65 
		self.slowDown = True
		self.cost = 20


