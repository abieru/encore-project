import json

f = open('ExportArchive.json', 'r')

data = json.load(f)

print(data)