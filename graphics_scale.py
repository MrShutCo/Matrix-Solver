#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Tyler
#
# Created:     05/10/2016
# Copyright:   (c) Tyer 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from graphics import *
import time


class Container():

    def __init__(self,win,perXStart,perYStart,perXEnd,perYEnd,container=None,shape="rectangle"):
        self.can_contain = True
        self.container = container
        self.win = win
        self.perXStart = perXStart
        self.perYStart = perYStart
        self.perXEnd = perXEnd
        self.perYEnd = perYEnd
        self.children = []
        self.shape = None

        if container != None:
            self.container.add_item(self)
            self.p1 = Point(container.width * (self.perXStart / 100) + container.top_left.x,container.height * (self.perYStart / 100) + container.top_left.y)
            self.p2 = Point(container.width * (self.perXEnd / 100) + container.top_left.x,container.height * (self.perYEnd / 100) + container.top_left.y)
        else:
            self.p1 = Point(self.win.getWidth() * (self.perXStart / 100),self.win.getHeight() * (self.perYStart / 100))
            self.p2 = Point(self.win.getWidth() * (self.perXEnd / 100),self.win.getHeight() * (self.perYEnd / 100))

        self.top_left = self.p1

        self.width = abs(self.p1.getX() - self.p2.getX())
        self.height = abs(self.p1.getY() - self.p2.getY())

        self.is_drawn = False

        if shape == "rectangle":
            self.shape = Rectangle(self.p1,self.p2)
            self.shape.draw(win)


    def undraw(self):
        self.shape.undraw()

    def add_item(self,item):
        if self.can_contain:
            self.children.append(item)

    def del_item(self,item):
        if self.can_contain:
            self.children.remove(item)

    def getChildren(self):
        if self.can_contain:
            return self.children

    def setFill(self,color):
        self.shape.setFill(color)

    def hide(self):
        for child in self.children:
            child.undraw()
            if type(child) == RectangleScale:
                child.hide()
            else:
                if type(child) == Button:
                    child.deactivate()

    def show(self):
        for child in self.children:
            child.draw()
            if type(child) == RectangleScale:
                child.show()
            else:
                if type(child) == Button:
                    child.activate()


class RectangleScale(Container):

    def __init__(self,win,perXStart,perYStart,perXEnd,perYEnd,container = None):

        Container.__init__(self,win,perXStart,perYStart,perXEnd,perYEnd,container)

        self.is_drawn = True

        self.rectangle = Rectangle(self.p1,self.p2)
        if container != None:
            container.add_item(self)

    def draw(self):
        if self.is_drawn == False:
            self.rectangle.draw(self.win)
            self.is_drawn = True
            Container.draw()

    def undraw(self):
        if self.is_drawn:
            self.rectangle.undraw()
            self.is_drawn = False
            Container.undraw(self)


    def setFill(self,color):
        self.rectangle.setFill(color)

    def add_item(self,item):
        self.children.append(item)

class LineScale(Container):

    def __init__(self,win,perXStart,perYStart,perXEnd,perYEnd,container=None):
        self.can_contain = False
        Container.__init__(self,win,perXStart,perYStart,perXEnd,perYEnd,container,"line")

        self.line = Line(self.p1,self.p2)
        self.line.draw(self.win)

    def draw(self):
        if self.is_drawn == False:
            self.rectangle.draw(self.win)
            self.is_drawn = True
            self.container.draw()

    def undraw(self):
        if self.is_drawn:
            self.rectangle.undraw()
            self.is_drawn = False
            self.container.undraw()

class CircleScale():

    def __init__(self,win,perXStart,perYStart,perRadius,container=None):
        self.can_contain = False
        if container != None:
            self.circle = Circle(Point(container.width * (perXStart / 100) + container.top_left.x,container.height * (perYStart / 100) + container.top_left.y),
                             container.width * (perRadius / 100) / 2)
            print("HELLO")
        else:
            self.circle = Circle(Point(win.getWidth() * (perXStart / 100) + container.top_left.x, * (perYStart / 100) + container.top_left.y),
                             container.width * (perRadius / 100) / 2)
            print("HELLo")
            container.add_item(self)

        self.circle.draw(win)

    def draw(self):
        if self.is_drawn == False:
            self.rectangle.draw(self.win)
            self.is_drawn = True

    def undraw(self):
        if self.is_drawn:
            self.rectangle.undraw()
            self.is_drawn = False

class EntryScale():

    def __init__(self,win,anchor,size,container=None):
        if container == None:
            self.entry = Entry(Point(anchor.getX() * win.getWidth()/100,anchor.getY() * win.getHeight()/100),size)
            self.entry.draw(win)
        else:
            self.entry = Entry(Point(container.width * (anchor.x / 100) + container.top_left.x,container.height * (anchor.y / 100) + container.top_left.y),size)
            self.entry.draw(win)
            container.add_item(self)

    def undraw(self):
        self.entry.undraw()

class TextScale():

    def __init__(self,win,anchor,text,lock_type=None,container=None):
        if lock_type == "Top":
            self.text = Text(Point(container.top_left.x + (anchor * container.width /100),container.top_left.y+12),text)
            self.text.draw(win)
        if lock_type == "Bottom":
            self.text = Text(Point(container.top_left.x + (anchor * container.width /100),container.p2.y-12),text)
            self.text.draw(win)
        if lock_type == "Right":
            self.text = Text(Point(container.top_left.x,container.p2.y-12),text)
            self.text.draw(win)
        if container != None:
            self.text = Text(Point(container.width * (anchor.x / 100) + container.top_left.x,container.height * (anchor.y / 100) + container.top_left.y),text)
            self.text.draw(win)
            container.add_item(self)
        else:
            self.text = Text(Point(anchor.getX() * win.getWidth()/100,anchor.getY() * win.getHeight()/100),text)
            self.text.draw(win)

    def undraw(self):
        self.text.undraw()


