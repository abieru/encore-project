

import requests, json

url = "http://localhost:8000/Project_result_json/"

#datajson = json.dumps({'data': 'test'}) #HERE THE IFCjson (json format )


# HERE THE DATA 
dataload ={

    "uploadedIfcFileUUID": "af3e5333s-3472-423c-bed2-44a317f07ebwwww1",
    "projectUUID":  "2ee3a9ba-fa94-449df2-b346-c25sss0dab346c7",
    "name": "EDEA_demostrador_kees_test1.ifc",
    "userU":  "familynoth@gmail.com"
    
}

files ={'IFCFile': open('ifc_files/EDEA_demostrador_kees_test1.ifc','rb')}


# THE HEADER PARAMS
datajson =json.dumps(dataload)

header ={
    'Authorization': 'Token 09e0f193971d77896b5327218238dee6efc06ced',
    

}


#----POST EXAMPLE
#response = requests.post(url, data=dataload,headers=header, files=files)
response = requests.get(url, headers=header).json()
# HER U CAN SEE THE RESPONSE
print(response)

#----GET EXAMPLE




