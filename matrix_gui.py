#This is the main program, where all the gui and interfacing happens

from graphics import *
from graphics_scale import *
from matrix import *
from matrix_container import *
from matrix_gui import *
from matrix_storage import *
import re


#All the logic for the editing menu, takes in a window and matrices, then returns
#the matrices and any changes done to it
def enter_edit_menu(win, matrices):
    container = Container(win,5,10,95,95)
    back_button = Button(win,Point(50,90+5),30,7.5,"Back",container)

    matrix_m = EntryScale(win,Point(45,75+5),2,container)
    matrix_n = EntryScale(win,Point(55,75+5),2,container)
    x = TextScale(win,Point(50,75+5),"x",None,container)
    x.text.setFill("white")
    gen_button = Button(win,Point(50,81.5+5),15,7.5,"Create",container)
    editor_helper = TextScale(win,Point(50,5),"Editing Matrix:",None,container)
    editor_helper.text.setSize(13)
    editor_helper.text.setFill("white")

    info = TextScale(win,Point(82.5,90),"",None,container)
    info.text.setFill("white")
    info.text.setSize(15)

    matrix = None
    buttons = load_entry_buttons(win,container)
    is_enter_edit = True

    while is_enter_edit:
        click = win.checkMouse()
        right_click = win.checkRightMouse()
        if right_click != None:
            for button in buttons:
                if button.clicked(right_click) and matrix != None:
                    try:
                        matrix.update_matrix()
                        matrices.set_matrix(button.getLabel(),matrix.internal_matrix)
                        info.text.setText("Saved Matrix {}".format(button.getLabel()))
                    except:
                        info.text.setText("Error, check input")

        if click != None:
            for button in buttons:
                if button.clicked(click):
                    temp_matrix = matrices.get_matrix(button.getLabel())
                    if matrix != None:
                        matrix.undraw()
                    matrix = MatrixEntry(win,Point(18.5+((10-temp_matrix.width)*3.555),5+5+(10-temp_matrix.height)*3.5),temp_matrix,container)
                    editor_helper.text.setText("Editing Matrix: {}".format(button.getLabel()))

            if back_button.clicked(click):
                win.autoflush = False
                container.hide()
                is_enter_edit = False
                container = None
            if gen_button.clicked(click):
                try:
                    m = int(matrix_m.entry.getText())
                    n = int(matrix_n.entry.getText())
                    if type(m) == int and type(n) == int:
                        if 1 <= m <= 10 and 1 <= n <= 10:
                            if matrix != None:
                                matrix.undraw()
                            info.text.setText("Created {}x{} matrix".format(m,n))
                            editor_helper.text.setText("Editing new Matrix")
                            matrix = MatrixEntry(win,Point(18.5+((10-m)*3.555),5+5+(10-n)*3.5),Matrix.emptyMatrix(m,n),container)
                except ValueError:
                    info.text.setText("Matrix size\n is not a number!")

    return matrices

#Helper function to create buttons for Edit menu (A-J)
def load_entry_buttons(win,container):
    helper = TextScale(win,Point(17.5,90+5),"Left click to load\nRight click to save",None,container)
    letters="ABCDEFGHIJ"
    buttons = []
    for x in range(5):
        for y in range(2):
            buttons.append(Button(win,Point(5+(x*8),5+75+(y*7)),5,5,letters[y*5+x],container))
    return buttons

