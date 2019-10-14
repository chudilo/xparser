#!/usr/bin/python3
import requests
import json
import dicttoxml
import openpyxl

import sys
import re

from collections import OrderedDict
from xml.dom.minidom import parseString


#TODO: try block in request dict block
hitDict = {}
hitDictL = {}
notHitDict = {}

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
    #for item in typesDict:
    #    print(item)

    def __init__(self, data, relationId=None):
        Person.total += 1
        self.data = data
        self.relationId = relationId
        self.setId()
        self.setName()
        self.setPosition()
        self.setRelation()
        self.setRealties()
        self.setTransports()
        self.setIncome()

    def compareWithDict(self, value):
        if value:
            ret = []
            for type_ in self.typesDict:
                #print(type_['data'], value)
                cmpr = re.match(type_['data'], value.strip())
                if cmpr:
                    if value.strip() in hitDict.keys():
                        hitDict[value.strip()] += 1
                    else:
                        hitDict[value.strip()] = 1

                    return type_['value']

            else:
                for type_ in self.typesDict:
                    #print(type_['data'], value)
                    cmpr = re.match(type_['data'], value.strip().lower())
                    if cmpr:
                        if value.strip().lower() in hitDictL.keys():
                            hitDictL[value.strip()] += 1
                        else:
                            hitDictL[value.strip()] = 1

                        return type_['value']
                else:
                    if value in notHitDict.keys():
                        notHitDict[value] += 1
                    else:
                        notHitDict[value] = 1

                    return "~"+value+"~"

        else:
            return "[NONE]"

    def setId(self):
        self.id = Person.total

    def setName(self):
        if self.relationId is None:
            self.name = self.data[0][1]
        else:
            self.name = None

    #realtyType: 1 || 2, objectType, RealtyName, ownershipType (ownershipPart???), square, country
    def setRealties(self):
        self.realties = []
        for row in self.data:
            realty = self.getRealty(row[3:7])
            if realty != None:
                self.realties.append(realty)

            realty = self.getUsedRealty(row[7:10])
            if realty != None:
                self.realties.append(realty)

    def getRealty(self, row):
        #print(row)
        if isSlotEmpty(row[0]):
            return None
        else:
            realty = OrderedDict()
            realty['realtyType'] = 1
            realty['objectType'] = self.compareWithDict(row[0])
            realty['ownershipType'] = self.compareWithDict(row[1])
            realty['ownershipPart'] = None
            realty['sqare'] = row[1]
            realty['country'] = self.compareWithDict(row[3])

            '''
            realty = {'realtyType': 1, 'objectType': None,
                      'realtyName': row[0], 'ownershipType': None,
                      'square': row[2], 'country': None}
            # MAKE FUNCTION
            #print("row[0]", row[0])
            realty['objectType'] = self.compareWithDict(row[0])
            realty['ownershipType'] = self.compareWithDict(row[1])
            realty['country'] = self.compareWithDict(row[3])
            '''
            return realty

    def getUsedRealty(self, row):
        if isSlotEmpty(row[0]):
            return None
        else:
            #print("used realty:",row)
            realty = OrderedDict()
            realty['realtyType'] = 2
            realty['objectType'] = self.compareWithDict(row[0])
            realty['sqare'] = row[1]
            realty['country'] = self.compareWithDict(row[2])

            '''
            realty = {'realtyType': 2, 'objectType': None,
                      'realtyName': row[0],
                      'square': row[1], 'country': None}
            # MAKE FUNCTION
            realty['objectType'] = self.compareWithDict(row[0])
            realty['country'] = self.compareWithDict(row[2])
            '''

            return realty

    def setTransports(self):
        self.transports = []
        for row in self.data:
            #print("HERE", row[10])
            transport = self.getTransport(row[10])
            if transport == None:
                return None
            else:
                self.transports.append(transport)


    def getTransport(self, auto):
        if not isSlotEmpty(auto):
            for type_ in self.typesDict:
                return self.compareWithDict(auto)
        return None

    def setPosition(self):
        if not isSlotEmpty(self.data[0][2]):
            self.position = self.data[0][2]
        else:
            self.position = None

    #Have to use the dictionary here V
    def setRelation(self):
        if self.relationId:
            #print("relation Type")
            self.relationType = self.compareWithDict(self.data[0][1])
            #print(self.relationType)
        else:
            self.relationType = None

    def setIncome(self):
        self.income = self.data[0][11]

    def __str__(self):
        string = "ID: {}\nИмя: {}\nРодство: {}\nДолжность:{}\nДоход: {}\n".format(
            self.id, self.name, self.relationType, self.position, self.income)
        string += "Собственность:\n"

        if self.realties:
            for realty in self.realties:
                string += "\t" + "; ".join(map(str,realty.values())) + "\n"
        else:
            string += "\t" + "None" + "\n"


        string += "Транспорт:\n"
        if self.transports:
            for transport in self.transports:
                string += "\t" + str(transport) + "\n"
        else:
            string += "\t" + "None" + "\n"
        return string

