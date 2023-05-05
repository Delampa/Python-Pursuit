from graphics import *
import random

import grid

class Food:
	def __init__(self, grid: grid.Grid):
		self.grid: grid.Grid = grid
		self.foodCol = color_rgb(int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))

		tmpX = random.randint(0, grid.gridX-1)
		tmpY = random.randint(0, grid.gridY-1)
		self.foodPos: Point = Point(tmpX, tmpY)

		targRect = grid.getRectFromIndex(tmpX, tmpY)
		self.body: Rectangle = Rectangle(targRect.p1, targRect.p2)
		self.body.setFill(self.foodCol)
		self.body.setWidth(0)

		self.hasDrawn: bool = False
	
	def update(self, delta) -> bool:
		# TODO: something
		return True

	def draw(self, win: GraphWin):
		if(self.hasDrawn):
			return
		self.body.draw(win)
		self.hasDrawn = True

	def undraw(self):
		if(not self.hasDrawn):
			return
		self.body.undraw()
		self.hasDrawn = False

	def reset(self):
		width = self.body.p2.x - self.body.p1.x
		height = self.body.p2.y - self.body.p1.y
		tmpX = random.randint(0, self.grid.gridX-1)
		tmpY = random.randint(0, self.grid.gridY-1)
		self.foodPos.x = tmpX
		self.foodPos.y = tmpY
		self.body.p1 = 	Point(	self.grid.targRect.p1.x + tmpX * width, \
								self.grid.targRect.p1.y + tmpY * height)
		self.body.p2 = Point(	self.grid.targRect.p1.x + (tmpX+1) * width, \
								self.grid.targRect.p1.y + (tmpY+1) * height)
		self.foodCol = color_rgb(int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))
		self.body.setFill(self.foodCol)
	
	def isInsideWall(self):
		return self.grid.containWall(self.foodPos)