import requests
import json

data={
    "email":"trial@gmail.com",
    "password":'register',
    "first_name":"abcdef",
    "institute":"Vidyalaya",
    "standard":5,
    "requiresDonation":"true",
    "requiresMentor":"true",
    "requiresTutor":"true",
}

URL='http://127.0.0.1:8000/student-register'

json_data=json.dumps(data)
r=requests.post(url=URL, data=json_data)
data=r.json()
print(data)