#for from dict to xml parser
def list_func(name):
    #print(name)
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

'''
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
'''


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

    familyObjs = []
    relationId = None
    for person in family:
    #    parseRealties(person, fieldTypes)
        #print(person[0][0])

        if person[0][0]:
            tmp = Person(person)
            relationId = tmp.id
        else:
            tmp = Person(person, relationId)
        familyObjs.append(tmp)

    return familyObjs
        #print(tmp)
        #for realty in tmp.realties:
        #    print(realty)
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
        break
    return result
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


def saveToXml(people):
    '''
    if not count:
        count = len(people)
    if not rng:
        rng = (0, len(people))

    for i in range(rng[0],rng[1]):
    '''
    xmlFamilyString = '<?xml version="1.0" ?><persons xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="declarationXMLtemplate_Schema _transport_merged.xsd">'
    for family in people:
        for person in family:
            orderedPerson = OrderedDict()
            orderedPerson['id'] = person.id
            orderedPerson['name'] = person.name
            orderedPerson['relativeOf'] = person.relationId
            orderedPerson['relationType'] = person.relationType
            orderedPerson['realties'] = person.realties
            orderedPerson['transports'] = person.transports
            orderedPerson['income'] = person.income
            orderedPerson['incomeComment'] = None
            orderedPerson['incomeSource'] = None
            #we dont take two last fields from files, they said

            #xmlString = dicttoxml.dicttoxml(orderedPerson, custom_root="person" ,attr_type=False, item_func=list_func).decode()
            xmlString = dicttoxml.dicttoxml({'person': orderedPerson}, root=False ,attr_type=False, item_func=list_func).decode()
            #xmlString = re.sub(r'<(.*?)></(.*?)>', r'<\1 xsi:nil="true"/>', xmlString)
            #print(xmlString)
            xmlFamilyString += xmlString


    #print(res)
    prettyXml = parseString(xmlFamilyString + "</persons>").toprettyxml()
    #print(prettyXml)
    #res = re.findall(r'<.*?/>', prettyXml)
    #print(res)

    #print("\n\n\n\n")
    res = re.sub(r'<(.*?)/>', r'<\1 xsi:nil="true"/>', prettyXml, count=0)
    #print(res)
    with open("my_out/out.xml", 'w') as f:
        f.write(res)

        #re.sub(pattern, repl, string, count=0)
#<?xml version="1.0" ?>\n<persons xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="declarationXMLtemplate_Schema _transport_merged.xsd">
#[22:]
def main():
    filename = str(sys.argv[1])
    #print(filename)

    fieldTypes = getTypesDict()
    people = parseTable(filename, fieldTypes)
    saveToXml(people)
    '''
    print("POSITIVE COMPARE")
    print(json.dumps(hitDict, indent=4, ensure_ascii=False))

    print("POSITIVE COMPARE WITH LOWER")
    print(json.dumps(hitDictL, indent=4, ensure_ascii=False))

    print("NEGATIVE COMPARE")
    print(json.dumps(notHitDict, indent=4, ensure_ascii=False))
    '''
#from xml.dom.minidom import parseString
#print(parseString(dicttoxml.dicttoxml(dictionary, item_func=lambda x: x[:-1] ,attr_type=False)).toprettyxml())


if __name__ == "__main__":
    main()
