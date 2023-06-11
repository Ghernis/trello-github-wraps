from typing import List
import datetime
import json
#pylint: disable=import-error
from dotenv import dotenv_values
import requests

from models.Ticket import Ticket

config=dotenv_values('.env')

class TrelloClient():
    headers = {
    "Accept": "application/json"
    }
    url='https://api.trello.com/1/'
    basic_query={
        'key': config['TRELLO_API_KEY'],
        'token': config['TRELLO_TOKEN'],
    }
    tickets:List[Ticket]
    def __init__(self,tickets):
        self.tickets=tickets

    def createCard(self,card,lista=config['list']):
        url = "https://api.trello.com/1/cards"
        query=self.basic_query
        query['name']=card.titulo
        query['idList']=lista
        inx=1
        acs=''
        for c in card.ac:
            acs=acs+f"\n{inx}. {c}"
            inx+=1
        descrip = f"""
# Motivation

{card.motivation}

# Acceptance Criteria    
{acs}

# Detalles tecnicos/Comandos
{card.cmd}"""

        query['desc']=descrip
        response = requests.request("POST", url, headers=self.headers, params=query,timeout=200)
        return json.loads(response.text)['id']

    def attachSticker(self,card_id,imagen=config['sticker'],top='-0.62',left='0',zIndex='1',rotate='11'):
        query_sticker = self.basic_query
        query_sticker['image']=imagen
        query_sticker['top']=top
        query_sticker['left']=left
        query_sticker['zIndex']=zIndex
        query_sticker['rotate']=rotate
        url = f"https://api.trello.com/1/cards/{card_id}/stickers"
        return requests.request("POST",url,headers=self.headers,params=query_sticker,timeout=200)

    def getCard(self,idCard):
        url=f"https://api.trello.com/1/cards/{idCard}"
        res = requests.request("GET",url,headers=self.headers,params=self.basic_query,timeout=200)
        return json.loads(res.text)
    
    def getCardsBoard(self,idBoard):
        url = f"https://api.trello.com/1/boards/{idBoard}/cards"
        res = requests.request("GET",url,params=self.basic_query,timeout=200)
        return json.loads(res.text)
    def getCardsList(self,idList):
        url = f"https://api.trello.com/1/lists/{idList}/cards"
        res = requests.request("GET",url,headers=self.headers,params=self.basic_query,timeout=200)
        return json.loads(res.text)


    def checkFormat(self,titulo,desc,dla):
        MAX_DAY_WO_ACTIVITY=14
        error={
            'titulo':titulo,
            'body':{},
            'ultimaActividad':{}
        }
        lastActivity=dla[0:10].split('-')
        dateTicket=datetime.datetime(int(lastActivity[0]),int(lastActivity[1]),int(lastActivity[2]))
        dateNow=datetime.datetime.now()
        diffDay=dateNow-dateTicket
        if diffDay.days>MAX_DAY_WO_ACTIVITY:
            error['ultimaActividad']['check']=True
            error['ultimaActividad']['comment']=f'El ticken no tiene actividad hace mas de {MAX_DAY_WO_ACTIVITY} dias'
        else:
            error['ultimaActividad']['check']=False
            error['ultimaActividad']['comment']=f''
        if '## Acceptance Criteria' in desc and '## Motivation' in desc:
            error['body']['check']=False
            error['body']['comment']=''
        else:
            error['body']['check']=True
            error['body']['comment']=f'Formato incorrecto del body'
        return error


    def getTags(self,tablero=config['tablero']):
        url_tags = f"https://api.trello.com/1/boards/{tablero}/labels"
        tags = requests.request("GET",url_tags,params=self.basic_query)
        tags_r = json.loads(tags.text)
        return {t['name']:t['id'] for t in tags_r}

    def makeTags(self,card_id,card,tags_board,tag_color=config['color_tags'],tablero=config['tablero']):
        url_add_label = f"https://api.trello.com/1/cards/{card_id}/idLabels"
        for t in card.tags:
            query_add = self.basic_query
            if t in tags_board.keys():
                #print(tags_board[t],t)
                query_add['value']=tags_board[t]
            else:
                query_tag = self.basic_query
                query_tag['name']=t
                query_tag['color']=tag_color
                url_create_tag = f"https://api.trello.com/1/boards/{tablero}/labels"
                res_tag = requests.request("POST",url_create_tag,params=query_tag,timeout=200)
                id_tag=json.loads(res_tag.text)['id']
                query_add['value']=id_tag
            res_add_tag = requests.request("POST",url_add_label,params=query_add,timeout=200)

    def assignMember(self,card_id,memberId=config['member']):
        query=self.basic_query
        query['value']=memberId
        url=f"https://api.trello.com/1/cards/{card_id}/idMembers"
        res_assign= requests.request("POST",url,params=query,timeout=200)


    def createCards(self,card):
        print('creating card')
        card_id=self.createCard(card)
        print('attaching sticker')
        res_sticker = self.attachSticker(card_id)
        print('getTags from board')
        res_tags = self.getTags()
        print('create tags that dont exist and add to card')
        self.makeTags(card_id,card,res_tags)
        print('assign a member to the card')
        self.assignMember(card_id)


#tc.createCards(tc.tickets[0])
#card_id=tc.createCard(tc.tickets[1],config['list'])
#tc.attachSticker('64857b3e95d4715fc0d564de')