from graphics_scale import *
from matrix import Matrix
from graphics import *

class MatrixImage():

    def __init__(self,win,start_point,matrix,container=None):
        self.internal_matrix = matrix
        self.container = container
        self.win = win
        self.start_point = start_point
        self.width = self.internal_matrix.width
        self.height = self.internal_matrix.height
        self.text_entries = []
        self._create_image()

    def _create_image(self):
        for x in range(self.height):
            st = ""
            for y in range(self.width):
                st += " {} ".format(str(round(self.get_entry(x,y),4)))

                #offset = 10
                #number = str(self.get_entry(x,y))
                #if len(number) > 2:
                    #offset -= len(number)
                #temp = TextScale(self.win,Point(self.start_point.x + (y * 4),self.start_point.y + (x * 4)),"{}".format(number),None,self.container)
                #temp.text.setSize(offset)
                #temp.text.setFill(color_rgb(255,255,255))
                #self.text_entries.append(temp)
            temp = TextScale(self.win,Point(self.start_point.x+(y*1.65),self.start_point.y + (x * 4)),"{}".format(st),None,self.container)
            temp.text.setFill(color_rgb(255,255,255))
            self.text_entries.append(temp)

    def get_entry(self,x,y):
        return self.internal_matrix.get_value(x,y)

    def undraw(self):
        for text in self.text_entries:
            text.undraw()

class MatrixEntry():

    def __init__(self,win,start_point,matrix,container=None):
        self.internal_matrix = matrix
        self.container = container
        self.win = win
        self.start_point = start_point
        self.width = self.internal_matrix.width
        self.height = self.internal_matrix.height
        self.text_entries = []
        self._create_image()
        self.show_matrix()

    def show_matrix(self):
        for y in range(self.height):
            for x in range(self.width):
                temp = self.internal_matrix.get_value(y,x)
                if temp != "":
                    self.text_entries[y*self.width+x].entry.setText(temp)

    def update_matrix(self):
        for x in range(self.width):
            for y in range(self.height):
                val = eval(self.text_entries[y*self.width+x].entry.getText())
                if type(val) == int or type(val) == float:
                    if val != "":
                        self.internal_matrix.set_value(y,x,val)

    def load_matrix(self,matrix):
        self.internal_matrix = matrix
        self.show_matrix()

    def _create_image(self):
        for x in range(self.height):
            for y in range(self.width):
                temp = EntryScale(self.win,Point(self.start_point.x + (y * 7),self.start_point.y + (x * 7)),3,self.container)
                self.text_entries.append(temp)


    def get_entry(self,x,y):
        return self.internal_matrix.get_value(x,y)

    def undraw(self):
        for text in self.text_entries:
            text.undraw()

"""class MatrixEntry():

    def __init__(self,win,center,width,height,container=None):
        self.width = width
        self.height = height
        self.rectangle = Container(win,center.x-width*3,center.y-height*3,center.x+width*3,center.y+height*3,container)
        self.matrix = Matrix.emptyMatrix(width,height)
        self.entries = [None] * width * height




    def getEntry(self,x,y):
        return self.entries(y * self.width + x).getText()

    def setEntry(self,x,y,value):
        if type(value) == float or type(value) == int:
            #self.entries[y * self.width + x].setText(value)
            self.matrix.set_value(value)

    def undraw(self):
        for i in self.entries:
            i.entry.undraw()
        self.rectangle.undraw()"""



