from encodings import utf_8
import re

def betweenLinesFill(filename, starting_text, ending_text, replacelines):
    with open(filename, 'r') as f: #Open original file to read it
        contents = f.read()

    to_replace = contents[contents.find(starting_text)+len(starting_text):contents.rfind(ending_text)] # what needs to be replaced

    contents = contents.replace(to_replace, "\n" + replacelines + "\n") # replacing it

    f = open(filename, "w")
    f.write(contents) # Rewrite the original file with the changed contents

replacelines0 = ("u = 10" + "\n" + 
                "v = 11" + "\n" + 
                "t = 20" + "\n" +
                "k = 0")

A_b = 1000

replaceLines = ("self.lineEdit_Ab.setText(_translate(" + "\"Dialog\"," + "\"" + str(A_b) + "\"" + "))" + "\n"
                "self.lineEdit_Ab.setText(_translate(" + "Dialog," + str(A_b) + "))" + "\n"
                "self.lineEdit_Ab.setText(_translate(" + "Dialog," + str(A_b) + "))" + "\n"
                "self.lineEdit_Ab.setText(_translate(" + "Dialog," + str(A_b) + "))" + "\n"
                "self.lineEdit_Ab.setText(_translate(" + "Dialog," + str(A_b) + "))" + "\n"
)   

betweenLinesFill("test.py", "#Begin", "#End", replaceLines)

