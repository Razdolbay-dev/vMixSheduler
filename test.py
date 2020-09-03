import xml.etree.ElementTree as ET
import os



a = []

root = ET.parse('res/API.xml').getroot()
root_find = root.findall('inputs/input')

for x in root_find:
    key = 'b7a13c0f-e592-4aa2-9ac2-7ef6595dddc2'
    inp = x.get('key')
    if inp == key:
        y = x.find('list')
        for i in y:
            a.append(i.text)
print(a)
