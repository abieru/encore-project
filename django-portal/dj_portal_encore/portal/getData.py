import requests, re, json

from requests.auth import HTTPBasicAuth
from requests.sessions import Request
from django.urls import resolve, reverse_lazy
from pathlib import Path
from .PIN_DESA_PRO_PPAL_ADM_v4d import ifcjsonfunc

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR2 = Path(__file__).resolve().parent.parent

string2 = 'http://localhost:8000/748dd2a7-b5ed-4329-9028-28427abffe66/'

"""
cadena_deletras = string2.split("/")
len_ofcadena = len(cadena_deletras)-2
print(cadena_deletras[len_ofcadena])
"""

response = requests.get('https://demo.encorebim.eu/api/projects', auth=HTTPBasicAuth('brea', 'nw7H6Bq13pOL'))

response_json = response.json()
response_f =response_json['projectMetadataDTOList']
#print(response_f)

def getifcfile(projectid):
    try:
        response_ifcinfo = requests.get(f'https://demo.encorebim.eu/api/projects/{projectid}/ifcs', auth=HTTPBasicAuth('brea', 'nw7H6Bq13pOL')).json()
        
        #ifcdata = response_ifcinfo['ifcMetadataDTOList'][0]
        ifcidofFile =response_ifcinfo['ifcMetadataDTOList'][0]['uploadedIfcFileUUID']
        

        responsefileifc = requests.get(f'https://demo.encorebim.eu/api/projects/{projectid}/ifcs/{ifcidofFile}', auth=HTTPBasicAuth('brea', 'nw7H6Bq13pOL'))
        
        namefile = responsefileifc.headers['Content-Disposition']


        
        string_clean = re.sub("\;|\=","",namefile)
        cadenalimpia = string_clean[18:]
        
        
        file = open(f'{BASE_DIR2}/portal/ifc_files/{cadenalimpia}', "wb") 
        file.write(responsefileifc.content)
        print(f'nombre del archivo {file.name}')
        file.close()
        
        url_of_ifcFILE = f'{BASE_DIR2}/portal/ifc_files/{cadenalimpia}'
        #PRUEBA DE ARCHIVO JSON GENEBASE_DIR2RADO
        
        ifcjsonfunc(cadenalimpia)
    
        file = open(f'{BASE_DIR2}/portal/json_results/{cadenalimpia}.json', 'r')

        data = json.load(file)
        print(data)
        return data
    except:
        print('este archivo no se puede leer')




def getoneProject(projectid):
    response_project = requests.get(f'https://demo.encorebim.eu/api/projects/{projectid}', auth=HTTPBasicAuth('brea', 'nw7H6Bq13pOL')).json()
    return response_project



def getifcinfo(projectid):
    responsefileifc = requests.get(f'https://demo.encorebim.eu/api/projects/{projectid}/ifcs', auth=HTTPBasicAuth('brea', 'nw7H6Bq13pOL')).json()
    try:
        
        ifcdata = responsefileifc['ifcMetadataDTOList'][0]
        return ifcdata
    except:
        ifcdata = 'nodata'
        return ifcdata

