from models.Ticket import Ticket
from TrelloClient import TrelloClient as TC

data = Ticket.load('./data.json')
tc = TC(tickets=data)
#card=tc.getCard('#idcard')
#check=tc.checkFormat(card['name'],card['desc'],card['dateLastActivity'])
#print(check)
cards=tc.getCardsList('#idList')
for c in cards:
    errors=tc.checkFormat(c)
    if errors['body']['check'] or errors['ultimaActividad']['check']:
        print(errors)
