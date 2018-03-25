#The main matrix class. This is where all operations are defined for them
#At the bottom are the tests for the test cases

from custom_exceptions import *
from matrix_inverse_helper import *

class Matrix:

    def __init__(self,values):
        self.internal_vals = values
        self.width = len(values[0])
        self.height = len(values)

    #Returns new empty matrix, acts as another constructor
    @classmethod
    def emptyMatrix(cls,width,height):
        return cls([[0 for col in range(width)] for row in range(height)])

    #Returns identity matrix, again as a constructor
    @classmethod
    def identityMatrix(cls,width,height):
        empty = Matrix.emptyMatrix(width,height)
        for x in range(height):
            for y in range(width):
                if x == y:
                    empty.set_value(x,y,1)
        return empty

    #-----------------Helper function--------

    def round(self,decimals):
        for x in range(self.height):
            for y in range(self.width):
                temp = self.get_value(x,y)
                self.set_value(x,y,round(temp,decimals))

    def samesize(self,other):
        return (self.height == other.height) and (self.width == other.width)

    def samewidth(self,other):
        return self.width == other.width

    def sameheight(self,other):
        return self.height == other.height

    def set_value(self,x,y,value):
        self.internal_vals[x][y] = value

    def get_value(self,x,y):
        return self.internal_vals[x][y]

    #----------------------END-----------------


    #----------------Overiding operators so eval will work on matrices------------
    def __add__(self, other):
        if self.samesize(other) == False:
            raise MatrixSizeError("Matrices are not the same size")
        resultant = Matrix.emptyMatrix(self.width,self.height)
        for x in range(self.height):
            for y in range(self.width):
                resultant.set_value(x,y,self.get_value(x,y) + other.get_value(x,y))
        return resultant

    def __sub__(self,other):
        if self.samesize(other) == False:
            #TODO: Raise new exception
            return None
        resultant = Matrix.emptyMatrix(self.width,self.height)
        for x in range(self.height):
            for y in range(self.width):
                resultant.set_value(x,y,self.get_value(x,y) - other.get_value(x,y))
        return resultant

    def __mul__(self,other):
        if type(other) == int or type(other) == float:
            resultant = Matrix.emptyMatrix(self.width,self.height)
            for x in range(self.height):
                for y in range(self.width):
                    resultant.set_value(x,y,other * self.get_value(x,y))
            return resultant
        if type(other) == Matrix:
            if self.width != other.height:
                raise MatrixMultiplyError("Matrix A width doesnt match Matrix B height")
            resultant = Matrix.emptyMatrix(other.width,self.height)
            for i in range(self.height):
                for j in range(other.width):
                    for k in range(self.width):
                        temp = resultant.get_value(i,j) + self.internal_vals[i][k] * other.internal_vals[k][j]
                        resultant.set_value(i,j,temp)
            return resultant

    def __rmul__(self,other):
        if type(other) == int or type(other) == float:
            resultant = Matrix.emptyMatrix(self.width,self.height)
            for x in range(self.height):
                for y in range(self.width):
                    resultant.set_value(x,y,other * self.get_value(x,y))
            return resultant
        if type(other) == Matrix:
            if self.width != other.height:
                raise MatrixMultiplyError("Matrix A width doesnt match Matrix B height")
            resultant = Matrix.emptyMatrix(other.width,self.height)
            for i in range(self.height):
                for j in range(other.width):
                    for k in range(self.width):
                        temp = resultant.get_value(i,j) + self.internal_vals[i][k] * other.internal_vals[k][j]
                        resultant.set_value(i,j,temp)
            return resultant

    #Override XOR just to look appealing, must be a square matrix
    def __xor__(self,other):
        if type(other) == int and self.width == self.height:
            print(other)
            if other > 0:
                resultant = Matrix.identityMatrix(self.width,self.height)
                print(resultant)
                for i in range(other):
                    resultant = resultant * self
                return resultant
            elif other == 0:
                raise MatrixPowerError("Matrix power can't be 0")
            elif other == -1:
                if self.width == 2:
                    result = self.clone()
                    try:
                        determinant = 1/((result.get_value(0,0)*result.get_value(1,1))-(result.get_value(1,0)*result.get_value(0,1)))
                        result = Matrix([[result.get_value(1,1),-result.get_value(0,1)],[-result.get_value(1,0),result.get_value(0,0)]])
                        final = determinant * result
                        #final.round(4)
                        return final
                    except:
                        raise MatrixInverseError("Matrix does not have an inverse")
                else:
                    result = self.clone()
                    try:
                        return Matrix(getMatrixInverse(result.internal_vals))
                    except:
                        raise MatrixInverseError("Matrix does not have an inverse")

        else:
            raise MatrixPowerError("Matrix power must be postive integer or -1")

    def __truediv__(self, other):
        raise MatrixDivideError("Matrices cannot be divided!")

    def __floordiv__(self,other):
        self.__truediv__()

    #---------------------End--------------

    def clone(self):
        return Matrix(self.internal_vals)

    def __str__(self):
        string = ""
        for x in self.internal_vals:
            string += "\n"
            for y in x:
                string += str(y) + ","

        return string + "\n"

    def __repr__(self):
        string = ""
        for x in self.internal_vals:
            string += "\n"
            for y in x:
                string += str(y) + ","
            string = string[:-1]

        return string + "\n"


def main():
    #firstTests()
    #secondTests()
    #thirdTest()
    #fourthTest()
    #evalTests()
    pass

def evalTests():
    A = Matrix([[3,-2],[-1,4],[5,6]])
    B = Matrix([[0,2,-1],[4,5,0]])
    C = eval("2 * A")
    print(C)

def secondTests():
     A = Matrix([[2.5,3.7,-8.1,-2],
                [4.2,5.3,-2.8,-3.6],
                [5.1,-6.2,0,-1.7],
                [-4.3,2.1,3.3,5]])
     B = Matrix([[3,6.1,5.4,-1.2],
                [-2.6,-1.8,-0.4,2.8],
                [5,-3.2,0,4.1],
                [2.7,0,-1.2,-3.4]])
     C = Matrix([[2],[0],[-3.5],[3]])

     result = A * B
     result.round(2)
     print(result)

def thirdTest():
    A = Matrix([[2,-10],
                [-1,5]])
    print(A^-1)

def fourthTest():
    A = Matrix([[0,2,0,1,0,0],
                [1,0,1,0,1,0],
                [0,1,0,0,0,0],
                [1,0,0,0,1,0],
                [0,1,0,1,0,2],
                [0,0,0,0,2,0]])
    print(A^10)

def firstTests():
    A = Matrix([[3,-2],[-1,4],[5,6]])
    B = Matrix([[0,2,-1],[4,5,0]])
    C = Matrix([[2,3],[4,-1]])
    D = Matrix([[1,-2],[-4,3],[-3,2]])

    print(2 * A)
    print(A + D)
    print(2*A - 0.5*D)
    #print(A+B)
    print(A*B)
    print(D*C)
    print(B*A)
    #print(A*D)
    print(C^3)
    print(C^-1)
    #print(D^3)
    #print(D^-1)
    print(2*B*A)
    print(2*C-B*A)
    print(C*B*A)
    print((C^-1)*(B*D))
    print(C*(C^-1))
    print((B*A)^2)
#firstTests()