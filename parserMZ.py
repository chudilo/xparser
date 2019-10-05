#!/usr/bin/python3
import requests
import json
import dicttoxml
import openpyxl

import sys
import re

def getTypesDict():
    url = "https://declarator.org/media/dumps/patterns.json"
    entities = requests.get(url).json()
    return entities


def isSlotEmpty(string):
    if string:
        empty = ('-', ' ', '', 'не имеет', None)
        if string.strip() in empty:
            return True
        else:
            return False
    else:
        return True

class Person(object):
    total = 0
    typesDict = getTypesDict()

    def __init__(self, data, relationId=None):
        Person.total += 1
        self.data = data
        self.relationId = relationId
        self.setId()
        self.setName()
        self.setPosition()
        self.setRelation()
        #self.setRealties()
        #self.setTransports()
        self.setIncome()

    def setId(self):
        self.id = Person.total

    def setName(self):
        if self.relationId is None:
            self.name = self.data[0][1]
        else:
            self.name = None

    def setPosition(self):
        if not isSlotEmpty(self.data[0][2]):
            self.position = self.data[0][2]
        else:
            self.position = None

    #Have to use the dictionary here V
    def setRelation(self):
        if self.relationId:
            self.relationType = self.data[0][1]
        else:
            self.relationType = None

    def setIncome(self):
        self.income = self.data[0][11]

    def __str__(self):
        return "ID: {}\nИмя: {}\nРодство: {}\nДолжность: {}\nДоход: {}\n".format(
            self.id, self.name, self.relationType, self.position, self.income)

#for from dict to xml parser
def list_func(name):
    print(name)
    if name == "transports":
        return "transport"
    elif name == "realties":
        return "realty"


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
    pass
    '''
    13 fields: 1.num, 2.name 3.position 4. value
    5-8.property 9-11.used property 12.vehicle 13.extra income

    print('{:<2d}{:<15s}{:>30s}{:>12f}{:<10s}{:>10s}{:>12f}{:>12s}{:>12s}{:>12f}{:>12s}{:>12s}{:>12s}'.format(data[0],
data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],
data[10],data[11],data[12]))

    print(data[0])
    print('{:<2d}'.format(data[0]))
    '''

def parseName():
    return None

def parsePosition():
    return None

def parseRealties(person, fieldTypes):
    for raw in person:
        if raw[3] not in [u'-', u' ', u'', None]:
            for type_ in fieldTypes:
                #print(type_['data'], raw[3])
                res = re.match(type_['data'], raw[3])
                if res:
                    print(type_['value'])
                    #print(res)
                    break

    return None

def parseTransports():
    return None

def parseIncome():
    return None


def getRelativeType(relation, fieldTypes):
    return None


def parseFamily(family, passThroughId, fieldTypes):
    passThroughId += 1
    officialId = passThroughId
    official = {"id": officialId,
              "name:": parseName(),
              "relativeOf": None,
              "relativeType": None,
              "position": parsePosition(),
              #"realties": parseRealties(),
              "transports": parseTransports(),
              "income": parseIncome(),
              }

    familyDicts = [official]

    for i in range(1, len(family)):
        passThroughId += 1
        person = {"id": passThroughId,
                  "name:": None,
                  "relativeOf": officialId,
                  "relativeType": getRelativeType(family[i][1], fieldTypes),
                  "position": parsePosition(),
                  #"realties": parseRealties(),
                  "transports": parseTransports(),
                  "income": parseIncome(),
                  }

        familyDicts.append(person)

    for person in familyDicts:
        print(person)
    return familyDicts



def getFamilyDicts(rawFamily, fieldTypes):
    family = []
    person = [rawFamily[0]]
    for i in range(1, len(rawFamily)):
        #print(" | ".join(map(str,row)))
        if not rawFamily[i][1]:
            person.append(rawFamily[i])
        else:
            family.append(person)
            person = [rawFamily[i]]
    family.append(person)

    for person in family:
    #    parseRealties(person, fieldTypes)
        #print(person[0][0])
        if person[0][0]:
            tmp = Person(person)
        else:
            tmp = Person(person, Person.total)

        print(tmp)
    #familyDicts = parseFamily(family, 0, fieldTypes)
    '''
    #printing the family
    for person in family:
        for row in person:
            print(row)
        print()
    '''
    return None


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

    result = []
    for person in rawPeople:
        result.append(getFamilyDicts(person, fieldTypes))

    #print(rawPeople[0])
    #print(rawPeople[0][0])
    #for person in rawPeople[0]:
        #formatPrint(person)
    #    print(person[:13])
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
#from xml.dom.minidom import parseString
#print(parseString(dicttoxml.dicttoxml(dictionary, item_func=lambda x: x[:-1] ,attr_type=False)).toprettyxml())


if __name__ == "__main__":
    main()
