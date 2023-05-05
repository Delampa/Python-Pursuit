from graphics import *

WALL_DISTANCE_MIN: float = 5.0

class Wall:
    def __init__(self, x: int, y: int, refRect: Rectangle):
        self.xPos: int = x
        self.yPos: int = y
        self.pos: Point = Point(x, y)
        
        if(refRect != None):
            self.rect: Rectangle = Rectangle(refRect.p1, refRect.p2)
            self.rect.setFill('gray')
            self.rect.setOutline('red')
            self.rect.setWidth(2)
        else:
            self.rect: Rectangle = None

        self.hasDrawn: bool = False
    
    def draw(self, win: GraphWin):
        if(self.hasDrawn):
            return
        self.rect.draw(win)
        self.hasDrawn = True
    
    def undraw(self):
        if(not self.hasDrawn):
            return
        self.rect.undraw()
        self.hasDrawn = False