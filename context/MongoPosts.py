from mongoengine import *

connect('Gamble_Bot_Database', host='mongodb+srv://Nikholas:nik220171@discordbotproject-41c9w.gcp.mongodb.net'
        '/Gamble_Bot_Database?retryWrites=true&w=majority')


class UserPost(Document):
    user_name = StringField(required=True, max_length=200)
    user_money = FloatField(default=200)
    user_games_won = IntField(default=0)
