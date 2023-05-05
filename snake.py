from graphics import *

import grid
import food

class Snake:
	def __init__(self, grid: grid.Grid, startPoint: Point):
		self.startP: Point = startPoint
		self.grid: grid.Grid = grid
		self.snakeDelta: float = 0
		self.MOVECONSTANT: float = 0.25
		self.FoodPerSpeedup: int = 3
		self.moveDelay: float = self.MOVECONSTANT
		self.facing: int = 0
		self.score: int = 0
		self.isPaused = False
		self.isOver = False
		# 0 -- Up
		# 1 -- Right
		# 2 -- Down
		# 3 -- Left

		self.bodyPos: list[Point] = []
		self.bodyPos.append(self.startP)

		self.body: list[Rectangle] = []
		self.bodyColor: list[any] = []
		targRect = grid.getRectFromIndex(int(self.startP.x), int(self.startP.y))
		startRect = Rectangle(targRect.p1, targRect.p2)
		startRect.setFill('white')
		startRect.setWidth(0)
		self.body.append(startRect)

	def update(self, delta: float) -> bool:
		self.snakeDelta += delta
		if(self.snakeDelta < self.moveDelay):
			return False
		elif(self.isPaused or self.isOver):
			return False
		self.snakeDelta = 0
		
		for pos in self.bodyPos:
			xInt = int(pos.x)
			yInt = int(pos.y)

		if(self.facing == 0):
			self.move(0, -1)
		elif(self.facing == 1):
			self.move(1, 0)
		elif(self.facing == 2):
			self.move(0, 1)
		elif(self.facing == 3):
			self.move(-1, 0)
		
		if(not self.isOutsideOfGrid()):
			xInt = int(self.bodyPos[0].x)
			yInt = int(self.bodyPos[0].y)
			for pos in self.bodyPos:
				xInt = int(pos.x)
				yInt = int(pos.y)
		return True

	def move(self, x: int, y: int):
		tmpX = self.startP.x
		tmpY = self.startP.y
		self.startP.x += x
		self.startP.y += y
		width = self.body[0].p2.x - self.body[0].p1.x
		height = self.body[0].p2.y - self.body[0].p1.y
		self.body[0].p1 = Point(self.grid.targRect.p1.x + self.startP.x * width, \
								self.grid.targRect.p1.y + self.startP.y * height)
		self.body[0].p2 = Point(self.grid.targRect.p1.x + (self.startP.x+1) * width, \
								self.grid.targRect.p1.y + (self.startP.y+1) * height)
		for i in range(1, len(self.bodyPos), 1):
			tmp2X = self.bodyPos[i].x
			tmp2Y = self.bodyPos[i].y
			self.bodyPos[i].x = tmpX
			self.bodyPos[i].y = tmpY
			self.body[i].p1 = Point(self.grid.targRect.p1.x + tmpX * width, \
									self.grid.targRect.p1.y + tmpY * height)
			self.body[i].p2 = Point(self.grid.targRect.p1.x + (tmpX+1) * width, \
									self.grid.targRect.p1.y + (tmpY+1) * height)
			tmpX = tmp2X
			tmpY = tmp2Y
		# self.body[0].move(width * x, height * y)
	
	def expandSnake(self, col: any = None):
		tmpX = self.bodyPos[-1].x
		tmpY = self.bodyPos[-1].y
		if(len(self.bodyPos) == 1):
			if(self.facing == 0):
				tmpY += 1
			elif(self.facing == 1):
				tmpX -= 1
			elif(self.facing == 2):
				tmpY -= 1
			elif(self.facing == 3):
				tmpX += 1
		else:
			prevTail = self.bodyPos[-1]
			prevTail2 = self.bodyPos[-2]
			dirX = prevTail.x - prevTail2.x
			dirY = prevTail.y - prevTail2.y
			tmpX += dirX
			tmpY += dirY

		if(tmpX < 0):
			tmpX = 0
		elif(tmpX >= self.grid.gridX):
			tmpX = self.grid.gridX-1
		if(tmpY < 0):
			tmpY = 0
		elif(tmpY >= self.grid.gridY):
			tmpY = self.grid.gridY-1

		targetRect = self.grid.getRectFromIndex(int(tmpX), int(tmpY))
		newTail = Rectangle(targetRect.p1, targetRect.p2)
		if(col == None):
			newTail.setFill('white')
		else:
			newTail.setFill(col)
		self.bodyPos.append(Point(tmpX, tmpY))
		self.body.append(newTail)

	def resetGame(self, undrawFirst: bool=True):
		if(undrawFirst):
			for p in self.body:
				p.undraw()
		self.body = self.body[:1]
		self.bodyPos = self.bodyPos[:1]
		self.bodyPos[0].x = self.grid.gridX//2
		self.bodyPos[0].y = self.grid.gridY//2
		self.move(0, 0)

	def draw(self, win: GraphWin):
		for p in self.body:
			p.draw(win)

	def undraw(self):
		for p in self.body:
			p.undraw()
	
	def isOutsideOfGrid(self) -> bool:
		xTmp = self.bodyPos[0].x
		yTmp = self.bodyPos[0].y
		return xTmp < 0 or xTmp >= self.grid.gridX or yTmp < 0 or yTmp >= self.grid.gridY
	
	def isTouchingWall(self) -> bool:
		return self.grid.containWall(self.startP)

	def isFoodInsideSnake(self, food: food.Food) -> bool:
		for pos in self.bodyPos:
			FIntX = int(food.foodPos.x)
			FIntY = int(food.foodPos.y)
			SIntX = int(pos.x)
			SIntY = int(pos.y)
			if(FIntX == SIntX and FIntY == SIntY):
				return True
		return False
	
	def isSnakeInsideSnake(self) -> bool:
		if(len(self.bodyPos) <= 1):
			return False
		headX = int(self.bodyPos[0].x)
		headY = int(self.bodyPos[0].y)
		for pos in range(1, len(self.bodyPos), 1):
			tailX = int(self.bodyPos[pos].x)
			tailY = int(self.bodyPos[pos].y)
			if(headX == tailX and headY == tailY):
				return True
		return False