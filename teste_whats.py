import requests
import json
 
url = "https://api.conexaoia.digital/message/sendText/ronaldo"
 

message = "Olá, eu sou Ronaldo"


payload = json.dumps({
  "number": "5551992090470",
  "options": {
    "delay": 1200,
    "presence": "composing",
    "linkPreview": False
  },
  "textMessage": {
    "text": message
  }
})
headers = {
  'Content-Type': 'application/json',
  'apikey': 'B6D711FCDE4D4FD5936544120E713976'
}
 
response = requests.request("POST", url, headers=headers, data=payload)
 
print(response.text)