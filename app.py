from models.Ticket import Ticket
from TrelloClient import TrelloClient as TC

data = Ticket.load('./data.json')
tc = TC(tickets=data)
print(tc.tickets)