#This is the main loop for the calculator menu.
#Once again this updates any matrices then returns them
def calculate_menu(win,matrices_calc):
    container = Container(win,5,10,95,95)
    #TODO: Turn into a custom ScaleObject, that can then append things to it
    entry = TextScale(win,Point(50,44.5),"",None,container)
    entry.text.setSize(16)
    entry.text.setFill(color_rgb(255,255,255))
    back_button = Button(win,Point(50,90),30,10,"Back",container)
    solve_button = Button(win,Point(40,54.5),15,7.5,"Solve",container)
    clear_button = Button(win,Point(60,54.5),15,7.5,"Clear",container)
    ans_button = Button(win,Point(80,54.5),15,7.5,"ANS",container)

    error_text = TextScale(win,Point(50,48),"",None,container)
    error_text.text.setFill(color_rgb(255,255,255))

    A,B,C,D,E,F,G,H,I,J = matrices_calc.unload_matrices()

    buttons, matrices = load_presets(win,container)

    valid_keys = "abcdefghij0123456789"
    valid_operators = {"plus" : "+","minus" : "-","asterisk": "*", "slash" : "/", "space" : " ", "asciicircum":"^", "parenleft":"(","parenright":")", "period":"."}
    shower_matrix = None
    solution_matrix = None
    is_calculate = True
    lastmove = None
    solution = None
    Z = None

    matrix_name = TextScale(win,Point(22.5,3),"Matrix:",None,container)
    matrix_name.text.setSize(15)
    matrix_name.text.setFill(color_rgb(255,255,255))

    #Lots of checks for left click, right click, mouse-over and key presses
    while is_calculate:
        click = win.checkMouse()
        right_click = win.checkRightMouse()
        keypress = win.checkKey()
        move = win.checkMovement()
        if move != None:
            for button in matrices:
                if ans_button.clicked(move) and Z != None and type(Z) != float and type(Z) != int:
                    if shower_matrix != None:
                        shower_matrix.undraw()
                    shower_matrix = MatrixImage(win,Point(4.5+((10-Z.width)*2.3),6+(10-Z.height)*2.3),Z,container)
                    matrix_name.text.setText("Matrix ANS")


                if button.clicked(move):
                     if button.mouse_in == False:
                        button.mouse_in = True
                        if (shower_matrix != None):
                            shower_matrix.undraw()
                        temp = matrices_calc.get_matrix(button.getLabel())
                        shower_matrix = MatrixImage(win,Point(4.5+((10-temp.width)*2.3),6+(10-temp.height)*2.3),temp,container)
                        matrix_name.text.setText("Matrix {}".format(button.getLabel()))
                else:
                    button.mouse_in = False
        if right_click != None:
            for button in matrices:
                if button.clicked(right_click):
                    if solution != None:
                        matrices_calc.set_matrix(button.getLabel(), solution)
                        if button.mouse_in:
                            temp = matrices_calc.get_matrix(button.getLabel())
                            if shower_matrix != None:
                                shower_matrix.undraw()
                            shower_matrix = MatrixImage(win,Point(4.5+((10-temp.width)*2.3),6+(10-temp.height)*2.3),temp,container)


        if click != None:
            if back_button.clicked(click):
                container.hide()
                is_calculate = False
                container = None
            if clear_button.clicked(click):
                entry.text.setText("")
                error_text.text.setText("")
                if solution_matrix != None:
                    solution_matrix.undraw()
            if ans_button.clicked(click):
                entry.text.setText(entry.text.getText() + "ANS")

            if solve_button.clicked(click):
                try:
                    solution = eval(cleanup_solution(entry.text.getText()))
                    Z = solution
                    if solution_matrix != None:
                        solution_matrix.undraw()
                    if type(solution) == Matrix:
                        solution_matrix = MatrixImage(win,Point(60.5+((10-solution.width)*2.3),5+(10-solution.height)*2.3),solution,container)
                    if type(solution) == int or type(solution) == float:
                        solution_matrix = TextScale(win,Point(60.5,5+9*2.3),round(solution,4),None,container)
                        solution_matrix.text.setFill("white")
                        solution_matrix.text.setSize(16)
                except MatrixSizeError:
                    error_text.text.setText("Matrices must be of the same size!")
                except MatrixMultiplyError:
                     error_text.text.setText("Matrices can't be multiplied (wrong sizes)")
                except MatrixInverseError:
                    error_text.text.setText("Matrix can't be inverted")
                except MatrixPowerError:
                    error_text.text.setText("Matrix power must be to -1 or a whole number")
                except MatrixDivideError:
                    error_text.text.setText("Matrix division is not defined")
                except Exception:
                    error_text.text.setText("Something else went wrong, check valid input")
            for button in buttons:
                if button.clicked(click):
                    if len(entry.text.getText()) < 15:
                        entry.text.setText(entry.text.getText() + button.getLabel())
            for button in matrices:
                if button.clicked(click):
                    if len(entry.text.getText()) < 15:
                        entry.text.setText(entry.text.getText() + button.getLabel())
        if keypress != "":
            if keypress == "BackSpace":
                entry.text.setText(entry.text.getText()[:-1] )
                error_text.text.setText("")
            if keypress == "Return":
                try:
                    solution = eval(cleanup_solution(entry.text.getText()))
                    Z = solution
                    if solution_matrix != None:
                        solution_matrix.undraw()
                    if type(solution) == Matrix:
                        solution_matrix = MatrixImage(win,Point(60.5+((10-solution.width)*2.3),5+(10-solution.height)*2.3),solution,container)
                    if type(solution) == int or type(solution) == float:
                        solution_matrix = TextScale(win,Point(60.5,5+9*2.3),round(solution,4),None,container)
                        solution_matrix.text.setFill("white")
                        solution_matrix.text.setSize(16)
                except MatrixSizeError:
                    error_text.text.setText("Matrices must be of the same size!")
                except MatrixMultiplyError:
                     error_text.text.setText("Matrices can't be multiplied (wrong sizes)")
                except MatrixInverseError:
                    error_text.text.setText("Matrix can't be inverted")
                except MatrixPowerError:
                    error_text.text.setText("Matrix power must be to -1 or a whole number")
                except MatrixDivideError:
                    error_text.text.setText("Matrix division is not defined")
                except Exception:
                    error_text.text.setText("Something else went wrong, check valid input")
            for key, value in valid_operators.items():
                if key == keypress and len(entry.text.getText()) < 15:
                    entry.text.setText(entry.text.getText() + value)
            for key in valid_keys:
                if key == keypress and len(entry.text.getText()) < 15:
                    entry.text.setText(entry.text.getText() + keypress.upper())
        lastmove = move
    return matrices_calc

