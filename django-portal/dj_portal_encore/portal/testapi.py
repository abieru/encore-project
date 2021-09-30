import requests
import json

url = 'http://localhost:8000/api/v1.0/projects/'

response = requests.get(url)
print(response)
