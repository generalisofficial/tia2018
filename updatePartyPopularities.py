from os import listdir
from os import path
from codecs import open
from shutil import copyfile
import copy
import re
import os

path = r"C:\Users\Victor Bohman Lind\Documents\Paradox Interactive\Hearts of Iron IV\mod\the-information-age"
paths = [r'\history\countries',
         r'\events']
for subPath in paths:
    filePath = path+subPath
    for filename in listdir(filePath):
        if os.path.isfile(filePath+"\\"+filename):
            if subPath != paths[1]:
                file = open(filePath+"\\"+filename, 'r', 'utf-8-sig')
            else:
                file = open(filePath+"\\"+filename, 'r', 'utf-8')
            line = file.readline()
            checkingParties = 0
            text = ""
            emptyNewLinesToDelete=0
            while line:
                if "set_politics = {" in line:
                    emptyNewLinesToDelete = 1

                if "parties = {" in line:
                    text = text.rstrip()
                    checkingParties = 1
                    indentation = 2
                    ideologyCount = 0
                    ideologyList = []
                    ideologyValues = []
                    line = line.rstrip()
                    whiteSpaces = line.count(' ')+line.count('\t')*4-4
                elif checkingParties == 1:
                    splitLine = line.split(' ')
                    for string in splitLine:
                        string = string.strip()
                        if "#" in string:
                            break
                        if len(string) > 0:
                            if "{" in string:
                                indentation += 1
                            if "}" in string:
                                indentation -= 1
                            if "{" not in string and "}" not in string and indentation == 2 and "=" not in string:
                                ideologyList.append(string.strip())
                            for i in range(1, 255):
                                if not (ord('0') <= i <= ord('9')):
                                    string = string.strip(str(chr(i)))
                            if indentation == 3 and len(string) > 0:
                                try:
                                    float(string)
                                    ideologyValues.append(string.strip())
                                    ideologyCount += 1
                                except ValueError:
                                    cancer = 1
                    if indentation == 1 and "}" not in line:
                        if len(line.strip()) != 0 and text == text.rstrip():
                            text += '\n'
                        text += line
                    if indentation == 0:
                        whiteSpaces -= 1
                        for i in range(1, whiteSpaces-4):
                            text += ' '
                        text += "}\n\n"
                        for i in range(1, whiteSpaces):
                            text += ' '
                        text += "set_popularities = {\n"
                        x = 0
                        for j in range(0, ideologyCount):
                            for i in range(1, whiteSpaces+4):
                                text += ' '
                            text += ideologyList[j] + " = " + ideologyValues[j] + '\n'
                            x = x+float(ideologyValues[j])
                        if x != 100:
                            print(subPath+"\\"+filename+" wrong sum")
                        for i in range(1, whiteSpaces):
                            text += ' '
                        text += "}\n"
                        checkingParties = 0
                        emptyNewLinesToDelete = 0
                else:
                    text += line
                line = file.readline()
            file.close()
            if subPath != paths[1]:
                file = open(filePath + "\\" + filename, 'r', 'utf-8-sig')
            else:
                file = open(filePath + "\\" + filename, 'r', 'utf-8')
            originalText = file.read()
            file.close()
            if text != originalText:
                if subPath != paths[1]:
                    file = open(filePath + "\\" + filename, 'w', 'utf-8-sig')
                else:
                    file = open(filePath + "\\" + filename, 'w', 'utf-8')
                file.write(text)
                file.close()