#Use some regexes to clean up and tidy input for a nicer eval()
def cleanup_solution(string):
    string = string.replace("ANS","Z")
    for i in range(5):
        string = re.sub(r"([A-Z]|[0-9])([A-Z])",r"\1*\2",string,10)
    string = re.sub(r"([A-Z])(\()", r"\1*\2",string,10)
    string = re.sub(r"([A-Z]\^(-1|\d\d|\d))",r"(\1)",string,10)
    return string


#Helper function for making all the buttons for the calculate menu
def load_presets(win,container):

    buttons = []
    matrix = []

    for x in range(3):
        for y in range(3):
            buttons.append(Button(win,Point(10+(x*7),60+(y*7)),5,5,str(y*3+x+1),container))
    buttons.append(Button(win,Point(17,60+21),5,5,"0",container))

    helper = TextScale(win,Point(17.5,90),"Left click matrix to use\nRight click to edit",None,container)

    letters = "ABCDEFGHIJ"

    for x in range(5):
        for y in range(2):
            matrix.append(Button(win,Point(55+(x*8),62.5+(y*7)),6,6,letters[y*5+x],container))

    operations = "+-*/^"

    for x in range(5):
        buttons.append(Button(win,Point(55+(x*8),70+(y*8)),6,6,operations[x],container))


    return buttons, matrix


def main():
    win = GraphWin("Matrix Calculator",650,650,False)
    win.setBackground(color_rgb(55,55,55))


    title_text = TextScale(win,Point(50,5),"Matrix Calculator")
    title_text.text.setSize(36)
    title_text.text.setTextColor("white")

    matrices = MatrixStorage()

    is_over = False

    container = Container(win,5,10,95,95)
    container.setFill(color_rgb(100,100,100))

    calculate = Button(win,Point(50,25),50,20,"Calculate",container)
    enter_edit = Button(win,Point(50,50),50,20,"Enter/edit",container)
    quit_button = Button(win,Point(50,90),30,10,"Quit",container)

    #A = Matrix([[3,-2],[-1,4],[5,6]])
    #B = Matrix([[0,2,-1],[4,5,0]])
    #C = Matrix([[2,3],[4,-1]])
    #D = Matrix([[1,-2],[-4,3],[-3,2]])

    matrices.load_matrices("Storage")

    while is_over == False:
        click = win.checkMouse()
        pos = win.checkRightMouse()
        if click != None:
            if calculate.clicked(click):
                container.hide()
                matrices = calculate_menu(win,matrices)
                matrices.save_matrices("storage")
                container.show()
            if enter_edit.clicked(click):
                container.hide()
                win.autoflush = True
                matrices = enter_edit_menu(win,matrices)
                matrices.save_matrices("storage")
                container.show()
            if quit_button.clicked(click):
                is_over = True

    win.close()

if __name__ == '__main__':
    main()
