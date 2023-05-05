from graphics import *
from wall import *
import random as rand
import math

class Grid:
	def __init__(self, targRect: Rectangle, gridX: int, gridY: int):
		self.gridX: int = gridX
		self.gridY: int = gridY

		self.targRect: Rectangle = targRect
		
		self.gridRect: list[Rectangle] = []
		self.wallList: list[Wall] = []
		self.hasDrawn: bool = False
		
		self.reset()

	def reset(self, undrawFirst: bool = False):
		if(undrawFirst):
			for rect in self.gridRect:
				rect.undraw()
		self.targRect.undraw()
		
		self.gridRect.clear()

		offsetX = self.targRect.getP1().x
		offsetY = self.targRect.getP1().y

		# List of gridboxes
		boxW = self.getWidth()/self.gridX
		boxH = self.getHeight()/self.gridY
		for y in range(self.gridY):
			for x in range(self.gridX):
				p1 = Point(offsetX + x * boxW, offsetY + y * boxH)
				p2 = Point(offsetX + (x+1) * boxW, offsetY + (y+1) * boxH)
				tmpRect = Rectangle(p1, p2)
				tmpRect.setOutline(color_rgb(20, 20, 20))
				self.gridRect.append(tmpRect)
		
		# Main grid
		self.targRect.setOutline('white') 

	def draw(self, win: GraphWin):
		if(not self.hasDrawn):
			for rect in self.gridRect:
				rect.draw(win)
			self.targRect.draw(win)
			self.hasDrawn = True
	
	def undraw(self):
		if(self.hasDrawn):
			for rect in self.gridRect:
				rect.undraw()
			self.targRect.undraw()
			self.hasDrawn = False
	
	def createWall(self, fromTarget: Point):
		tmpLoc: Point = Point(rand.randint(0, self.gridX-1), rand.randint(0, self.gridY-1))
		while(self.getDistanceBetweenPoints(tmpLoc, fromTarget) < WALL_DISTANCE_MIN or self.containWall(tmpLoc)):
			tmpLoc: Point = Point(rand.randint(0, self.gridX-1), rand.randint(0, self.gridY-1))
		tmpX = int(tmpLoc.x)
		tmpY = int(tmpLoc.y)
		self.wallList.append(Wall(tmpX, tmpY, self.getRectFromIndex(tmpX, tmpY)))

	def drawWall(self, win: GraphWin):
		for w in self.wallList:
			w.draw(win)

	def undrawWall(self):
		for w in self.wallList:
			w.undraw()

	def clearWall(self):
		self.wallList.clear()

	def resetRect(self, x: int, y: int, win: GraphWin):
		box = self.getRectFromIndex(x, y)
		box.undraw()
		box.setFill(None)
		box.draw(win)

	def getRectFromIndex(self, x: int, y: int) -> Rectangle:
		if(x < 0 or x >= self.gridX or y < 0 or y >= self.gridY):
			raise IndexError("X/Y Input is out of range.")
		else:
			return self.gridRect[x + y * self.gridX]
	
	def containWall(self, targetPos: Point) -> bool:
		targX = int(targetPos.x)
		targY = int(targetPos.y)
		for w in self.wallList:
			if(targX == w.xPos and targY == w.yPos):
				return True
		return False

	def getWidth(self) -> float:
		return self.targRect.getP2().x - self.targRect.getP1().x
	
	def getHeight(self) -> float:
		return self.targRect.getP2().y - self.targRect.getP1().y
	
	def getDistanceBetweenPoints(self, p1: Point, p2: Point) -> float:
		return math.sqrt(math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2))