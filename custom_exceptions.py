#Custom errors for custom error messages

class MatrixDivideError(Exception):
    '''Raised when a matrice is attempted to be divided'''

class MatrixSizeError(Exception):
    '''Raised when the Matrices aren't the same size'''

class MatrixMultiplyError(Exception):
    '''Raised usually when two matrices can't be multiplied'''

class MatrixInverseError(Exception):
    '''Raised when the determinant of a matrix is 0'''

class MatrixPowerError(Exception):
    '''Raised when the power of a matrix is either wrong size or is raised to 0'''
