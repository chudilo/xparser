#!/usr/bin/python3
import requests
import json
import dicttoxml
import openpyxl

import sys

def getTypesDict():
    url = "https://declarator.org/media/dumps/patterns.json"
    entities = requests.get(url).json()
    return entities

'''
def getBorder(sheet):
    char = 'A'
    i = 0
    while sheet[char+str(i)].value:
        while
        i += 1
'''

def getPerson(sheet, fieldTypes):
    pass


def formatPrint(data):
    '''
    13 fields: 1.num, 2.name 3.position 4. value
    5-8.property 9-11.used property 12.vehicle 13.extra income
    '''
    '''
    print('{:<2d}{:<15s}{:>30s}{:>12f}{:<10s}{:>10s}{:>12f}{:>12s}{:>12s}{:>12f}{:>12s}{:>12s}{:>12s}'.format(data[0],
data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],
data[10],data[11],data[12]))
    '''
    print(data[0])
    print('{:<2d}'.format(data[0]))

def parseTable(filename, fieldTypes):
    excel_document = openpyxl.load_workbook(filename)
    #sheets = excel_document.get_sheet_names()
    sheets = excel_document.active.values
    rawPeople = []
    cond = False
    person = []
    for value in sheets:
        if value[0]:
            if value[0].__class__.__name__ == 'int':
                if cond:
                    rawPeople.append(person)
                    person = []
                else:
                    cond = True

        if cond:
            person.append(value)

    #print(rawPeople[0])

    for person in rawPeople[1]:
        formatPrint(person)

        #print(value)
        #break
        #rawPeople.append(value)


    #sheet = excel_document.get_sheet_by_name(sheets[0])

    #for i in range(1):
        #print(dir(sheet))
    #    print(dir(sheet.values)

    '''
    officials = ''[] #people
    #start, finish = getBorder(sheet)
    #head =
    #count = getCountOfPeople(sheet)
    position = 15
    left =
    #while True:
    person = getPerson(sheet, fieldTypes, position, left, right)
    if person:
        officials.append(person)

    print(person)
    '''

    '''
    char = 'A'
    while char <= 'Z':
        print(sheet[char+'15'].value)
        char = chr(ord(char) + 1)
    '''


def saveToXml():
    pass


def main():
    filename = str(sys.argv[1])
    #print(filename)

    fieldTypes = getTypesDict()
    people = parseTable(filename, fieldTypes)
    saveToXml()


if __name__ == "__main__":
    main()
