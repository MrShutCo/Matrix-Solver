#Interaction class, reads, writes and keeps track of the 10 matrices stored
#in a text file

from matrix import *

class MatrixStorage():

    def __init__(self):
        self.matrices = []
        for i in range(10):
            self.matrices.append(Matrix.emptyMatrix(i+1,i+1))

    def get_matrix(self,letter):
        letters = "ABCDEFGHIJ"
        for l in range(len(letters)):
            if letter == letters[l]:
                return self.matrices[l]

    def set_matrix(self,letter,matrix):
        letters = "ABCDEFGHIJ"
        for l in range(len(letters)):
            if letter == letters[l]:
                self.matrices[l] = matrix


    def unload_matrices(self):
        return tuple(self.matrices)

    def save_matrices(self,filename):
        file = open(filename+".txt","w")
        letters = "ABCDEFGHIJ"
        for m in range(len(self.matrices)):
            file.write("{}:{}x{}".format(letters[m],self.matrices[m].width,self.matrices[m].height))
            file.write(self.matrices[m].__repr__())
        file.close()

    def load_matrices(self,filename):
        file = open(filename+".txt","r")
        lines = file.readlines()
        line_counter = 0
        #tileMap = [list(row) for row in file.read().split('\n')]
        for i in range(10):
            matrix_info = lines[line_counter].rstrip("\n")
            matrix_name_size = matrix_info.split(":")
            matrix_name = matrix_name_size[0]
            matrix_size = matrix_name_size[1].split("x")
            matrix_values = []
            line_counter += 1
            for j in range(int(matrix_size[1])):
                matrix_entry = []
                for u in lines[line_counter].split(","):
                    matrix_entry.append(eval(u))
                matrix_values.append(matrix_entry)
                line_counter+=1
            self.set_matrix(matrix_name,Matrix(matrix_values))