#TODO: Get this to the Container system
class LockObject(Container):

    def __init__(self,win,width,height,anchor,lock_type="None",container=None):

            if lock_type == "Left":
                Container.__init__(self,win,0,anchor - height / 2,width,anchor + height / 2,container)

            if lock_type == "Right":
                Container.__init__(self,win,100-width,anchor - height / 2,100,anchor + height / 2,container)

            if lock_type == "Top":
                Container.__init__(self,win,anchor - width / 2,0,anchor + width / 2,height,container)

            if lock_type == "Bottom":
                Container.__init__(self,win,anchor - width / 2,100-height,anchor + width / 2,100,container)

            if lock_type == "Center":
                Container.__init__(self,win,50-width/2,50-height/2,50+width/2,50+height/2,container)


class Button:
    """ A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active qnd p is inside """

    def __init__(self, win, center, width, height, label,container=None):
        """Creates a rectangular button, eg:
            qb = Button(myWin, centerPoint, width, height, 'Quit')"""
        if container == None:
           self.center = Point(center.getX() * win.getWidth()/100,center.getY() * win.getHeight()/100)
           self.p1 = Point(self.center.x - width * win.getWidth()/200, self.center.y - height * win.getHeight()/200)
           self.p2 = Point(self.center.x + width * win.getWidth()/200, self.center.y + height * win.getHeight()/200)
        else:
           self.center = Point(container.top_left.x + (center.x * container.width/100),container.top_left.y + (center.getY() * container.height/100))
           self.p1 = Point(self.center.x - width * container.width/200, self.center.y - height * container.height/200)
           self.p2 = Point(self.center.x + width * container.width/200, self.center.y + height * container.height/200)
           container.add_item(self)
        self.win = win
        self.rect = Rectangle(self.p1,self.p2)
        self.label = Text(self.center, label)
        self.rect.draw(win)
        self.rect.label = Text(self.center, label)
        self.label.draw(win)
        self.mouse_in = False
        self.activate(0)

    def undraw(self):
        """Undraws the button"""
        self.rect.undraw()
        self.label.undraw()

    def draw(self):
        """Draw the button"""
        self.rect.draw(self.win)
        self.label.draw(self.win)

    def clicked(self, p):
        """Returns true if button active and p is inside"""
        return (self.active and
            self.p1.x <= p.getX() <= self.p2.x and
            self.p1.y <= p.getY() <= self.p2.y)

    def mouse_under(self,p):
        if (self.p1.x <= p.getX() <= self.p2.x and
            self.p1.y <= p.getY() <= self.p2.y):
            self.mouse_in = True
            return True
        self.mouse_in = False
        return False

    def getLabel(self):
        """Returns the label string of this button"""
        return self.label.getText()

    def activate(self, option=0):
        """Sets this button to 'active'."""
        if (option == 0):
            #self.rect.setOutline(color_rgb(100, 0, 0))
            self.label.setFill(color_rgb(255, 255, 255))
            self.rect.setFill("red")
        elif (option == 1):
            self.rect.setOutline(color_rgb(36, 36, 36))
            self.label.setTextColor('white')
            self.rect.setFill(color_rgb(36, 36, 36))
        self.rect.setWidth(2)
        self.active = True

    def deactivate(self, option=0):
        """Sets this button to 'inactive'."""
        if (option == 0):
            self.rect.setOutline(color_rgb(0, 0, 0))
            self.label.setFill('lightgrey')
            self.rect.setFill('darkgrey')
        elif (option == 1):
            self.rect.setOutline(color_rgb(36, 36, 36))
            self.label.setTextColor('black')
            self.rect.setFill(color_rgb(36, 36, 36))
        self.rect.setWidth(2)
        self.rect.setWidth(1)
        self.active = False


def main():

    win = GraphWin("Testing Grounds",1000,750)

    container_test_1(win)
    #line_test_1(win)
    #circle_test_1(win)

    win.getMouse()
    win.close()

    pass

def circle_test_1(win):
    container = Container(win,10,10,90,90)

    circle = CircleScale(win,50,50,50,container)

def line_test_1(win):
    container = Container(win,1,1,99,99)

    for i in range(20):
        line = LineScale(win,i*5,0,i*5,100,container)
        line2 = LineScale(win,0,i*5,100,i*5,container)

def container_test_1(win):
    container = Container(win,1,1,100,100)

    rect_meta = [Container(win,1,1,100,100,container)]
    circle_meta = [CircleScale(win,50,50,90,container)]
    line_meta = []
    for i in range(100):
        time.sleep(0.1)
        line_meta.append(LineScale(win,10,10,90,90,rect_meta[i-1]))
        line_meta.append(LineScale(win,90,10,10,90,rect_meta[i-1]))
        if i % 4 == 0:
            rect_meta.append(LockObject(win,90,90,50,"Left",rect_meta[i-1]))
            circle_meta.append(CircleScale(win,50,50,90,rect_meta[i-1]))
        elif i % 4 == 1:
            rect_meta.append(LockObject(win,90,90,50,"Center",rect_meta[i-1]))
        elif i % 4 == 2:
            rect_meta.append(LockObject(win,90,90,50,"Center",rect_meta[i-1]))
        else:
            rect_meta.append(LockObject(win,90,90,50,"Right",rect_meta[i-1]))
            circle_meta.append(CircleScale(win,50,50,90,rect_meta[i-1]))
