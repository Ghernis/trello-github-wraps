import csv
from dotenv import dotenv_values
import json
import requests
from models.Ticket import Ticket

config=dotenv_values('.env')

url = "https://api.trello.com/1/cards"

headers = {
  "Accept": "application/json"
}

query = {
  'idList': config['backlog'],
  'key': config['api_key'],
  'token': config['token']
}
def readData():
    data=[]
    with open('./data.csv')as csv_file:
        reader = csv.reader(csv_file,delimiter=';')
        for l in reader:
            aux = {
                'titulo':l[0],
                'motivation':l[1],
                'ac':l[2],
            }
            data.append(aux)
    return data

def createCard(card):
    query['name']=card['titulo']
    descrip = f"""
# Motivation

{card['motivation']}

# Acceptance Criteria    
{card['ac']}
    """
    query['desc']=descrip
    
    #response = requests.request("POST", url, headers=headers, params=query)
    #print(response)
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

#data = readData()

#for d in data:
#    createCard(d)
data = Ticket.load('./ceci.json')
print(data[len(data)-1])